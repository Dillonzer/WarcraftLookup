from interactions import Embed, BrandColors
from test_consts import Consts

class Error():
    @staticmethod
    def GetErrorEmbed():
        e = Embed()
        e.color = BrandColors.RED
        e.title = "Work is da poop!"
        e.description = "Looks like there was an issue with this command, reach out to [Dillonzer](discord.gg/SqpJZn2) if this issue presists"
        e.set_author(name="Warcraft Lookup")#,icon_url=Consts.LOGO_ADDRESS)
        #e.set_thumbnail(url="poop orc")
        return e