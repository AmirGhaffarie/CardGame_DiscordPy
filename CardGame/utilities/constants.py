import os
from pathlib import Path
from datas import common_emojis

# emojis
EMOJIS_DROP = "GENERIC_CHOOSEARROW"
EMOJIS_SKIP = "GENERIC_RIGHTARROW"
EMOJIS_SKIPLEFT = "GENERIC_LEFTARROW"
EMOJIS_COOLDOWN_CHECK = "COOLDOWN_CHECK"
EMOJIS_COIN = "<:Coin:931482402419789824>"

ICON_TOPRIGHT = (
    "https://i.pinimg.com/originals/ed/76/df/ed76df1b5da78ca7317a01cf9a648d0c.gif"
)

# timers
DROP_TIMEOUT = 20
LONG_COMMAND_TIMEOUT = 120
# settings
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE_ADDRESS = os.path.join(BASE_DIR, "Configs", "BotConfig.cfg")
LOCALIZATION_FILE_ADDRESS = os.path.join(BASE_DIR, "Configs", "localization.xlsx")

DB_ADDRESS = "http://django.db:8020"
DB_BASE_ADDRESS = "http://django.db:8020/base"
DB_CONFIGS_ADDRESS = "http://django.db:8020/configs"

TEMP_FILE_ADDRESS = "/opt/app/CardGame/temp"

LOCAL_MEDIA_FILES = True
LOCAL_MEDIA_ADDRESS = "/opt/app"
REMOTE_MEDIA_ADDRESS = "http://146.70.88.124:10020"

INVENTORY_PAGE_SIZE = 10
