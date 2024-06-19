from interactions import Extension, slash_command, Embed, BrandColors, SlashContext, OptionType, slash_option, AutocompleteContext, SlashCommandChoice, Button, ButtonStyle
from consts import Consts
import requests
import json
from error import Error
from battlenet import BattleNet
from raiderio_helper import RaiderIO_Helper

guild_ids = [642081591371497472]
_battleNet = BattleNet()

class WarcraftLogs(Extension):
    def __init__(self, bot):
        self.Authentication()
        pass

    def Authentication(self):
        try:
            url = "https://www.warcraftlogs.com/oauth/token"

            payload = {'grant_type': 'client_credentials'}
            files=[

            ]
            headers = {
            'Authorization': f'Basic {Consts.WARCRAFTLOGS_BASICAUTH}'
            }

            response = requests.request("POST", url, headers=headers, data=payload, files=files)
            jsonObject = json.loads(response.text.encode('utf8'))
            self.AccessToken = jsonObject['access_token']   
            print('Retrieved WarcraftLogs Authentication!')   
        except Exception as e:
            print(f"Failed to hit WarcraftLogs Auth due to {e}.")
            return None
        
    def GetCharacterData(self, name, realm, region, zoneId, metric):
        try:
            url = "https://www.warcraftlogs.com/api/v2/client"

            payload = "{\"query\":\"query($name: String!, $server: String!, $region: String!, $zoneId: Int!)\\r\\n{\\r\\n    characterData{\\r\\n        character(name: $name, serverSlug: $server, serverRegion: $region)\\r\\n        {\\r\\n               id\\r\\n               name\\r\\n               classID                             \\r\\n               faction\\r\\n               {\\r\\n                   id\\r\\n                   name\\r\\n               }\\r\\n               zoneRankings(zoneID: $zoneId, metric: "+metric+")\\r\\n               \\r\\n        }\\r\\n    }\\r\\n}\",\"variables\":{\"name\":\""+name+"\",\"server\":\""+realm+"\",\"region\":\""+region+"\",\"zoneId\":"+str(zoneId)+"}}"
            headers = {
            'Authorization': f'Bearer {self.AccessToken}',
            'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            jsonObject = json.loads(response.text.encode('utf8'))
            return jsonObject
        except Exception as e:
            print(f"Failed to hit WarcraftLogs Character due to {e}.")
            self.Authentication()
            return None
        
    def GetRaidZones(self):
        try:
            url = "https://www.warcraftlogs.com/api/v2/client"
            payload = "{\"query\":\"query($id: Int!)\\r\\n{\\r\\n    worldData\\r\\n    {\\r\\n        zones(expansion_id: $id)\\r\\n        {\\r\\n            id\\r\\n            name\\r\\n        }\\r\\n    }\\r\\n}\",\"variables\":{\"id\":"+str(Consts.WARCRAFTLOGS_EXPANSION_ID)+"}}"
            headers = {
            'Authorization': f'Bearer {self.AccessToken}',
            'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            jsonObject = json.loads(response.text.encode('utf8'))
            return jsonObject
        except Exception as e:
            print(f"Failed to hit WarcraftLogs Zones due to {e}.")
            self.Authentication()
            return None
        
    def GetClassName(self, classId):
        try:
            url = "https://www.warcraftlogs.com/api/v2/client"
            payload = "{\"query\":\"query($id: Int!)\\r\\n{\\r\\n    gameData\\r\\n    {\\r\\n        class(id: $id)\\r\\n        {\\r\\n            name\\r\\n        }\\r\\n    }\\r\\n\\r\\n}\",\"variables\":{\"id\":"+str(classId)+"}}"
            headers = {
            'Authorization': f'Bearer {self.AccessToken}',
            'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            jsonObject = json.loads(response.text.encode('utf8'))
            return jsonObject['data']['gameData']['class']['name']
        except Exception as e:
            print(f"Failed to hit WarcraftLogs Class Name due to {e}.")
            self.Authentication()
            return None
        
    def GetEncounterName(self, encounterId):       
        raidZones = self.GetRaidZones() 
        for raid in raidZones['data']['worldData']['zones']:
            if(str(encounterId) == str(raid['id'])):
                return raid['name']
    
    def GetDifficulty(diffId):
        switch={
            Consts.LFR: "LFR",
            Consts.NORMAL: "Normal",
            Consts.HEROIC: "Heroic",
            Consts.MYTHIC: "Mythic",
        }
        return switch.get(diffId,"")

    @slash_command(name="warcraft_logs", description="Get a character's specific logs for a raid or season.")
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
    @slash_option(
        name="encounter",
        description="The Raid or Mythic+ Season",
        required=True,
        opt_type=OptionType.STRING,
        autocomplete=True
    )
    @slash_option(
        name="metric",
        description="Check which type of logs to look at, DPS or Healing",
        required=True,
        opt_type=OptionType.STRING,
        choices=[
        SlashCommandChoice(name="Damage", value='dps'),
        SlashCommandChoice(name="Healing", value='hps')
        ]
    )
    async def WarcraftLogRetrieval(self, ctx: SlashContext, name, region, realm, encounter, metric): 
        await ctx.defer()  
        data = self.GetCharacterData(name, realm, region, encounter, metric)
        charInfo = RaiderIO_Helper.GetRaiderIOData(name, realm, region)
        if(data is None or charInfo is None):
            e = Error.GetErrorEmbed()
            await ctx.send(embeds = e)
        else:    
            profileButton = Button(
                style=ButtonStyle.URL,
                label=f"{charInfo['name']}'s WarcraftLog's Page",
                url=f"https://www.warcraftlogs.com/character/id/{data['data']['characterData']['character']['id']}",
            )
            e = Embed()
            e.color = BrandColors.BLURPLE
            e.title = f"{data['data']['characterData']['character']['name']}"
            encounterName = self.GetEncounterName(encounter)
            e.set_author(name=f"Logs for {encounterName} - {WarcraftLogs.GetDifficulty(data['data']['characterData']['character']['zoneRankings']['difficulty'])}")
            e.description = f"{charInfo['race']} {charInfo['class']}"
            for rankings in data['data']['characterData']['character']['zoneRankings']['rankings']:
                if(rankings['rankPercent'] is not None):
                    e.add_field(name=rankings['encounter']['name'], value=round(rankings['rankPercent'],2), inline=True)
                else:            
                    e.add_field(name=rankings['encounter']['name'], value="No Kills Logged", inline=True)
            e.set_thumbnail(url=charInfo['thumbnail_url'])
            e.set_footer(text="Powered by WarcraftLogs", icon_url="https://assets.rpglogs.com/img/warcraft/favicon.png?v=2")
            await ctx.send(embeds = e, components=profileButton)
        
    @WarcraftLogRetrieval.autocomplete("encounter")
    async def autocompleteEncounter(self, ctx: AutocompleteContext):  
        try:
            encounters = self.GetRaidZones()
            choices = [
                SlashCommandChoice(name = raid['name'], value = raid['id']) for raid in encounters['data']['worldData']['zones'] if ctx.input_text.lower() in raid['name'].lower()
            ] 

            if(len(choices) > 25):
                choices = choices[0:25]

            await ctx.send(choices)
        except:
            pass

    @WarcraftLogRetrieval.autocomplete("realm")
    async def autocompleteRealm(self, ctx: AutocompleteContext):  
        try:
            region = ctx.kwargs.get("region")
            realmList = _battleNet.GetRealms(region) 
            choices = [
                SlashCommandChoice(name = realm['name'], value = realm['slug']) for realm in realmList['realms'] if ctx.input_text.lower() in realm['name'].lower()
            ] 

            if(len(choices) > 25):
                choices = choices[0:25]

            await ctx.send(choices)
        except:
            pass

