import os
from os import getenv
from dotenv import load_dotenv

if os.path.exists("local.env"):
    load_dotenv("local.env")

load_dotenv()
admins = {}
SESSION_NAME = getenv("SESSION_NAME", "session")
BOT_TOKEN = getenv("BOT_TOKEN")
BOT_NAME = getenv("BOT_NAME", "MUSIC")
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
OWNER_NAME = getenv("OWNER_NAME", "HARSH_PANDIT)
ALIVE_NAME = getenv("ALIVE_NAME", "HYPER")
BOT_USERNAME = getenv("BOT_USERNAME", "UNIQUE_SOCIETY)
ASSISTANT_NAME = getenv("ASSISTANT_NAME", "HYPERMEN_ASSISTANT")
GROUP_SUPPORT = getenv("GROUP_SUPPORT", "KIARA_SUPPORT)
UPDATES_CHANNEL = getenv("UPDATES_CHANNEL", "LOVE_X_POISON)
SUDO_USERS = list(map(int, getenv("SUDO_USERS").split()))
COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ ! .").split())
ALIVE_IMG = getenv("ALIVE_IMG", "https://telegra.ph/file/f819b0e13c279ff09e69b.jpg")
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "60"))
UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/levina-lab/video-stream")
IMG_1 = getenv("IMG_1", "https://telegra.ph/file/f819b0e13c279ff09e69b.jpg")
IMG_2 = getenv("IMG_2", "https://telegra.ph/file/6213d2673486beca02967.png")
IMG_3 = getenv("IMG_3", "https://telegra.ph/file/18224dde07348970107b3.jpg")
IMG_4 = getenv("IMG_4", "https://telegra.ph/file/f819b0e13c279ff09e69b.jpg")
