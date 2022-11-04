from quart import Quart, redirect, render_template, url_for, request
from quart_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from nextcord.ext import ipc
import os
from dotenv import load_dotenv
from helper_functions import check_guild

load_dotenv()

app = Quart(__name__)
app.secret_key = "Hercules"
ipc_client = ipc.Client(secret_key="Hercules")

app.config["DISCORD_CLIENT_ID"] = os.getenv("CLIENT_ID")
app.config["DISCORD_CLIENT_SECRET"] = os.getenv("CLIENT_SECRET")
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:5000/callback"
app.config["DISCORD_BOT_TOKEN"] = os.getenv("BOT_TOKEN")
discord = DiscordOAuth2Session(app)

@app.route("/")
async def index():
    guild_count = await ipc_client.request("get_guild_count")
    return str(guild_count)

@app.route("/login/")
async def login():
    return await discord.create_session()

@app.route("/callback/")
async def callback():
    try:
        await discord.callback()
    except:
        return redirect(url_for("login"))
    return redirect(url_for("select_server"))

@app.errorhandler(Unauthorized)
async def redirect_unauthorized(error):
    """
    This is the error handler for the error which is raised when an 
    unauthorized user tries to access some routes which requires authorization.
    """
    return redirect(url_for("login"))

@app.route("/select_server/")
@requires_authorization
async def select_server():
    bot_guild_ids = await ipc_client.request("get_guild_ids")
    user_guilds = await discord.fetch_guilds()
    mutual_guilds = [guild for guild in user_guilds if guild.permissions.manage_guild and int(guild.id) in bot_guild_ids]
    return await render_template("select_server.html", mutual_guilds = mutual_guilds)

@app.route("/dashboard/<int:guild_id>/")
@requires_authorization
async def dashboard(guild_id):
    guild = await check_guild(guild_id, discord)
    if not guild:
        return await render_template("no_dashboard_access.html", reason="not in guild")
    if not guild.permissions.manage_guild:
        return await render_template("no_dashboard_access.html", reason="no permission")
    return await render_template("dashboard.html", guild = guild)

@app.route("/dashboard/<int:guild_id>/autorole", methods=['GET', 'POST'])
@requires_authorization
async def autorole(guild_id):
    form = await request.form
    guild = await check_guild(guild_id, discord)
    if not guild:
        return await render_template("no_dashboard_access.html", reason="not in guild")
    if not guild.permissions.manage_guild:
        return await render_template("no_dashboard_access.html", reason="no permission")

    # This condition is true when the user submits the form
    if request.method == "POST":
        role_id = form['role-id']
        role = guild.fetch_roles()
        return role
    return await render_template('autorole.html')

if __name__ == "__main__":
    app.run(debug=True)