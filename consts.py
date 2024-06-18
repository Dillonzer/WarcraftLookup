from os import environ

class Consts:    
    BOT_ID = environ.get('BOT_ID')
    TOKEN = environ.get('TOKEN')
    CURRENT_EXPANSION_ID = 9 #Dragonflight   
    BATTLENET_BASICAUTH = environ.get('BATTLENET_BASICAUTH')
    WARCRAFTLOGS_BASICAUTH = environ.get('WARCRAFTLOGS_BASICAUTH')
    REGION_US = 'us'
    REGION_EU = 'eu'