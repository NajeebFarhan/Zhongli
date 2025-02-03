import hikari
import hikari.intents
import tanjun
from dotenv import load_dotenv
import os

load_dotenv()


def build_bot() -> hikari.GatewayBot:

    Intents = hikari.intents.Intents
    INTENTS = (
        Intents.ALL_GUILDS
        | Intents.DM_MESSAGES
        | Intents.GUILD_MESSAGES
        | Intents.MESSAGE_CONTENT
    )

    TOKEN = os.environ.get("BOT_TOKEN")
    bot = hikari.GatewayBot(TOKEN, intents=INTENTS)
    make_client(bot)

    return bot


def make_client(bot: hikari.GatewayBot) -> tanjun.Client:
    PREFIX = os.environ.get("BOT_PREFIX")

    client = (
        tanjun.Client.from_gateway_bot(
            bot, mention_prefix=True, declare_global_commands=True
        )
    ).add_prefix(PREFIX)

    client.load_modules("bot.plugins.text")

    return client
