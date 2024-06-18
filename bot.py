from interactions import Client
from test_consts import Consts
#import aiohttp
#import asyncio

bot = Client(token=Consts.TOKEN)
bot.load_extension("information")
bot.load_extension("raiderio")

bot.start()
