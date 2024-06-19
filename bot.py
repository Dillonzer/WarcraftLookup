from interactions import Client, listen
from consts import Consts

bot = Client(token=Consts.TOKEN)
bot.load_extension("information")
bot.load_extension("raiderio")
bot.load_extension("warcraftlogs")

@listen()
async def on_startup():
    await bot.change_presence(activity="World of Warcraft")

bot.start()
