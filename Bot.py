import logging
import random
import json
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = "8506256564:AAHvVu1CYdtwnsdVcF
5rypl6NnkLOFZZTdY"
DATA_FILE = "members.json"  # Lưu danh sách thành viên

# ===== KHO LỜI CHÀO KHÁC NHAU =====
GREETINGS = [
    "☀️ Chào {name}, chúc bạn ngày mới tràn đầy năng lượng!",
    "🌅 {name} ơi, dậy chưa? Chúc một ngày tuyệt vời nhé!",
    "🍀 Chào buổi sáng {name}, hôm nay sẽ là ngày may mắn của bạn!",
    "💪 {name}, cố lên nhé! Ngày mới thành công rực rỡ!",
    "🌸 Chào {name}, chúc bạn buổi sáng vui vẻ và hạnh phúc!",
    "🌟 {name} thân mến, chúc ngày mới an lành và nhiều niềm vui!",
    "🔥 {name} ơi! Sáng rồi, bắt đầu ngày mới thôi nào!",
    "🌻 Chào buổi sáng {name}, chúc bạn luôn tươi cười như hoa hướng dương!",
    "🍵 {name}, một ngày mới bắt đầu rồi, uống ly cà phê rồi chiến đấu nhé!",
    "🎉 Chào {name}, chúc bạn hôm nay gặp nhiều điều tốt lành!",
    "😊 {name} ơi, sáng tốt lành! Bạn đã sẵn sàng chưa?",
    "✨ Chào {name}, chúc bạn một ngày mới ngập tràn yêu thương!",
    "🚀 {name}, khởi động ngày mới đầy nhiệt huyết nhé!",
    "🌞 Chào {name}, chúc bạn có ngày làm việc hiệu quả!",
    "🎁 {name} ơi, hôm nay sẽ có điều bất ngờ dành cho bạn đó!",
    "🌈 Chào {name}, chúc ngày mới nhiều màu sắc tươi vui!",
    "🍀 {name}, hôm nay mọi chuyện sẽ suôn sẻ với bạn!",
    "💖 Chào buổi sáng {name}, chúc bạn hạnh phúc cả ngày!",
    "⭐ {name} thân yêu, ngày mới vui vẻ nhé!",
    "🌼 Chào {name}, chúc bạn một ngày tươi đẹp như bông hoa!",
]

# ===== QUẢN LÝ DỮ LIỆU =====
def load_members() -> dict:
    """Load danh sách thành viên đã đăng ký"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_members(members: dict):
    """Lưu danh sách thành viên"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(members, f, ensure_ascii=False, indent=2)

# ===== COMMAND HANDLERS =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Chào bạn!\n\n"
        "📌 **Các lệnh:**\n"
        "/register - Đăng ký nhận chào buổi sáng\n"
        "/unregister - Hủy đăng ký\n"
        "/morning - Chào buổi sáng tất cả thành viên đã đăng ký\n"
        "/list - Xem danh sách đã đăng ký",
        parse_mode="Markdown"
    )

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Đăng ký nhận chào buổi sáng"""
    user = update.effective_user
    chat = update.effective_chat
    
    members = load_members()
    chat_key = str(chat.id)
    
    if chat_key not in members:
        members[chat_key] = {}
    
    # Lưu user_id và tên
    members[chat_key][str(user.id)] = user.full_name
    save_members(members)
    
    await update.message.reply_text(
        f"✅ Đã đăng ký **{user.full_name}**!\n"
        f"🆔 ID: `{user.id}`\n"
        f"Bạn sẽ được chào mỗi sáng nhé! 🌅",
        parse_mode="Markdown"
    )

async def unregister(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Hủy đăng ký"""
    user = update.effective_user
    chat = update.effective_chat
    members = load_members()
    chat_key = str(chat.id)
    
    if chat_key in members and str(user.id) in members[chat_key]:
        del members[chat_key][str(user.id)]
        save_members(members)
        await update.message.reply_text(f"🛑 Đã hủy đăng ký cho **{user.full_name}**!", parse_mode="Markdown")
    else:
        await update.message.reply_text("ℹ️ Bạn chưa đăng ký.")

async def list_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xem danh sách thành viên đã đăng ký"""
    chat = update.effective_chat
    members = load_members()
    chat_key = str(chat.id)
    
    if chat_key not in members or not members[chat_key]:
        await update.message.reply_text("📭 Chưa có ai đăng ký.")
        return
    
    text = "📋 **Danh sách thành viên đã đăng ký:**\n\n"
    for uid, name in members[chat_key].items():
        text += f"• {name} — `{uid}`\n"
    
    await update.message.reply_text(text, parse_mode="Markdown")

async def morning(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Chào buổi sáng từng người một, mỗi người một câu khác nhau"""
    chat = update.effective_chat
    
    if chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("⚠️ Lệnh này chỉ dùng trong group!")
        return
    
    members = load_members()
    chat_key = str(chat.id)
    
    if chat_key not in members or not members[chat_key]:
        await update.message.reply_text(
            "📭 Chưa có ai đăng ký!\n"
            "Mọi người gõ /register để đăng ký nhận chào buổi sáng nhé!"
        )
        return
    
    # Lấy danh sách lời chào ngẫu nhiên (không trùng)
    member_list = list(members[chat_key].items())
    greetings_pool = GREETINGS.copy()
    random.shuffle(greetings_pool)
    
    # Gửi tin nhắn mở đầu
    await update.message.reply_text("🌅 **CHÀO BUỔI SÁNG CẢ NHÀ!** ☀️", parse_mode="Markdown")
    
    # Chào từng người, mỗi người 1 câu khác nhau
    for i, (uid, name) in enumerate(member_list):
        # Chọn lời chào (nếu hết thì random lại)
        if i < len(greetings_pool):
            greeting = greetings_pool[i]
        else:
            greeting = random.choice(GREETINGS)
        
        # Format: chèn tên + tag ID
        # Dùng HTML để tag: <a href="tg://user?id=UID">Tên</a>
        text = greeting.format(name=f'<a href="tg://user?id={uid}">{name}</a>')
        
        await context.bot.send_message(
            chat_id=chat.id,
            text=text,
            parse_mode="HTML"
        )

async def auto_morning(context: ContextTypes.DEFAULT_TYPE):
    """Tự động chào buổi sáng (job_queue)"""
    job = context.job
    chat_id = job.chat_id
    members = load_members()
    chat_key = str(chat_id)
    
    if chat_key not in members or not members[chat_key]:
        return
    
    member_list = list(members[chat_key].items())
    greetings_pool = GREETINGS.copy()
    random.shuffle(greetings_pool)
    
    await context.bot.send_message(
        chat_id=chat_id,
        text="🌅 **CHÀO BUỔI SÁNG CẢ NHÀ!** ☀️",
        parse_mode="Markdown"
    )
    
    for i, (uid, name) in enumerate(member_list):
        if i < len(greetings_pool):
            greeting = greetings_pool[i]
        else:
            greeting = random.choice(GREETINGS)
        
        text = greeting.format(name=f'<a href="tg://user?id={uid}">{name}</a>')
        await context.bot.send_message(chat_id=chat_id, text=text, parse_mode="HTML")

async def set_auto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Đặt lịch tự động chào buổi sáng 6:00 sáng VN"""
    chat = update.effective_chat
    
    if chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("⚠️ Lệnh này chỉ dùng trong group!")
        return
    
    # Xóa job cũ
    jobs = context.job_queue.get_jobs_by_name(f"morning_{chat.id}")
    for job in jobs:
        job.schedule_removal()
    
    import datetime
    # 6:00 sáng VN (UTC+7) = 23:00 UTC
    t = datetime.time(hour=23, minute=0)
    
    context.job_queue.run_daily(
        auto_morning,
        time=t,
        chat_id=chat.id,
        name=f"morning_{chat.id}"
    )
    
    await update.message.reply_text("✅ Đã đặt lịch tự động chào buổi sáng lúc **6:00 sáng** hàng ngày!", parse_mode="Markdown")

async def stop_auto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    jobs = context.job_queue.get_jobs_by_name(f"morning_{chat.id}")
    
    if jobs:
        for job in jobs:
            job.schedule_removal()
        await update.message.reply_text("🛑 Đã tắt tự động chào buổi sáng.")
    else:
        await update.message.reply_text("ℹ️ Chưa có lịch tự động nào.")

# ===== MAIN =====
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("register", register))
    app.add_handler(CommandHandler("unregister", unregister))
    app.add_handler(CommandHandler("list", list_members))
    app.add_handler(CommandHandler("morning", morning))
    app.add_handler(CommandHandler("set_auto", set_auto))
    app.add_handler(CommandHandler("stop_auto", stop_auto))
    
    print("🤖 Bot đang chạy...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
