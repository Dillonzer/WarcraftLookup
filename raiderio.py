from interactions import Extension, slash_command, Embed, BrandColors, SlashContext, OptionType, slash_option, AutocompleteContext, SlashCommandChoice, Button, ButtonStyle, Client
from test_consts import Consts
import requests
import json
from error import Error
from battlenet import BattleNet
from datetime import datetime

_battleNet = BattleNet()

class RaiderIO(Extension):
    guild_ids = [642081591371497472]

    @slash_command(name="mythic_plus_rating", description="Get current mythic plus season rating for a character.", scopes=guild_ids)
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
        if(data is None):
            e = Error.GetErrorEmbed()
            await ctx.send(embeds = e)
        else:    
            profileButton = Button(
                style=ButtonStyle.URL,
                label=f"{data["name"]}'s Raider.IO Page",
                url=data["profile_url"],
            )
            e = Embed()
            e.color = BrandColors.YELLOW
            seasonName = self.GetNameForSlug_MythicPlus(data["mythic_plus_scores_by_season"][0]["season"])
            e.title = f"{data["name"]}"
            e.set_author(name=f"Mythic+ {seasonName}")
            e.description = f"{data["race"]} {data["class"]}"
            e.add_field(name="DPS", value=data["mythic_plus_scores_by_season"][0]["scores"]["dps"], inline=True)
            e.add_field(name="Healer", value=data["mythic_plus_scores_by_season"][0]["scores"]["healer"], inline=True)
            e.add_field(name="Tank", value=data["mythic_plus_scores_by_season"][0]["scores"]["tank"], inline=True)
            e.set_thumbnail(url=data["thumbnail_url"])
            e.set_footer(text="Powered by Raider.IO", icon_url="https://cdn.raiderio.net/images/brand/Icon_FullColor_Square.png")
            await ctx.send(embeds = e, components=profileButton)

    @slash_command(name="raid_progress", description="Get current expansions raid progression information for a character", scopes=guild_ids)
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
    async def RaidProgression(self, ctx: SlashContext, name, region, realm):        
        await ctx.defer()
        data = self.GetRaiderIOData(name, realm, region)
        if(data is None):
            e = Error.GetErrorEmbed()
            await ctx.send(embeds = e)
        else:    
            profileButton = Button(
                style=ButtonStyle.URL,
                label=f"{data["name"]}'s Raider.IO Page",
                url=data["profile_url"],
            )
            e = Embed()
            e.color = BrandColors.YELLOW
            e.title = f"{data["name"]}"
            e.set_author(name=f"Raid Progression")
            e.description = f"{data["race"]} {data["class"]}"
            for key, value in data["raid_progression"].items():
                raidName = RaiderIO.GetNameForSlug_Raid(key)
                e.add_field(name=raidName, value=f"{value["normal_bosses_killed"]} N\n{value["heroic_bosses_killed"]} H\n{value["mythic_bosses_killed"]} M", inline=True)
            e.set_thumbnail(url=data["thumbnail_url"])
            e.set_footer(text="Powered by Raider.IO", icon_url="https://cdn.raiderio.net/images/brand/Icon_FullColor_Square.png")
            await ctx.send(embeds = e, components=profileButton)
       
    @MythicPlusRating.autocomplete("realm")
    @RaidProgression.autocomplete("realm")
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
            if(response.status_code != 200):
                return None
            
            jsonObject = json.loads(response.text.encode('utf8'))

            return jsonObject   
        except Exception as e:
            print(f"Failed to hit RaiderIO due to {e}.")
            return None
        
    @staticmethod
    def GetStaticSeasonData():
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
    def GetStaticRaidData():
        try:
            url = f"https://raider.io/api/v1/raiding/static-data?expansion_id={Consts.CURRENT_EXPANSION_ID}"

            payload={}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)
            jsonObject = json.loads(response.text.encode('utf8'))

            return jsonObject   
        except Exception as e:
            print(f"Failed to hit RaiderIO due to {e}.")
            return None
        
    @staticmethod
    def GetNameForSlug_MythicPlus(name):
        staticData = RaiderIO.GetStaticSeasonData()        
        for data in staticData["seasons"]:
            if(name == data["slug"]):
                return data["name"]
    
    @staticmethod
    def GetNameForSlug_Raid(name):
        staticData = RaiderIO.GetStaticRaidData()        
        for data in staticData["raids"]:
            if(name == data["slug"]):
                return data["name"]
        