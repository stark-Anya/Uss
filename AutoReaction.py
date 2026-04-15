# ==========================================
#        J.A.R.V.I.S PROTOCOL INITIALIZED
# ==========================================
#   Creator   : Mister Stark
#   System    : Telegram AI Bot
#   Level     : Advanced Automation
#   Security  : Stark Shield Enabled 🛡️
# ==========================================



from telegram import (
    Update,
    ReactionTypeEmoji,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto
)
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
import random
import asyncio
BOT_TOKEN = ""
WELCOME_IMAGE = "https://files.catbox.moe/dgelfj.jpg"
REACTIONS = [
"👍","👎","❤️","🔥","🥰","👏","😁","🤩","😎","🤗",
"😇","👀","🎉","😂","😍","💯","😆","😜","🤔","😢",
"😭","😡","😱","😈","💋","⚡ ","🍓","🍾","🏆","💔",
"🤬","👻","☃️","🧑‍💻","🙉","🙈","🙊","🕊️",
"🤷","🤷🏻‍♀️"
]
# ================= WELCOME DESIGN =================
WELCOME_TEXT = """
<b>👋 ʜᴇʟʟᴏ  !</b>
<b>❍ ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ᴧᴜᴛᴏ ᴇᴍᴏᴊɪ ʀᴇᴧᴄᴛɪᴏη ʙᴏᴛ.  🎉</b>
<b>✦━━━━━━━━━━━━━━━━━━━━━✦</b>
<b>🛠 ғᴇᴀᴛᴜʀᴇs :</b>
<b>❍ ɪ ᴧᴜᴛᴏᴍᴧᴛɪᴄᴧʟʟʏ ʀᴇᴧᴄᴛ ᴛᴏ ᴍᴇꜱꜱᴧɢᴇꜱ.</b>
<b>❍ ᴍᴧᴋᴇ ʏᴏᴜʀ ᴄʜᴧᴛ ᴍᴏʀᴇ ꜰᴜη ᴧηᴅ ᴇηᴇʀɢᴇᴛɪᴄ.</b>
<b>❍ ᴧᴅᴅ ᴇxᴘʀᴇꜱꜱɪᴏη ᴛᴏ ᴇᴠᴇʀʏ ᴍᴇꜱꜱᴧɢᴇ.</b>
<b>✦━━━━━━━━━━━━━━━━━━━━━✦</b>
<b>➤ ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ : <a href="https://t.me/CarelessxOwner">˹ᴍɪsᴛᴇʀ ꭙ
sᴛᴀʀᴋ˼</a></b>
<b>➤ ᴍᴏʀᴇ ʙᴏᴛs : <a href="https://t.me/StarkxNetwrk">˹sᴛᴀʀᴋ ꭙ ɴᴇᴛᴡᴏʀᴋ˼</a></b>
<b>➤ ᴘᴏᴡᴇʀᴇᴅ ʙʏ : <a href="https://t.me/ll_CarelessxCoder_ll">˹ᴄᴀʀᴇʟᴇss ꭙ ᴄᴏᴅᴇʀ˼</a></b>
<b>╰─━━━  ✦ ❀ ✦ ❖ ✦ ❀ ✦   ━━━─╯</b>
"""
# ================= BUTTON DESIGN =================
keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("˹ᴀᴅᴅ ᴍє ɪη ʏσᴜʀ ɢʀσᴜᴘ˼", url="https://t.me/AutoReact_ccbot?startgroup=true")],
    [InlineKeyboardButton("˹❍ᴡηєʀ˼", url="https://t.me/CarelessxOwner")],
    [
        InlineKeyboardButton("˹sᴜᴘᴘσʀᴛ˼", url="https://t.me/CarelessxWorld"),
        InlineKeyboardButton("˹ᴜᴘᴅᴀᴛᴇ˼", url="https://t.me/ll_CarelessxCoder_ll")
    ]
])
# ================= AUTO REACTION (UNCHANGED) =================
async def auto_react(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    if update.effective_chat.type not in ["group", "supergroup"]:
        return
    emoji = random.choice(REACTIONS)
    try:
        await asyncio.sleep(0.1)
        await context.bot.set_message_reaction(
            chat_id=update.effective_chat.id,
            message_id=update.message.message_id,
            reaction=[ReactionTypeEmoji(emoji)]
        )
    except:
        pass
# ================= START COMMAND =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=WELCOME_IMAGE,
        caption=WELCOME_TEXT,
        parse_mode="HTML",
        reply_markup=keyboard,
        has_spoiler=True  # 🔥 Blur Image Effect
    )
# ================= BOT START =================
app = (
    ApplicationBuilder()
    .token(BOT_TOKEN)
    .concurrent_updates(True)
    .build()
)
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.ALL, auto_react))
print("🔥 Designed Reaction Bot Running...")
app.run_polling()
