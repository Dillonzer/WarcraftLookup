from interactions import Extension, slash_command, Embed, BrandColors, SlashContext, OptionType, slash_option, AutocompleteContext, SlashCommandChoice
from test_consts import Consts
import requests
import json
from error import Error
from battlenet import BattleNet

_battleNet = BattleNet()

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
        name="region",
        description="Character's Region",
        required=True,
        opt_type=OptionType.STRING,
        choices=[
        SlashCommandChoice(name="United States", value=Consts.REGION_US),
        SlashCommandChoice(name="Europe", value=Consts.REGION_EU)
        ]
    )
    @slash_option(
        name="realm",
        description="Character's Realm",
        required=True,
        opt_type=OptionType.STRING,
        autocomplete=True
    )
    async def MythicPlusRating(self, ctx: SlashContext, name, region, realm):        
        data = self.GetRaiderIOData(name, realm, region)
        if(data["name"] is None):
            e = Error.GetErrorEmbed()
        else:    
            e = Embed()
            e.color = BrandColors.YELLOW
            seasonName = self.GetNameForSlug(data["mythic_plus_scores_by_season"][0]["season"])
            e.title = f"Mythic+ {seasonName}"
            e.author = f"{data["name"]}"
            e.description = f"{data["race"]} - {data["class"]}"
            e.add_field(name="DPS", value=data["mythic_plus_scores_by_season"][0]["scores"]["dps"], inline=True)
            e.add_field(name="Healer", value=data["mythic_plus_scores_by_season"][0]["scores"]["healer"], inline=True)
            e.add_field(name="Tank", value=data["mythic_plus_scores_by_season"][0]["scores"]["tank"], inline=True)
            e.set_thumbnail(url=data["thumbnail_url"])
            e.set_footer(text="Powered by RaiderIO", icon_url="https://cdn.raiderio.net/images/brand/Icon_FullColor_Square.png")

        await ctx.send(embeds = e)

    @MythicPlusRating.autocomplete("realm")
    async def autocompleteRealm(self, ctx: AutocompleteContext):  
        try:
            region = ctx.kwargs.get("region")
            realmList = _battleNet.GetRealms(region) 
            choices = [
                SlashCommandChoice(name = realm["name"], value = realm["slug"]) for realm in realmList["realms"] if ctx.input_text.lower() in realm["name"].lower()
            ] 

            if(len(choices) > 25):
                choices = choices[0:25]

            await ctx.send(choices)
        except:
            pass

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
        