# config.py
from pathlib import Path

# ==================== 基本配置 ====================
# 你的机器人 Token（@BotFather 给的那串）
BOT_TOKEN: str = "8226949795:AAE8fTfPB6WUQQlj4gMokpBydAg6faJLAd0"

# 管理员的 Telegram 数字 ID（可以有多个，用列表）
# 用 @userinfobot 私聊一下就能看到自己的 ID
ADMIN_IDS: list[int] = [
    8220598557,   # ← 改成你的 ID
    # 987654321, # 如果有多个管理员，再取消这行注释并填上
]

# ==================== 路径配置 ====================
# 项目根目录（自动计算，无需改）
BASE_DIR = Path(__file__).resolve().parent

# 以后数据库、日志、缓存等都放这里
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# 数据库文件路径（后面会用到）
DB_PATH = DATA_DIR / "bot.db"

# ==================== 功能开关（以后加）===================
# 以后想临时关掉某个功能，直接改这里就行
ENABLE_SUBMISSION = True   # 投稿功能
ENABLE_COMPETE    = True   # 雌竞功能
ENABLE_SURVEY     = True   # 剧情问卷