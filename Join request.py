# ==========================================
#        J.A.R.V.I.S PROTOCOL INITIALIZED
# ==========================================
#   Creator   : Mister Stark
#   System    : Telegram AI Bot
#   Level     : Advanced Automation
#   Security  : Stark Shield Enabled 🛡️
# ==========================================

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import logging
import asyncio
# ==============================
# 🔑 TOKEN YAHAN DAALO
# ==============================
API_TOKEN = ""
# ==============================
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
# ==============================
# 🚀 START / WELCOME MESSAGE
# ==============================
@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    caption_text = """
<b>👋 ʜᴇʟʟᴏ  !</b>
<b>❍ ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ʀᴇǫᴜᴇsᴛ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ ʙᴏᴛ. 🥳</b>
<b>✦━━━━━━━━━━━━━━━━━━━━━✦</b>
<b>🛠 ғᴇᴀᴛᴜʀᴇs :</b>
<b>❍ Jᴏɪɴ ʀᴇǫᴜᴇsᴛ's ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ ɪɴ ɢʀᴏᴜᴘ.</b>
<b>❍ Aᴄᴄᴇᴘᴛ ✅  / Dᴇᴄʟɪɴᴇ ❌  ɪɴʟɪɴᴇ ʙᴜᴛᴛᴏɴs.</b>
<b>❍ Oɴʟʏ Aᴅᴍɪɴ / Oᴡɴᴇʀ ᴄᴀɴ ᴀᴘᴘʀᴏᴠᴇ.</b>
<b>✦━━━━━━━━━━━━━━━━━━━━━✦</b>
<b>➤ ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ : <a href="https://t.me/CarelessxOwner">˹ᴍɪsᴛᴇʀ ꭙ
sᴛᴀʀᴋ˼</a></b>
<b>➤ ᴍᴏʀᴇ ʙᴏᴛs : <a href="https://t.me/StarkxNetwrk">˹sᴛᴀʀᴋ ꭙ ɴᴇᴛᴡᴏʀᴋ˼</a></b>
<b>➤ ᴘᴏᴡᴇʀᴇᴅ ʙʏ : <a href="https://t.me/ll_CarelessxCoder_ll">˹ᴄᴀʀᴇʟᴇss ꭙ ᴄᴏᴅᴇʀ˼</a></b>
<b>╰─━━━  ✦ ❀ ✦ ❖ ✦ ❀ ✦   ━━━─╯</b>
"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    # Row 1
    keyboard.add(
        InlineKeyboardButton(
            "˹ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ˼",
            url="https://t.me/Request_ccbot?startgroup=true"
        )
    )
    # Row 2
    keyboard.add(
        InlineKeyboardButton(
            "˹ᴏᴡɴᴇʀ˼",
            url="https://t.me/CarelessxOwner"
        )
    )
    # Row 3
    keyboard.row(
        InlineKeyboardButton(
            "˹ᴜᴘᴅᴀᴛᴇ˼",
            url="https://t.me/ll_CarelessxCoder_ll"
        ),
        InlineKeyboardButton(
            "˹sᴜᴘᴘᴏʀᴛ˼",
            url="https://t.me/CarelessxWorld"
        )
    )
    await bot.send_photo(
        message.chat.id,
        photo="https://files.catbox.moe/dgelfj.jpg",
        caption=caption_text,
        parse_mode="HTML",
        reply_markup=keyboard,
        has_spoiler=True
    )

# ==============================
# 👥 JOIN REQUEST HANDLER
# ==============================
@dp.chat_join_request_handler()
async def handle_join_request(join_request: types.ChatJoinRequest):
    user = join_request.from_user
    chat_id = join_request.chat.id
    username = f"@{user.username}" if user.username else "No Username"
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("✅  ᴀᴄᴄᴇᴘᴛ", callback_data=f"accept_{user.id}"),
        InlineKeyboardButton("❌  ᴅᴇᴄʟɪɴᴇ", callback_data=f"decline_{user.id}")
    )
    await bot.send_message(
        chat_id,
        f"👤 <b>{user.full_name}</b>\n"
        f"𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲: {username}\n\n"
        f"<b>🥳 Hᴇ ʜᴀs sᴇɴᴛ ᴀ ᴊᴏɪɴ ʀᴇǫᴜᴇsᴛ.</b>",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
# ==============================
# ✅  ACCEPT BUTTON
# ==============================
@dp.callback_query_handler(lambda c: c.data.startswith("accept_"))
async def approve_user(callback_query: types.CallbackQuery):
    user_id = int(callback_query.data.split("_")[1])
    chat_id = callback_query.message.chat.id
    clicker_id = callback_query.from_user.id
    member = await bot.get_chat_member(chat_id, clicker_id)
    if member.status not in ["administrator", "creator"]:
        await callback_query.answer(
            "❌  ᴏɴʟʏ ᴀᴅᴍɪɴ / ᴏᴡɴᴇʀ ᴄᴀɴ ᴀᴘᴘʀᴏᴠᴇ ᴛʜɪs!",
            show_alert=True
        )
        return
    await bot.approve_chat_join_request(chat_id, user_id)
    await callback_query.message.edit_text("✅  ᴜsᴇʀ ᴀᴘᴘʀᴏᴠᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ")
    await callback_query.answer()
    await asyncio.sleep(5)
    await callback_query.message.delete()
# ==============================
# ❌  DECLINE BUTTON
# ==============================
@dp.callback_query_handler(lambda c: c.data.startswith("decline_"))
async def decline_user(callback_query: types.CallbackQuery):
    user_id = int(callback_query.data.split("_")[1])
    chat_id = callback_query.message.chat.id
    clicker_id = callback_query.from_user.id
    member = await bot.get_chat_member(chat_id, clicker_id)
    if member.status not in ["administrator", "creator"]:
        await callback_query.answer(
            "❌  ᴏɴʟʏ ᴀᴅᴍɪɴ / ᴏᴡɴᴇʀ ᴄᴀɴ ᴅᴇᴄʟɪɴᴇ ᴛʜɪs!",
            show_alert=True
        )
        return
    await bot.decline_chat_join_request(chat_id, user_id)
    await callback_query.message.edit_text("❌  ᴜsᴇʀ ᴅᴇᴄʟɪɴᴇ sᴜᴄᴄᴇssғᴜʟʟʏ")
    await callback_query.answer()
    await asyncio.sleep(5)
    await callback_query.message.delete()
# ==============================
# ▶️ START BOT
# ==============================
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
