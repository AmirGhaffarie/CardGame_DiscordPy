import os
from pathlib import Path
# emojis
EMOJIS_DROP = "<:Drop:893384648057552917>"
EMOJIS_SKIP = "<:Skip:895004188348657724>"
EMOJIS_SKIPLEFT = "<:SkipLeft:901033048148148267>"
EMOJIS_CHECKMARK = "<a:check_mark_button:892593202400469052>"
EMOJIS_COIN = "<:Coin:931482402419789824>"

# timers
DROP_TIMEOUT = 20
LONG_COMMAND_TIMEOUT = 120
# settings
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_ADDRESS = os.path.join(BASE_DIR,'BotConfig.cfg')
LOCAL_MEDIA_FILES = True
DJANGO_SERVER_ADDRESS = "http://127.0.0.1:8000/base"

LOCAL_MEDIA_ADDRESS = (
    "C:/Users/amirg/Desktop/PythonProjects/CardgameBackend_Django/CardGameDB"
)
REMOTE_MEDIA_ADDRESS = "http://146.70.88.124:10020"
INVENTORY_PAGE_SIZE = 10