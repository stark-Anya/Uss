"""
╔══════════════════════════════════════════════════════════════╗
║          DUAL JOIN REQUEST BOT - Single File                 ║
║  • Do alag bots ek saath ek file se                         ║
║  • Dono ki alag-alag settings (alag JSON file)              ║
║  • Jis bot pe /start karo usi ka panel khule                ║
║  • Same owner/admin dono manage kar sake                     ║
╚══════════════════════════════════════════════════════════════╝

SETUP:
1. pip install python-telegram-bot==20.7
2. Niche BOT_1_TOKEN, BOT_2_TOKEN set karo
3. OWNER_ID aur ADMIN_IDS set karo
4. python dual_bot.py

"""

import json
import os
import logging
import asyncio
import threading
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes, ChatJoinRequestHandler
)
from telegram.constants import ParseMode

logging.basicConfig(
    format='%(asctime)s [%(name)s] %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ════════════════════════════════════════════════
#         ⚙️ CONFIGURATION — YAHAN SET KARO
# ════════════════════════════════════════════════

BOT_1_TOKEN = "TOKEN_1_YAHAN"        # Pehle bot ka token (BotFather se)
BOT_2_TOKEN = "TOKEN_2_YAHAN"        # Doosre bot ka token (BotFather se)

OWNER_ID  = 123456789                # Apna Telegram user ID
ADMIN_IDS = [123456789, 987654321]   # Owner + extra admins (OWNER_ID bhi daalo)

# Dono bots ki settings alag-alag files mein save hongi
SETTINGS_FILES = {
    "bot1": "settings_bot1.json",
    "bot2": "settings_bot2.json",
}

DEFAULT_SETTINGS = {
    "auto_approve": True,
    "message_type": "text",       # "text" | "photo" | "video"
    "message_text": "👋 <b>Welcome!</b>\n\nAapki join request receive ho gayi!\n\nJald approve karenge ✅",
    "media_file_id": None,
    "inline_buttons": [],         # [{"text": "...", "url": "..."}]
    "stats": {"total": 0, "approved": 0},
}


# ════════════════════════════════════════════════
#              💾 Per-Bot Settings
# ════════════════════════════════════════════════

def load_settings(bot_key: str) -> dict:
    path = SETTINGS_FILES[bot_key]
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # naye keys default se fill karo
        for k, v in DEFAULT_SETTINGS.items():
            if k not in data:
                data[k] = v
        return data
    return DEFAULT_SETTINGS.copy()


def save_settings(bot_key: str, settings: dict):
    path = SETTINGS_FILES[bot_key]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)


# ════════════════════════════════════════════════
#              🔑 Auth Check
# ════════════════════════════════════════════════

def is_authorized(user_id: int) -> bool:
    return user_id == OWNER_ID or user_id in ADMIN_IDS


# ════════════════════════════════════════════════
#              🎛️ Keyboards
# ════════════════════════════════════════════════

def main_menu_kb(settings: dict) -> InlineKeyboardMarkup:
    aa = "✅ ON" if settings["auto_approve"] else "❌ OFF"
    mt = {"text": "📝 Text", "photo": "🖼️ Image+Text", "video": "🎥 Video+Text"}.get(settings["message_type"], "📝 Text")
    bc = len(settings["inline_buttons"])
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"🤖 Auto Approve: {aa}", callback_data="toggle_approve")],
        [InlineKeyboardButton(f"✏️ Message Set Karo  ({mt})", callback_data="set_message")],
        [InlineKeyboardButton(f"🔘 Inline Buttons ({bc})", callback_data="manage_buttons")],
        [InlineKeyboardButton("👁️ Preview", callback_data="preview"),
         InlineKeyboardButton("🚀 Publish", callback_data="publish")],
        [InlineKeyboardButton("📊 Stats", callback_data="stats")],
    ])


def message_type_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 Sirf Text", callback_data="msg_type_text"),
         InlineKeyboardButton("🖼️ Image + Text", callback_data="msg_type_photo")],
        [InlineKeyboardButton("🎥 Video + Text", callback_data="msg_type_video")],
        [InlineKeyboardButton("🔙 Back", callback_data="back_main")],
    ])


def buttons_manager_kb(settings: dict) -> InlineKeyboardMarkup:
    rows = []
    for i, btn in enumerate(settings["inline_buttons"]):
        rows.append([InlineKeyboardButton(f"❌ {btn['text']}", callback_data=f"remove_btn_{i}")])
    rows.append([InlineKeyboardButton("➕ Naya Button Add Karo", callback_data="add_button")])
    rows.append([InlineKeyboardButton("🔙 Back", callback_data="back_main")])
    return InlineKeyboardMarkup(rows)


def after_save_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Button Add Karo", callback_data="manage_buttons")],
        [InlineKeyboardButton("👁️ Preview", callback_data="preview")],
        [InlineKeyboardButton("🔙 Main Menu", callback_data="back_main")],
    ])


def after_button_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Aur Button Add Karo", callback_data="add_button")],
        [InlineKeyboardButton("👁️ Preview", callback_data="preview")],
        [InlineKeyboardButton("🔙 Main Menu", callback_data="back_main")],
    ])


# ════════════════════════════════════════════════
#              📤 Send Message Helper
# ════════════════════════════════════════════════

async def send_bot_message(bot, chat_id: int, settings: dict, user_name: str = ""):
    text = settings.get("message_text", "👋 Welcome!")
    if user_name:
        text = text.replace("{name}", user_name).replace("{first_name}", user_name)

    media_id  = settings.get("media_file_id")
    msg_type  = settings.get("message_type", "text")
    buttons   = settings.get("inline_buttons", [])

    inline_kb = None
    if buttons:
        inline_kb = InlineKeyboardMarkup(
            [[InlineKeyboardButton(b["text"], url=b["url"])] for b in buttons]
        )

    if msg_type == "photo" and media_id:
        await bot.send_photo(chat_id=chat_id, photo=media_id,
                             caption=text, parse_mode=ParseMode.HTML,
                             reply_markup=inline_kb)
    elif msg_type == "video" and media_id:
        await bot.send_video(chat_id=chat_id, video=media_id,
                             caption=text, parse_mode=ParseMode.HTML,
                             reply_markup=inline_kb)
    else:
        await bot.send_message(chat_id=chat_id, text=text,
                               parse_mode=ParseMode.HTML,
                               reply_markup=inline_kb)


# ════════════════════════════════════════════════
#         🏭 Bot Factory — ek function se dono
# ════════════════════════════════════════════════

def make_bot_handlers(bot_key: str, bot_label: str):
    """
    bot_key   = "bot1" ya "bot2"
    bot_label = display name jaise "🤖 Bot 1" ya "🤖 Bot 2"
    """

    # ── /start ──────────────────────────────────
    async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        uid = update.effective_user.id
        if not is_authorized(uid):
            await update.message.reply_text("👋 Yeh bot private use ke liye hai.")
            return
        settings = load_settings(bot_key)
        await update.message.reply_text(
            f"🛠️ <b>{bot_label} Admin Panel</b>\n\n"
            f"{'✅' if settings['auto_approve'] else '❌'} Auto Approve: <b>{'ON' if settings['auto_approve'] else 'OFF'}</b>\n"
            f"📨 Message Type: <b>{settings['message_type'].upper()}</b>\n"
            f"🔘 Inline Buttons: <b>{len(settings['inline_buttons'])}</b>\n\n"
            "Niche se setting choose karo 👇",
            reply_markup=main_menu_kb(settings),
            parse_mode=ParseMode.HTML
        )

    # ── Callback ─────────────────────────────────
    async def cb_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        uid   = query.from_user.id
        await query.answer()

        if not is_authorized(uid):
            await query.answer("❌ Access denied!", show_alert=True)
            return

        data     = query.data
        settings = load_settings(bot_key)

        async def refresh_main(text_override=None):
            t = text_override or (
                f"🛠️ <b>{bot_label} Admin Panel</b>\n\n"
                f"{'✅' if settings['auto_approve'] else '❌'} Auto Approve: <b>{'ON' if settings['auto_approve'] else 'OFF'}</b>\n"
                f"📨 Message Type: <b>{settings['message_type'].upper()}</b>\n"
                f"🔘 Inline Buttons: <b>{len(settings['inline_buttons'])}</b>\n\n"
                "Niche se setting choose karo 👇"
            )
            await query.edit_message_text(t, reply_markup=main_menu_kb(load_settings(bot_key)),
                                          parse_mode=ParseMode.HTML)

        # Toggle auto approve
        if data == "toggle_approve":
            settings["auto_approve"] = not settings["auto_approve"]
            save_settings(bot_key, settings)
            await query.answer(f"Auto Approve: {'✅ ON' if settings['auto_approve'] else '❌ OFF'}", show_alert=True)
            await refresh_main()

        # Message type menu
        elif data == "set_message":
            await query.edit_message_text(
                "📨 <b>Message Type Choose Karo:</b>\n\n"
                "• <b>Text</b> — Sirf text\n"
                "• <b>Image + Text</b> — Photo + caption\n"
                "• <b>Video + Text</b> — Video + caption\n\n"
                "💡 HTML supported: <code>&lt;b&gt;bold&lt;/b&gt;</code>, "
                "<code>&lt;i&gt;italic&lt;/i&gt;</code>, "
                "<code>&lt;a href='url'&gt;link&lt;/a&gt;</code>",
                reply_markup=message_type_kb(), parse_mode=ParseMode.HTML
            )

        # Select type
        elif data.startswith("msg_type_"):
            msg_type = data.replace("msg_type_", "")
            settings["message_type"] = msg_type
            save_settings(bot_key, settings)
            context.user_data["awaiting"] = "text"
            hint = "\n\n📸 <i>Text ke baad media bhi maangega.</i>" if msg_type != "text" else ""
            await query.edit_message_text(
                f"✏️ <b>Ab apna message text bhejo:</b>{hint}\n\n"
                "💡 <code>{name}</code> likhne se user ka naam aa jaayega.",
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="set_message")]])
            )

        # Buttons manager
        elif data == "manage_buttons":
            await query.edit_message_text(
                f"🔘 <b>Inline Buttons ({len(settings['inline_buttons'])})</b>\n\n"
                "Buttons add ya remove karo 👇",
                reply_markup=buttons_manager_kb(settings), parse_mode=ParseMode.HTML
            )

        # Add button
        elif data == "add_button":
            context.user_data["awaiting"] = "button_text"
            await query.edit_message_text(
                "🔘 <b>Naya Button — Step 1/2</b>\n\n"
                "Button par kya <b>text</b> dikhna chahiye?\n"
                "Example: <code>Channel Join Karo</code>",
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="manage_buttons")]])
            )

        # Remove button
        elif data.startswith("remove_btn_"):
            idx = int(data.replace("remove_btn_", ""))
            removed = settings["inline_buttons"].pop(idx)
            save_settings(bot_key, settings)
            await query.answer(f"✅ '{removed['text']}' remove ho gaya!", show_alert=True)
            await query.edit_message_text(
                f"🔘 <b>Inline Buttons ({len(settings['inline_buttons'])})</b>\n\nButtons manage karo 👇",
                reply_markup=buttons_manager_kb(settings), parse_mode=ParseMode.HTML
            )

        # Preview
        elif data == "preview":
            await query.edit_message_text("👁️ <b>Preview aa raha hai...</b>", parse_mode=ParseMode.HTML)
            try:
                await send_bot_message(context.bot, query.message.chat_id, settings)
            except Exception as e:
                await context.bot.send_message(query.message.chat_id, f"⚠️ Preview error:\n{e}")
            await context.bot.send_message(
                query.message.chat_id,
                "👆 Yeh preview hai!\nPublish karne ke liye niche dabao.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🚀 Publish Karo", callback_data="publish")],
                    [InlineKeyboardButton("✏️ Edit Karo", callback_data="back_main")],
                ])
            )

        # Publish
        elif data == "publish":
            save_settings(bot_key, settings)
            await query.edit_message_text(
                f"✅ <b>{bot_label} — Published!</b>\n\n"
                "Ab har join request pe yeh message jaayega. ✔️",
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Main Menu", callback_data="back_main")]])
            )

        # Stats
        elif data == "stats":
            st = settings.get("stats", {"total": 0, "approved": 0})
            await query.edit_message_text(
                f"📊 <b>{bot_label} — Statistics</b>\n\n"
                f"📥 Total Requests: <b>{st['total']}</b>\n"
                f"✅ Approved: <b>{st['approved']}</b>\n"
                f"🤖 Auto Approve: <b>{'ON' if settings['auto_approve'] else 'OFF'}</b>",
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_main")]])
            )

        # Back
        elif data == "back_main":
            context.user_data.clear()
            await refresh_main()

    # ── Message Handler ──────────────────────────
    async def msg_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        uid = update.effective_user.id
        if not is_authorized(uid):
            return

        awaiting = context.user_data.get("awaiting")
        settings = load_settings(bot_key)

        if awaiting == "text":
            text = update.message.text or update.message.caption or ""
            settings["message_text"] = text
            save_settings(bot_key, settings)
            context.user_data["awaiting"] = None

            if settings["message_type"] in ("photo", "video"):
                context.user_data["awaiting"] = "media"
                word = "Photo" if settings["message_type"] == "photo" else "Video"
                await update.message.reply_text(
                    f"✅ Text save!\n\nStep 2: Ab apna <b>{word}</b> bhejo 📤",
                    parse_mode=ParseMode.HTML
                )
            else:
                await update.message.reply_text(
                    "✅ <b>Text save ho gaya!</b>", parse_mode=ParseMode.HTML,
                    reply_markup=after_save_kb()
                )

        elif awaiting == "media":
            file_id  = None
            msg_type = settings["message_type"]
            if update.message.photo and msg_type == "photo":
                file_id = update.message.photo[-1].file_id
            elif update.message.video and msg_type == "video":
                file_id = update.message.video.file_id

            if file_id:
                settings["media_file_id"] = file_id
                save_settings(bot_key, settings)
                context.user_data["awaiting"] = None
                await update.message.reply_text(
                    "✅ <b>Media save ho gayi!</b>", parse_mode=ParseMode.HTML,
                    reply_markup=after_save_kb()
                )
            else:
                word = "Photo" if msg_type == "photo" else "Video"
                await update.message.reply_text(f"⚠️ Sahi type bhejo — <b>{word}</b> chahiye!",
                                                parse_mode=ParseMode.HTML)

        elif awaiting == "button_text":
            context.user_data["new_btn_text"] = update.message.text
            context.user_data["awaiting"] = "button_url"
            await update.message.reply_text(
                f"✅ Text: <b>{update.message.text}</b>\n\n"
                "Step 2/2: Ab <b>URL</b> bhejo:\n<code>https://t.me/yourchannel</code>",
                parse_mode=ParseMode.HTML
            )

        elif awaiting == "button_url":
            url = update.message.text.strip()
            if not url.startswith("http"):
                await update.message.reply_text("⚠️ URL <code>https://</code> se start hona chahiye!",
                                                parse_mode=ParseMode.HTML)
                return
            btn_text = context.user_data.pop("new_btn_text", "Button")
            context.user_data["awaiting"] = None
            settings["inline_buttons"].append({"text": btn_text, "url": url})
            save_settings(bot_key, settings)
            await update.message.reply_text(
                f"✅ <b>Button add ho gaya!</b>\n"
                f"Label: <b>{btn_text}</b>\n"
                f"URL: <code>{url}</code>\n\n"
                f"Total Buttons: <b>{len(settings['inline_buttons'])}</b>",
                parse_mode=ParseMode.HTML,
                reply_markup=after_button_kb()
            )

    # ── Join Request Handler ─────────────────────
    async def join_req_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        jr       = update.chat_join_request
        user_id  = jr.from_user.id
        user_name = jr.from_user.first_name
        settings = load_settings(bot_key)

        # Stats
        st = settings.get("stats", {"total": 0, "approved": 0})
        st["total"] += 1

        try:
            await send_bot_message(context.bot, user_id, settings, user_name)
            logger.info(f"[{bot_label}] ✅ DM sent → {user_name} ({user_id})")
        except Exception as e:
            logger.error(f"[{bot_label}] ❌ DM failed → {user_id}: {e}")

        if settings.get("auto_approve", True):
            try:
                await jr.approve()
                st["approved"] += 1
                logger.info(f"[{bot_label}] ✅ Approved → {user_name}")
            except Exception as e:
                logger.error(f"[{bot_label}] ❌ Approve failed: {e}")

        settings["stats"] = st
        save_settings(bot_key, settings)

    return start_cmd, cb_handler, msg_handler, join_req_handler


# ════════════════════════════════════════════════
#         🔧 Build Application
# ════════════════════════════════════════════════

def build_app(token: str, bot_key: str, bot_label: str) -> Application:
    start_cmd, cb_handler, msg_handler, join_req_handler = make_bot_handlers(bot_key, bot_label)

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CallbackQueryHandler(cb_handler))
    app.add_handler(ChatJoinRequestHandler(join_req_handler))
    app.add_handler(MessageHandler(
        filters.TEXT | filters.PHOTO | filters.VIDEO,
        msg_handler
    ))
    return app


# ════════════════════════════════════════════════
#         🚀 Run Both Bots Simultaneously
# ════════════════════════════════════════════════

def run_bot_in_thread(token: str, bot_key: str, bot_label: str):
    """Har bot apne alag thread + event loop mein chalta hai"""
    import asyncio

    async def runner():
        app = build_app(token, bot_key, bot_label)
        print(f"✅ {bot_label} chal raha hai...")
        async with app:
            await app.initialize()
            await app.start()
            await app.updater.start_polling(drop_pending_updates=True)
            # Infinite loop — jab tak program band na ho
            await asyncio.Event().wait()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(runner())


def main():
    print("=" * 55)
    print("  DUAL JOIN REQUEST BOT — Starting...")
    print(f"  Owner ID : {OWNER_ID}")
    print(f"  Admin IDs: {ADMIN_IDS}")
    print("=" * 55)

    # Bot 1 thread
    t1 = threading.Thread(
        target=run_bot_in_thread,
        args=(BOT_1_TOKEN, "bot1", "🤖 Bot 1"),
        daemon=True,
        name="Bot-1"
    )

    # Bot 2 thread
    t2 = threading.Thread(
        target=run_bot_in_thread,
        args=(BOT_2_TOKEN, "bot2", "🤖 Bot 2"),
        daemon=True,
        name="Bot-2"
    )

    t1.start()
    t2.start()

    print("✅ Dono bots chal rahe hain! Ctrl+C se band karo.\n")

    try:
        t1.join()
        t2.join()
    except KeyboardInterrupt:
        print("\n🛑 Bots band ho rahe hain...")


if __name__ == "__main__":
    main()
