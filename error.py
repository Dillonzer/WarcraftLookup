from interactions import Embed, BrandColors
from test_consts import Consts

class Error():
    @staticmethod
    def GetErrorEmbed():
        e = Embed()
        e.color = BrandColors.RED
        e.title = "Looks like we cannot process this request."
        e.description = "Looks like there was an issue with this command, either the player cannot be found or something else happened. Reach out to [Dillonzer](https://discord.gg/SqpJZn2) if this issue presists"
        e.set_author(name="WEEO-WEEO")
        e.set_thumbnail(url="https://wow.zamimg.com/images/wow/icons/large/trade_engineering.jpg")
        return e