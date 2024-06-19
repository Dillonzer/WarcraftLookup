from consts import Consts
import requests
import json

class RaiderIO_Helper:
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
    def GetRaiderIOGuildData(name, realm, region):
        try:
            url = f"https://raider.io/api/v1/guilds/profile?region={region}&realm={realm}&name={name}&fields=raid_progression,raid_rankings"

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
            url = f"https://raider.io/api/v1/mythic-plus/static-data?expansion_id={Consts.RAIDERIO_EXPANSION_ID}"

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
            url = f"https://raider.io/api/v1/raiding/static-data?expansion_id={Consts.RAIDERIO_EXPANSION_ID}"

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
        staticData = RaiderIO_Helper.GetStaticSeasonData()        
        for data in staticData['seasons']:
            if(name == data['slug']):
                return data['name']
    
    @staticmethod
    def GetNameForSlug_Raid(name):
        staticData = RaiderIO_Helper.GetStaticRaidData()        
        for data in staticData['raids']:
            if(name == data['slug']):
                return data['name']