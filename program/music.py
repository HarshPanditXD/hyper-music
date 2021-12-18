# Copyright (C) 2021 By Veez Music-Project
# Commit Start Date 20/10/2021
# Finished On 28/10/2021

import re
import asyncio

from config import ASSISTANT_NAME, BOT_USERNAME, IMG_1, IMG_2
from driver.filters import command, other_filters
from driver.queues import QUEUE, add_to_queue
from driver.veez import call_py, user
from driver.utils import bash
from pyrogram import Client
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped
from youtubesearchpython import VideosSearch


def ytsearch(query: str):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        songname = data["title"]
        url = data["link"]
        duration = data["duration"]
        thumbnail = f"https://i.ytimg.com/vi/{data['id']}/hqdefault.jpg"
        return [songname, url, duration, thumbnail]
    except Exception as e:
        print(e)
        return 0


async def ytdl(format: str, link: str):
    stdout, stderr = await bash(f'youtube-dl -g -f "{format}" {link}')
    if stdout:
        return 1, stdout.split("\n")[0]
    return 0, stderr


@Client.on_message(command(["play", f"play@{BOT_USERNAME}"]) & other_filters)
async def play(c: Client, m: Message):
    await m.delete()
    replied = m.reply_to_message
    chat_id = m.chat.id
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="• Mᴇɴᴜ", callback_data="cbmenu"),
                InlineKeyboardButton(text="• Cʟᴏsᴇ", callback_data="cls"),
            ]
        ]
    )
    if m.sender_chat:
        return await m.reply_text("you're an __Anonymous__ Admin !\n\n» revert back to user account from admin rights.")
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"✌️Tᴏ ᴜsᴇ ᴍᴇ, I ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴀɴ **Aᴅᴍɪɴɪsᴛʀᴀᴛᴏʀ** Wɪᴛʜ ᴛʜᴇ Fᴏʟʟᴏᴡɪɴɢ✌️ **Pᴇʀᴍɪssɪᴏɴs**:\n\n» ✌️ __Dᴇʟᴇᴛᴇ Mᴇssᴀɢᴇs__\n» ✌️ __Aᴅᴅ Usᴇʀs__\n» ✌️ __Mᴀɴᴀɢᴇ Vᴏɪᴄᴇ Cʜᴀᴛ__\n\nData is **Uᴘᴅᴀᴛᴇᴅ** Aᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ Aғᴛᴇʀ Yᴏᴜ **Pʀᴏᴍᴏᴛᴇ Mᴇ**"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
            "Mɪssɪɴɢ Rᴇϙᴜɪʀᴇᴅ Pᴇʀᴍɪssɪᴏɴ❔:" + "\n\n» ✌️ __Mᴀɴᴀɢᴇ Vᴏɪᴄᴇ Cʜᴀᴛ__"
        )
        return
    if not a.can_delete_messages:
        await m.reply_text(
            "Mɪssɪɴɢ Rᴇϙᴜɪʀᴇᴅ Pᴇʀᴍɪssɪᴏɴ❔:" + "\n\n» 🗑️ __Dᴇʟᴇᴛᴇ Mᴇssᴀɢᴇs__"
        )
        return
    if not a.can_invite_users:
        await m.reply_text("Mɪssɪɴɢ Rᴇϙᴜɪʀᴇᴅ Pᴇʀᴍɪssɪᴏɴ✌️:" + "\n\n» ✌️ __Aᴅᴅ Usᴇʀ__")
        return
    try:
        ubot = (await user.get_me()).id
        b = await c.get_chat_member(chat_id, ubot)
        if b.status == "kicked":
            await m.reply_text(
                f"@{ASSISTANT_NAME} **Is ʙᴀɴɴᴇᴅ ɪɴ Gʀᴏᴜᴘ** {m.chat.title}\n\n» **Uɴʙᴀɴ ᴛʜᴇ ᴜsᴇʀʙᴏᴛ ғɪʀsᴛ ɪғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴜsᴇ ᴛʜɪs Bᴏᴛ.**"
            )
            return
    except UserNotParticipant:
        if m.chat.username:
            try:
                await user.join_chat(m.chat.username)
            except Exception as e:
                await m.reply_text(f"✌️ **Usᴇʀʙᴏᴛ ғᴀɪʟᴇᴅ ᴛᴏ Jᴏɪɴ**\n\n**Rᴇᴀsᴏɴ**: `{e}`")
                return
        else:
            try:
                invitelink = await c.export_chat_invite_link(
                    m.chat.id
                )
                if invitelink.startswith("https://t.me/+"):
                    invitelink = invitelink.replace(
                        "https://t.me/+", "https://t.me/joinchat/"
                    )
                await user.join_chat(invitelink)
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                return await m.reply_text(
                    f"✌️ **Usᴇʀʙᴏᴛ Tᴏ Jᴏɪɴ**\n\n**reason**: `{e}`"
                )
    if replied:
        if replied.audio or replied.voice:
            suhu = await replied.reply("📥 **downloading audio...**")
            dl = await replied.download()
            link = replied.link
            if replied.audio:
                if replied.audio.title:
                    songname = replied.audio.title[:70]
                else:
                    if replied.audio.file_name:
                        songname = replied.audio.file_name[:70]
                    else:
                        songname = "Audio"
            elif replied.voice:
                songname = "Voice Note"
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await suhu.delete()
                await m.reply_photo(
                    photo=f"{IMG_1}",
                    caption=f"✌️ **Tʀᴀᴄᴋ Aᴅᴅᴇᴅ Tᴏ Qᴜᴇᴜᴇ »** `{pos}`\n\n🏷 **Name:** [{songname}]({link})\n💭 **Chat:** `{chat_id}`\n🎧 **Request by:** {m.from_user.mention()}",
                    reply_markup=keyboard,
                )
            else:
             try:
                await suhu.edit("🔄 **✌️Pʟᴀʏɪɴɢ Oɴ Vᴄ Sᴏɴɢs✌️...**")
                await call_py.join_group_call(
                    chat_id,
                    AudioPiped(
                        dl,
                    ),
                    stream_type=StreamType().local_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await suhu.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                await m.reply_photo(
                    photo=f"{IMG_2}",
                    caption=f"✌️ Mᴜsɪᴄ Pʟᴀʏɪɴɢ sᴛᴀʀᴛᴇᴅ ✌️**.**\n\n🏷 **Name:** [{songname}]({link})\n💭 **Chat:** `{chat_id}`\n💡 **Status:** `Playing`\n🎧 **Request by:** {requester}",
                    reply_markup=keyboard,
                )
             except Exception as e:
                await suhu.delete()
                await m.reply_text(f"🚫єгг๏г❔:\n\n» {e}")
        else:
            if len(m.command) < 2:
                await m.reply(
                    "» ✨Rᴇᴘʟʏ Tᴏ Aɴ ✨ **Aᴜᴅɪᴏ Fɪʟᴇ** or **😂Gɪᴠᴇ Sᴏᴍᴇᴛʜɪɴɢ Tᴏ Sᴇᴀʀᴄʜ✨🙀.**"
                )
            else:
                suhu = await c.send_message(chat_id, "🔍 🐱**Sᴇᴀʀᴄʜɪɴɢ Sᴏɴɢs ✌️🎧..**")
                query = m.text.split(None, 1)[1]
                search = ytsearch(query)
                if search == 0:
                    await suhu.edit("✌️ **Nᴏ Rᴇsᴜʟᴛs Fᴏᴜɴᴅ.✌️**")
                else:
                    songname = search[0]
                    url = search[1]
                    duration = search[2]
                    thumbnail = search[3]
                    format = "bestaudio[ext=m4a]"
                    veez, ytlink = await ytdl(format, url)
                    if veez == 0:
                        await suhu.edit(f"❌ yt-dl issues detected\n\n» `{ytlink}`")
                    else:
                        if chat_id in QUEUE:
                            pos = add_to_queue(
                                chat_id, songname, ytlink, url, "Audio", 0
                            )
                            await suhu.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_photo(
                                photo=thumbnail,
                                caption=f" **Tʀᴀᴄᴋ Aᴅᴅᴇᴅ Tᴏ Qᴜᴇᴜᴇ✨ »** `{pos}`\n\n🏷 **Name:** [{songname}]({url})\n**⏱ Duration:** `{duration}`\n🎧 **Request by:** {requester}",
                                reply_markup=keyboard,
                            )
                        else:
                            try:
                                await suhu.edit("🔄 **😂Jᴏɪɴɪɴɢ Vᴄ Sᴏɴɢ Pʟᴀʏɪɴɢ🎧🙀.**")
                                await call_py.join_group_call(
                                    chat_id,
                                    AudioPiped(
                                        ytlink,
                                    ),
                                    stream_type=StreamType().local_stream,
                                )
                                add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                                await suhu.delete()
                                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                                await m.reply_photo(
                                    photo=thumbnail,
                                    caption=f"✌️ **Mᴜsɪᴄ Pʟᴀʏɪɴɢ Sᴛᴀʀᴛᴇᴅ.**\n\n🏷 **Name:** [{songname}]({url})\n**⏱ Duration:** `{duration}`\n✌️ **Status:** `Playing`\n🎧 **Request by:** {requester}",
                                    reply_markup=keyboard,
                                )
                            except Exception as ep:
                                await suhu.delete()
                                await m.reply_text(f"🚫єгг๏г❔: `{ep}`")

    else:
        if len(m.command) < 2:
            await m.reply(
                "» reply to an **Aᴜᴅɪᴏ Fɪʟᴇ** or **Gɪᴠᴇ Sᴏᴍᴇᴛʜɪɴɢ Tᴏ Sᴇᴀʀᴄʜ Sᴏɴɢs.**"
            )
        else:
            suhu = await c.send_message(chat_id, "🔍**✌️Sᴇᴀʀᴄʜɪɴɢ. Sᴏɴɢs🎧✌️..**")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            if search == 0:
                await suhu.edit("🤧 **✨Nᴏ Sᴏɴɢs Fᴏᴜɴᴅ🤧❔.**")
            else:
                songname = search[0]
                url = search[1]
                duration = search[2]
                thumbnail = search[3]
                format = "bestaudio[ext=m4a]"
                veez, ytlink = await ytdl(format, url)
                if veez == 0:
                    await suhu.edit(f"❌ yt-dl issues detected\n\n» `{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                        await suhu.delete()
                        requester = (
                            f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                        )
                        await m.reply_photo(
                            photo=thumbnail,
                            caption=f"✌️ **Tʀᴀᴄᴋ Aᴅᴅᴇᴅ Tᴏ Qᴜᴇᴜᴇ »** `{pos}`\n\n🏷 **Nᴀᴍᴇ:** [{songname}]({url})\n**⏱ Dᴜʀᴀᴛɪᴏɴ:** `{duration}`\n🎧 **Rᴇϙᴜᴇsᴛ Bʏ:** {requester}",
                            reply_markup=keyboard,
                        )
                    else:
                        try:
                            await suhu.edit("🔄 **Jᴏɪɴɪɴɢ Vᴄ Sᴏɴɢ Pʟᴀʏɪɴɢ✌️...**")
                            await call_py.join_group_call(
                                chat_id,
                                AudioPiped(
                                    ytlink,
                                ),
                                stream_type=StreamType().local_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                            await suhu.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_photo(
                                photo=thumbnail,
                                caption=f"✌️ **Mᴜsɪᴄ Pʟᴀʏɪɴɢ Sᴛᴀʀᴛᴇᴅ.**\n\n🏷 **Nᴀᴍᴇ:** [{songname}]({url})\n**⏱ Dᴜʀᴀᴛɪᴏɴ:** `{duration}`\n💡 **Sᴛᴀᴛᴜs:** `Playing`\n🎧 **Rᴇϙᴜᴇsᴛ Bʏ:** {requester}",
                                reply_markup=keyboard,
                            )
                        except Exception as ep:
                            await suhu.delete()
                            await m.reply_text(f"🚫ҽɾɾօɾ❔: `{ep}`")
