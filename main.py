# main.py
import asyncio
import logging
from telegram import Update
from telegram import ChatMemberUpdated
from telegram.ext import Application, CommandHandler, ContextTypes, ChatMemberHandler

from config import BOT_TOKEN, ADMIN_IDS
from database.db import add_or_update_chat, mark_chat_left  # ← 新增这两行

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("机器人已就绪！\n数据库已连接，所有加群记录都会永久保存～")

# 自动检测加群/退群
async def track_my_chat_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_member: ChatMemberUpdated = update.my_chat_member
    chat = chat_member.chat

    # 被加入新群/频道
    if chat_member.new_chat_member.status in ["member", "administrator"]:
        if chat_member.old_chat_member.status in ["left", "kicked", None]:
            title = chat.title or "无标题频道"
            add_or_update_chat(chat.id, title, chat.type)   # ← 存进数据库

            msg = f"加入新地点\n标题：{title}\nID：{chat.id}\n类型：{chat.type}"
            print(msg)

            for admin_id in ADMIN_IDS:
                try:
                    await context.bot.send_message(chat_id=admin_id, text=msg)
                except Exception as e:
                    print(f"通知 {admin_id} 失败: {e}")

    # 被踢出或离开
    elif chat_member.old_chat_member.status in ["member", "administrator"] and \
         chat_member.new_chat_member.status in ["left", "kicked"]:
        mark_chat_left(chat.id)
        msg = f"被移出群组\n标题：{chat.title}\nID：{chat.id}"
        print(msg)
        for admin_id in ADMIN_IDS:
            try:
                await context.bot.send_message(chat_id=admin_id, text=msg)
            except:
                pass

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("处理更新时出错:", exc_info=context.error)

async def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(ChatMemberHandler(track_my_chat_member, ChatMemberHandler.MY_CHAT_MEMBER))
    app.add_error_handler(error_handler)

    print("机器人启动中... 数据库已准备好")
    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)

    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())