import os
import re
import subprocess
import sys
import traceback
from inspect import getfullargspec
from io import StringIO
from time import time

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from TEAMZYRO import app
from config import OWNER_ID, EVAL

# Async Python code executor
async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {a}" for a in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)

# Edit or reply handler
async def edit_or_reply(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    await func(**{k: v for k, v in kwargs.items() if k in spec})

# Eval handler
@app.on_edited_message(filters.command("eval") & filters.user(EVAL) & ~filters.forwarded & ~filters.via_bot)
@app.on_message(filters.command("eval") & filters.user(EVAL) & ~filters.forwarded & ~filters.via_bot)
async def executor(client: app, message: Message):
    if len(message.command) < 2:
        return await edit_or_reply(message, text="<b>ᴡʜᴀᴛ ʏᴏᴜ ᴡᴀɴɴᴀ ᴇxᴇᴄᴜᴛᴇ ʙᴀʙʏ ?</b>")

    try:
        cmd = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await message.delete()

    t1 = time()
    old_stderr, old_stdout = sys.stderr, sys.stdout
    redirected_output, redirected_error = StringIO(), StringIO()
    sys.stdout, sys.stderr = redirected_output, redirected_error

    exc = None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()

    sys.stdout, sys.stderr = old_stdout, old_stderr
    stdout, stderr = redirected_output.getvalue(), redirected_error.getvalue()

    result = exc or stderr or stdout or "Success"
    final_output = f"<b>⥤ ʀᴇsᴜʟᴛ :</b>\n<pre language='python'>{result}</pre>"

    t2 = time()
    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("⏳", callback_data=f"runtime {round(t2 - t1, 3)} Seconds"),
            InlineKeyboardButton("🗑", callback_data=f"forceclose abc|{message.from_user.id}")
        ]]
    )

    if len(final_output) > 4096:
        filename = "output.txt"
        with open(filename, "w+", encoding="utf-8") as f:
            f.write(result)
        await message.reply_document(
            document=filename,
            caption=f"<b>⥤ ᴇᴠᴀʟ :</b>\n<code>{cmd[:980]}</code>\n\n<b>⥤ ʀᴇsᴜʟᴛ :</b>\nAttached Document",
            quote=False,
            reply_markup=keyboard,
        )
        os.remove(filename)
        await message.delete()
    else:
        await edit_or_reply(message, text=final_output, reply_markup=keyboard)

# Runtime response
@app.on_callback_query(filters.regex(r"runtime"))
async def runtime_func_cq(_, cq):
    runtime = cq.data.split(None, 1)[1]
    await cq.answer(runtime, show_alert=True)

# Force close eval result
@app.on_callback_query(filters.regex("forceclose"))
async def forceclose_command(_, cq):
    try:
        _, payload = cq.data.split(None, 1)
        _, user_id = payload.split("|")
    except:
        return
    if cq.from_user.id != int(user_id):
        return await cq.answer("» ʟɪᴍɪᴛ ᴇxᴄᴇᴇᴅᴇᴅ.", show_alert=True)
    try:
        await cq.message.delete()
        await cq.answer()
    except:
        pass

# Shell command runner
@app.on_edited_message(filters.command("sh") & filters.user(EVAL) & ~filters.forwarded & ~filters.via_bot)
@app.on_message(filters.command("sh") & filters.user(EVAL) & ~filters.forwarded & ~filters.via_bot)
async def shellrunner(_, message: Message):
    if len(message.command) < 2:
        return await edit_or_reply(message, text="<b>ᴇxᴀᴍᴩʟᴇ :</b>\n/sh git pull")

    text = message.text.split(None, 1)[1]
    output = ""

    commands = text.splitlines() if "\n" in text else [text]
    for cmd in commands:
        shell = re.split(r""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", cmd)
        try:
            process = subprocess.Popen(shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            out_text = out.decode().strip()
            err_text = err.decode().strip()
            output += f"\n<b>$ {cmd}</b>\n"
            output += f"<pre>{out_text or err_text or 'Success'}</pre>\n"
        except Exception as e:
            error_trace = traceback.format_exc()
            output += f"\n<b>$ {cmd}</b>\n<pre>{error_trace}</pre>\n"

    if len(output) > 4096:
        with open("output.txt", "w+", encoding="utf-8") as f:
            f.write(output)
        await app.send_document(
            chat_id=message.chat.id,
            document="output.txt",
            reply_to_message_id=message.id,
            caption="<b>OUTPUT</b>",
        )
        os.remove("output.txt")
    else:
        await edit_or_reply(message, text=output)

    await message.stop_propagation()
