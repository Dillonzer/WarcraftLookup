from test_consts import Consts
import requests
import json

class WarcraftLogs:
    def __init__(self):
        self.Authentication()

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
        
    def GetCharacterData(self, name, realm, region):
        try:
            url = "https://www.warcraftlogs.com/api/v2/client"

            payload = "{\"query\":\"query($name: String!, $server: String!, $region: String!)\\r\\n{\\r\\n    characterData{\\r\\n        character(name: $name, serverSlug: $server, serverRegion: $region)\\r\\n        {\\r\\n name\\r\\n level\\r\\n classID\\r\\n server\\r\\n {\\r\\n     id\\r\\n     slug\\r\\n     region\\r\\n     {\\r\\n         id\\r\\n         slug\\r\\n         name\\r\\n     }\\r\\n } \\r\\n faction\\r\\n {\\r\\n     id\\r\\n     name\\r\\n }\\r\\n encounterRankings(encounterID: 62521) #Will need to use this to pull specific parses\\r\\n zoneRankings #Seems to show the current most recent Raid\\r\\n \\r\\n        }\\r\\n    }\\r\\n}\",\"variables\":{\"name\":\""+name+"\",\"server\":\""+realm+"\",\"region\":\""+region+"\"}}"
            headers = {
            'Authorization': f'Bearer {self.AccessToken}',
            'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            jsonObject = json.loads(response.text.encode('utf8'))
            return jsonObject
        except Exception as e:
            print(f"Failed to hit WarcraftLogs Character due to {e}.")
            return None