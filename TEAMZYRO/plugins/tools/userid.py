from TEAMZYRO import app
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.errors import PeerIdInvalid, ChannelInvalid

@app.on_message(filters.command('id'))
async def getid(client, message):
    chat = message.chat
    your_id = message.from_user.id
    message_id = message.id
    reply = message.reply_to_message

    text = f"**[ᴍᴇssᴀɢᴇ ɪᴅ:]({message.link})** `{message_id}`\n"
    text += f"**[ʏᴏᴜʀ ɪᴅ:](tg://user?id={your_id})** `{your_id}`\n"

    # Handle command arguments for user ID lookup
    if len(message.command) == 2:
        try:
            split = message.text.split(None, 1)[1].strip()
            user = await client.get_users(split)
            text += f"**[ᴜsᴇʀ ɪᴅ:](tg://user?id={user.id})** `{user.id}`\n"
        except (PeerIdInvalid, ValueError):
            return await message.reply_text("ᴛʜɪs ᴜsᴇʀ ᴅᴏᴇsɴ'ᴛ ᴇxɪsᴛ ᴏʀ ɪs ɪɴᴠᴀʟɪᴅ.", quote=True)

    # Handle chat ID safely
    try:
        text += f"**[ᴄʜᴀᴛ ɪᴅ:](https://t.me/{chat.username})** `{chat.id}`\n\n"
    except Exception as e:
        text += f"**ᴄʜᴀᴛ ɪᴅ:** `Error: {str(e)}`\n\n"

    # Handle replied message
    if (
        not getattr(reply, "empty", True)
        and not reply.forward_from_chat
        and not reply.sender_chat
    ):
        try:
            text += f"**[ʀᴇᴘʟɪᴇᴅ ᴍᴇssᴀɢᴇ ɪᴅ:]({reply.link})** `{reply.id}`\n"
            text += f"**[ʀᴇᴘʟɪᴇᴅ ᴜsᴇʀ ɪᴅ:](tg://user?id={reply.from_user.id})** `{reply.from_user.id}`\n\n"
        except Exception as e:
            text += f"**ʀᴇᴘʟɪᴇᴅ ᴍᴇssᴀɢᴇ:** `Error: {str(e)}`\n\n"

    # Handle forwarded messages from channels
    if reply and reply.forward_from_chat:
        try:
            text += f"ᴛʜᴇ ғᴏʀᴡᴀʀᴅᴇᴅ ᴄʜᴀɴɴᴇʟ, {reply.forward_from_chat.title}, ʜᴀs ᴀɴ ɪᴅ ᴏғ `{reply.forward_from_chat.id}`\n\n"
            print(f"Forwarded from chat: {reply.forward_from_chat}")  # Debug log
        except (PeerIdInvalid, ChannelInvalid) as e:
            text += f"**ғᴏʀᴡᴀʀᴅᴇᴅ ᴄʜᴀɴɴᴇʟ:** `Error: {str(e)}`\n\n"
            print(f"Error accessing forwarded chat: {str(e)}")  # Debug log

    # Handle sender chat (e.g., anonymous admins or channels)
    if reply and reply.sender_chat:
        try:
            text += f"ɪᴅ ᴏғ ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ ᴄʜᴀᴛ/ᴄʜᴀɴɴᴇʟ, ɪs `{reply.sender_chat.id}`\n"
            print(f"Sender chat: {reply.sender_chat}")  # Debug log
        except (PeerIdInvalid, ChannelInvalid) as e:
            text += f"**ʀᴇᴘʟɪᴇᴅ ᴄʜᴀᴛ/ᴄʜᴀɴɴᴇʟ:** `Error: {str(e)}`\n"
            print(f"Error accessing sender chat: {str(e)}")  # Debug log

    await message.reply_text(
        text,
        disable_web_page_preview=True,
        parse_mode=ParseMode.DEFAULT,
    )

# Optional: Add a custom error handler for background updates
@app.on_raw_update()
async def handle_raw_update(client, update, users, chats):
    try:
        # Process updates as needed
        pass
    except (PeerIdInvalid, ChannelInvalid) as e:
        print(f"Error in raw update: Invalid peer ID {str(e)}")
        # Optionally log to a file or notify admin
