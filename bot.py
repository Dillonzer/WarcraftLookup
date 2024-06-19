from interactions import Client
from consts import Consts
import aiohttp

bot = Client(token=Consts.TOKEN)
bot.load_extension("information")
bot.load_extension("raiderio")
bot.load_extension("warcraftlogs")

bot.start()
