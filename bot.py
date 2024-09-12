from interactions import Client, listen, Task, IntervalTrigger
from consts import Consts
import aiohttp

bot = Client(token=Consts.TOKEN)
bot.load_extension("information")
bot.load_extension("raiderio")
bot.load_extension("warcraftlogs")

@Task.create(IntervalTrigger(minutes=10))
async def ListServers():
    if(Consts.TOPGG_AUTHTOKEN is not None):
        async with aiohttp.ClientSession() as session:
            headers = {
                    'Content-Type': "application/json",
                    'Authorization': f"Bearer {Consts.TOPGG_AUTHTOKEN}",
                    'Accept': "*/*",
                    'Host': "top.gg",
                    }
            servercount = len(bot.guilds)
            async with session.post(url="https://top.gg/api/bots/1252000060867215490/stats", json={'server_count': servercount}, headers=headers) as response:                
                print("List Server POST Status:", response.status)

@listen()
async def on_startup():
    await bot.change_presence(activity="World of Warcraft")
    ListServers.start()

bot.start()
