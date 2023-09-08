import os
from os import getenv, environ
from dotenv import load_dotenv



load_dotenv()

class Var(object):

# if heroku acc get banned then change this main vars
# AKS_APP_NAME is same as APP_NAME, IN BOTH VARS ADD SAME HEROKU APP NAME
    if 'DYNO' in environ:
        ON_HEROKU = True
        APP_NAME = str(getenv('APP_NAME'))    
    else:
        ON_HEROKU = False
    AKS_APP_NAME = "aks-file-to-link-ashubhskeleton1.koyeb.app"

#end

    
    MULTI_CLIENT = False
    API_ID = int(getenv('API_ID', '24781773'))
    API_HASH = str(getenv('API_HASH', 'ad907569f68cab06c733794fc91be7b6'))
    BOT_TOKEN = str(getenv('BOT_TOKEN', '6048839696:AAHFqRNlvdPvV_cQSvm3NJ5tmwphrKCRupg'))
    name = str(getenv('name', 'aks-on-bot'))
    SLEEP_THRESHOLD = int(getenv('SLEEP_THRESHOLD', '60'))
    WORKERS = int(getenv('WORKERS', '4'))
    BIN_CHANNEL = int(getenv('BIN_CHANNEL', '-1001696019751'))
    PORT = int(getenv('PORT', 8080))
    BIND_ADRESS = str(getenv('WEB_SERVER_BIND_ADDRESS', '0.0.0.0'))
    PING_INTERVAL = int(environ.get("PING_INTERVAL", "1200"))  # 20 minutes
    OWNER_ID = set(int(x) for x in os.environ.get("OWNER_ID", "1030335104").split())  
    NO_PORT = bool(getenv('NO_PORT', False))
    APP_NAME = str(getenv('APP_NAME'))
    OWNER_USERNAME = str(getenv('OWNER_USERNAME', 'Aks_support01_bot'))
    FQDN = str(getenv('FQDN', BIND_ADRESS)) if not ON_HEROKU or getenv('FQDN') else APP_NAME+'.herokuapp.com'
    HAS_SSL=bool(getenv('HAS_SSL',False))
    if HAS_SSL:
        URL = "https://{}/".format(FQDN)
    else:
        URL = "https://{}/".format(FQDN)
    DATABASE_URL = str(getenv('DATABASE_URL', 'mongodb+srv://akstechnical33:akstechnical3333@cluster0.nytdi94.mongodb.net/?retryWrites=true&w=majority'))
    UPDATES_CHANNEL = str(getenv('UPDATES_CHANNEL', 'Aksbackup'))
    BANNED_CHANNELS = list(set(int(x) for x in str(getenv("BANNED_CHANNELS", "-1001362659779")).split())) 


















