import asyncio
import time
import re

from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    Message,
)
from pyrogram.errors import (
    FloodWait,
    UserDeactivated,
    UserIsBlocked,
    ChatAdminRequired,
)

from AniyaMusic import app
from AniyaMusic.misc import SUDOERS
from AniyaMusic.utils.database import (
    get_served_chats,
    get_served_users,
    delete_served_chat,
    delete_served_user,
)
from AniyaMusic.utils.theme import UI

IS_BROADCASTING = False


def extract_buttons(text):
    if not text:
        return "", []

    buttons = []

    matches = re.findall(r"\[(.+?)\s*\|\s*(https?://.+?)\]", text)

    for name, url in matches:
        buttons.append(
            [InlineKeyboardButton(name.strip(), url=url.strip())]
        )

    cleaned_text = re.sub(
        r"\[(.+?)\s*\|\s*(https?://.+?)\]",
        "",
        text,
    ).strip()

    return cleaned_text, buttons


def broadcast_keyboard(pin, preview, forward):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    f"📌 PIN {'✅' if pin else '❌'}",
                    callback_data=f"broadcast_pin_{int(pin)}_{int(preview)}_{int(forward)}",
                ),
                InlineKeyboardButton(
                    f"🌐 PREVIEW {'✅' if preview else '❌'}",
                    callback_data=f"broadcast_lprev_{int(pin)}_{int(preview)}_{int(forward)}",
                ),
            ],
            [
                InlineKeyboardButton(
                    f"⏩ FORWARD {'✅' if forward else '❌'}",
                    callback_data=f"broadcast_fwd_{int(pin)}_{int(preview)}_{int(forward)}",
                ),
                InlineKeyboardButton(
                    "👁 PREVIEW",
                    callback_data=f"broadcast_view_{int(pin)}_{int(preview)}_{int(forward)}",
                ),
            ],
            [
                InlineKeyboardButton(
                    "📢 START ALL",
                    callback_data=f"broadcast_run_all_{int(pin)}_{int(preview)}_{int(forward)}",
                )
            ],
            [
                InlineKeyboardButton(
                    "👤 USERS",
                    callback_data=f"broadcast_run_users_{int(pin)}_{int(preview)}_{int(forward)}",
                ),
                InlineKeyboardButton(
                    "👥 GROUPS",
                    callback_data=f"broadcast_run_groups_{int(pin)}_{int(preview)}_{int(forward)}",
                ),
            ],
            [
                InlineKeyboardButton(
                    "⛔ STOP",
                    callback_data="broadcast_stop",
                )
            ],
        ]
    )


@app.on_message(filters.command("broadcast") & SUDOERS)
async def broadcast_command(client: Client, message: Message):
    global IS_BROADCASTING

    if not message.reply_to_message and len(message.command) < 2:
        return await message.reply_text(
            UI.panel(
                "📡 BROADCAST TOOL",
                (
                    "<b>Reply to a message or type text.</b>\n\n"
                    "<b>Buttons:</b>\n"
                    "<code>[Button | https://example.com]</code>\n\n"
                    "<b>Example:</b>\n"
                    "<code>/broadcast Hello [Support | https://t.me/yourchannel]</code>"
                ),
            )
        )

    if IS_BROADCASTING:
        return await message.reply_text(
            UI.panel(
                "⚠️ BUSY",
                "<b>Broadcast already running.</b>",
            )
        )

    await message.reply_text(
        text=UI.panel(
            "📡 BROADCAST DASHBOARD",
            "<b>Configure your broadcast settings.</b>",
        ),
        reply_markup=broadcast_keyboard(
            pin=False,
            preview=True,
            forward=False,
        ),
        reply_to_message_id=message.id,
    )


@app.on_callback_query(filters.regex(r"^broadcast_"))
async def broadcast_callback(client: Client, query: CallbackQuery):
    global IS_BROADCASTING

    data = query.data.split("_")

    if len(data) < 2:
        return

    action = data[1]

    if action == "stop":
        IS_BROADCASTING = False
        return await query.message.delete()

    try:
        if action == "run":
            mode = data[2]
            pin_enabled = bool(int(data[3]))
            preview_enabled = bool(int(data[4]))
            forward_enabled = bool(int(data[5]))
        else:
            pin_enabled = bool(int(data[2]))
            preview_enabled = bool(int(data[3]))
            forward_enabled = bool(int(data[4]))

    except Exception:
        return await query.answer(
            "Invalid callback data.",
            show_alert=True,
        )

    if action in ["pin", "lprev", "fwd"]:

        if action == "pin":
            pin_enabled = not pin_enabled

        elif action == "lprev":
            preview_enabled = not preview_enabled

        elif action == "fwd":
            forward_enabled = not forward_enabled

        return await query.message.edit_reply_markup(
            broadcast_keyboard(
                pin_enabled,
                preview_enabled,
                forward_enabled,
            )
        )

    cmd_msg = query.message.reply_to_message

    if not cmd_msg:
        return await query.answer(
            "Broadcast source lost.",
            show_alert=True,
        )

    content_chat_id = cmd_msg.chat.id
    content_msg_id = None
    raw_text = ""

    msg_text = cmd_msg.text or cmd_msg.caption or ""

    if cmd_msg.reply_to_message:
        content_msg_id = cmd_msg.reply_to_message.id

        parts = msg_text.split(None, 1)

        if len(parts) > 1:
            raw_text = parts[1]

    else:
        parts = msg_text.split(None, 1)

        if len(parts) > 1:
            raw_text = parts[1]

    if not content_msg_id and not raw_text:
        return await query.answer(
            "No content found.",
            show_alert=True,
        )

    cleaned_text, buttons = extract_buttons(raw_text)

    reply_markup = (
        InlineKeyboardMarkup(buttons)
        if buttons
        else None
    )

    # ================= PREVIEW =================

    if action == "view":

        try:
            if forward_enabled and content_msg_id:

                await client.forward_messages(
                    chat_id=query.from_user.id,
                    from_chat_id=content_chat_id,
                    message_ids=content_msg_id,
                )

            elif content_msg_id:

                await client.copy_message(
                    chat_id=query.from_user.id,
                    from_chat_id=content_chat_id,
                    message_id=content_msg_id,
                    caption=cleaned_text or None,
                    reply_markup=reply_markup,
                )

            else:

                await client.send_message(
                    chat_id=query.from_user.id,
                    text=cleaned_text,
                    reply_markup=reply_markup,
                    disable_web_page_preview=not preview_enabled,
                )

            return await query.answer(
                "Preview sent.",
                show_alert=True,
            )

        except Exception as e:
            return await query.answer(
                str(e),
                show_alert=True,
            )

    # ================= RUN =================

    if action == "run":

        if IS_BROADCASTING:
            return await query.answer(
                "Broadcast already running.",
                show_alert=True,
            )

        targets = []

        if mode in ["users", "all"]:
            users = await get_served_users()
            targets.extend(
                [int(x["user_id"]) for x in users]
            )

        if mode in ["groups", "all"]:
            groups = await get_served_chats()
            targets.extend(
                [int(x["chat_id"]) for x in groups]
            )

        if not targets:
            return await query.answer(
                "No targets found.",
                show_alert=True,
            )

        IS_BROADCASTING = True

        sent = 0
        failed = 0
        cleaned = 0

        total = len(targets)

        start_time = time.time()

        await query.message.edit_text(
            UI.panel(
                "🚀 BROADCAST STARTED",
                (
                    f"<b>Total:</b> {total}\n"
                    f"<b>Mode:</b> {mode.upper()}\n"
                    f"<b>Forward:</b> {'Enabled' if forward_enabled else 'Disabled'}"
                ),
            )
        )

        for i, chat_id in enumerate(targets):

            if not IS_BROADCASTING:
                break

            try:

                sent_msg = None

                # FORWARD MODE
                if forward_enabled and content_msg_id:

                    sent_msg = await client.forward_messages(
                        chat_id=chat_id,
                        from_chat_id=content_chat_id,
                        message_ids=content_msg_id,
                    )

                # COPY MODE
                elif content_msg_id:

                    sent_msg = await client.copy_message(
                        chat_id=chat_id,
                        from_chat_id=content_chat_id,
                        message_id=content_msg_id,
                        caption=cleaned_text or None,
                        reply_markup=reply_markup,
                    )

                # TEXT MODE
                else:

                    sent_msg = await client.send_message(
                        chat_id=chat_id,
                        text=cleaned_text,
                        reply_markup=reply_markup,
                        disable_web_page_preview=not preview_enabled,
                    )

                if pin_enabled and sent_msg:
                    try:
                        await sent_msg.pin(
                            disable_notification=True
                        )
                    except:
                        pass

                sent += 1

            except FloodWait as e:

                await asyncio.sleep(e.value)

            except (UserDeactivated, UserIsBlocked):

                cleaned += 1

                try:
                    await delete_served_user(chat_id)
                except:
                    pass

            except ChatAdminRequired:

                cleaned += 1

                try:
                    await delete_served_chat(chat_id)
                except:
                    pass

            except Exception:
                failed += 1

            # Progress
            if i % 15 == 0 or i == total - 1:

                percent = int((i + 1) / total * 100)

                prog = int(percent / 10)

                bar = (
                    "■" * prog
                    + "□" * (10 - prog)
                )

                try:
                    await query.message.edit_text(
                        UI.panel(
                            "📡 BROADCASTING",
                            (
                                f"<code>{bar}</code> {percent}%\n\n"
                                f"✅ <b>Sent:</b> {sent}\n"
                                f"❌ <b>Failed:</b> {failed}\n"
                                f"🧹 <b>Cleaned:</b> {cleaned}"
                            ),
                        )
                    )
                except:
                    pass

            await asyncio.sleep(0.05)

        IS_BROADCASTING = False

        total_time = int(time.time() - start_time)

        report = (
            f"⏱ <b>Time:</b> {total_time}s\n"
            f"✅ <b>Sent:</b> {sent}\n"
            f"❌ <b>Failed:</b> {failed}\n"
            f"🧹 <b>Cleaned:</b> {cleaned}"
        )

        try:
            await query.message.edit_text(
                UI.panel(
                    "🏁 FINAL REPORT",
                    report,
                )
            )

        except:

            await client.send_message(
                query.from_user.id,
                UI.panel(
                    "🏁 FINAL REPORT",
                    report,
                ),
        )
