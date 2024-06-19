from consts import Consts
import requests
import json

class BattleNet:
    def __init__(self):
        self.Authentication()

    def Authentication(self):
        try:
            url = "https://oauth.battle.net/token"

            payload = {'grant_type': 'client_credentials'}
            files=[

            ]
            headers = {
            'Authorization': f'Basic {Consts.BATTLENET_BASICAUTH}'
            }

            response = requests.request("POST", url, headers=headers, data=payload, files=files)
            jsonObject = json.loads(response.text.encode('utf8'))
            self.AccessToken = jsonObject['access_token']   
            print('Retrieved Battle.net Authentication!')   
        except Exception as e:
            print(f"Failed to hit Battle.Net Auth due to {e}.")
            return None

    
    def GetRealms(self, region):
        try:
            url = f"https://{region}.api.blizzard.com/data/wow/realm/index?namespace=dynamic-{region}&locale=en_US"

            payload = {}
            headers = {
            'Authorization': f'Bearer {self.AccessToken}'
            }

            response = requests.request("GET", url, headers=headers, data=payload)
            jsonObject = json.loads(response.text.encode('utf8'))

            return jsonObject         
        except Exception as e:
            print(f"Failed to hit Battle.Net Realms due to {e}.")
            self.Authentication()
            return None