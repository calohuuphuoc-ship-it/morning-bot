import os
import random
import requests

TOKEN = "8506256564:AAFKR3P_asc-p-03UdPy5gp59iYOn3ІMHE"
CHAT_ID = "6034352335"

MORNING_WISHES = [
    "☀️ Chào buổi sáng! Chúc bạn một ngày mới ngập tràn năng lượng, làm việc hiệu quả và gặp nhiều may mắn! 💪",
    "☕ Dậy thôi nào! Chúc bạn buổi sáng tốt lành, một tách cà phê ngon và một khởi đầu tuyệt vời cho ngày hôm nay! ✨",
    "🌸 Chúc bạn buổi sáng an lành! Mong rằng mọi điều tốt đẹp nhất sẽ đến với bạn trong ngày hôm nay. Have a nice day! 😊",
    "🌅 Chào buổi sáng! Hãy mỉm cười và đón nhận ngày mới với một tâm trạng thật tích cực nhé! 💖",
    "🍀 Chúc bạn một ngày mới thật suôn sẻ, mọi việc hanh thông và luôn giữ được nụ cười trên môi! Chào buổi sáng! 🌟"
]

def send_telegram_message():
    message = random.choice(MORNING_WISHES)
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("✅ Đã gửi lời chúc buổi sáng thành công!")
    else:
        print(f"❌ Gửi thất bại. Lỗi: {response.text}")

if __name__ == "__main__":
    send_telegram_message()
