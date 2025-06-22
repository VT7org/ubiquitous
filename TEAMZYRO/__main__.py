import asyncio
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from TEAMZYRO import LOGGER, app, userbot
from TEAMZYRO.core.call import ZYRO
from TEAMZYRO.misc import sudo
from TEAMZYRO.plugins import ALL_MODULES
from TEAMZYRO.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("String Session is Missing , Please fill 𝐀 PyrogramV2 Session")
        exit()
    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("TEAMZYRO.plugins" + all_module)
    LOGGER("TEAMZYRO.plugins").info("All Plugins Loaded Successfully 🍃...")
    await userbot.start()
    await ZYRO.start()
    try:
        await ZYRO.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("TEAMZYRO").error(
            "Please Start Videochat In Logger Gc\n\nZYRO start the VC & Restart the Music Bot........"
        )
        exit()
    except:
        pass
    await ZYRO.decorators()
    LOGGER("TEAMZYRO").info(
        "✯\n ᴄᴏ-ᴘᴏᴡᴇʀᴇᴅ ʙʏ\n @BillaSpace"
    )
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("TEAMZYRO").info("sᴘᴀᴄᴇ-x sᴛᴏᴘᴘᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ...")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
