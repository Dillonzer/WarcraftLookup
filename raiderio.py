from interactions import Extension, slash_command, Embed, BrandColors, SlashContext, OptionType, slash_option
from test_consts import Consts
import requests
import json
from error import Error

class RaiderIO(Extension):
    guild_ids = [642081591371497472]

    @slash_command(name="mythic_plus_rating", description="Get your current mythic plus season rating", scopes=guild_ids)
    @slash_option(
        name="name",
        description="Character Name",
        required=True,
        opt_type=OptionType.STRING
    )
    @slash_option(
        name="realm",
        description="Character's Realm",
        required=True,
        opt_type=OptionType.STRING
    )
    @slash_option(
        name="region",
        description="Character's Region",
        required=True,
        opt_type=OptionType.STRING
    )
    async def MythicPlusRating(self, ctx: SlashContext, name, realm, region):        
        data = self.GetRaiderIOData(name, realm, region)
        if(data is None):
            e = Error.GetErrorEmbed()
        else:    
            e = Embed()
            e.color = BrandColors.YELLOW
            seasonName = self.GetNameForSlug(data["mythic_plus_scores_by_season"][0]["season"])
            e.title = f"Mythic+ {seasonName}"
            e.description = f"DPS: {data["mythic_plus_scores_by_season"][0]["scores"]["dps"]}\nHealer: {data["mythic_plus_scores_by_season"][0]["scores"]["healer"]}\nTank: {data["mythic_plus_scores_by_season"][0]["scores"]["tank"]}"
            e.set_thumbnail(url=data["thumbnail_url"])
            e.set_footer(text="Powered by RaiderIO", icon_url="https://cdn.raiderio.net/images/brand/Icon_FullColor_Square.png")

        await ctx.send(embeds = e)

    @staticmethod
    def GetRaiderIOData(name, realm, region):
        try:
            url = f"https://raider.io/api/v1/characters/profile?region={region}&realm={realm}&name={name}&fields=gear,talents,mythic_plus_scores_by_season:current,mythic_plus_ranks,raid_progression"

            payload={}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)
            jsonObject = json.loads(response.text.encode('utf8'))

            return jsonObject   
        except Exception as e:
            print(f"Failed to hit RaiderIO due to {e}.")
            return None
        
    @staticmethod
    def GetStaticSeasonAndRaidData():
        try:
            url = f"https://raider.io/api/v1/mythic-plus/static-data?expansion_id={Consts.CURRENT_EXPANSION_ID}"

            payload={}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)
            jsonObject = json.loads(response.text.encode('utf8'))

            return jsonObject   
        except Exception as e:
            print(f"Failed to hit RaiderIO due to {e}.")
            return None
        
    @staticmethod
    def GetNameForSlug(name):
        staticData = RaiderIO.GetStaticSeasonAndRaidData()        
        for data in staticData["seasons"]:
            if(name == data["slug"]):
                return data["name"]
        