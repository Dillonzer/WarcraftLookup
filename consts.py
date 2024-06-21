from os import environ

class Consts:    
    BOT_ID = environ.get('BOT_ID')
    TOKEN = environ.get('TOKEN') 
    RAIDERIO_EXPANSION_ID = 9 #Dragonflight
    WARCRAFTLOGS_EXPANSION_ID = 5 #Dragonflight
    BATTLENET_BASICAUTH = environ.get('BATTLENET_BASICAUTH')
    WARCRAFTLOGS_BASICAUTH = environ.get('WARCRAFTLOGS_BASICAUTH')
    TOPGG_AUTHTOKEN = environ.get('TOPGG_AUTHTOKEN')
    REGION_US = 'us'
    REGION_EU = 'eu'
    MYTHIC = 5
    HEROIC = 4
    NORMAL = 3
    LFR = 1
    LOGO = "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/!Logos/WL_Logo.png"