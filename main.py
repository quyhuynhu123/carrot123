import discord
import asyncio
import os

# KHÔNG CÓ INTENTS (hoặc ALL)! Điều này rất quan trọng cho self-bots.
client = discord.Client()

# Định dạng cấu hình
CONFIG = {
    "TOKEN": os.environ.get("DISCORD_BOT_TOKEN"),  # Lấy token từ biến môi trường (khuyến nghị)
    "MESSAGES": [
        {
            "channel_id": 123456789012345678,  # Thay bằng ID kênh thực
            "content": "📢 Nội dung 1 - gửi đến channel 1",
            "delay": 5 # Delay giữa các tin nhắn (tùy chọn)
        },
        {
            "channel_id": 876543210987654321,  # Thay bằng ID kênh thực
            "content": "📢 Nội dung 2 - gửi đến channel 2",
            "delay": 10 # Delay giữa các tin nhắn (tùy chọn)
        },
        # Thêm các tin nhắn khác vào đây
    ]
}

@client.event
async def on_ready():
    print(f"Self-bot đã đăng nhập với tên: {client.user.name}")

    # Kiểm tra xem token có hợp lệ không
    if not CONFIG["TOKEN"]:
        print("Lỗi: Chưa thiết lập biến môi trường DISCORD_BOT_TOKEN")
        return

    # Duyệt qua danh sách tin nhắn
    for message_config in CONFIG["MESSAGES"]:
        channel_id = message_config.get("channel_id") #Sử dụng .get() để tránh lỗi KeyError nếu channel_id bị thiếu
        content = message_config.get("content") #Sử dụng .get() để tránh lỗi KeyError nếu content bị thiếu
        delay = message_config.get("delay", 0) # Lấy delay từ cấu hình, mặc định là 0 nếu không có

        if not channel_id or not content:
            print("Lỗi: channel_id hoặc content bị thiếu trong cấu hình tin nhắn.")
            continue  # Chuyển sang tin nhắn tiếp theo

        channel = client.get_channel(int(channel_id))  # Chuyển đổi channel_id thành số nguyên
        if channel:
            await asyncio.sleep(delay) # Chờ đợi trước khi gửi (nếu có delay)
            try:
                await channel.send(content)
                print(f"Đã gửi: {content} đến channel {channel_id}")
            except discord.errors.Forbidden:
                print(f"Không có quyền gửi tin nhắn đến channel {channel_id}")
            except Exception as e:
                print(f"Lỗi khi gửi tin nhắn đến channel {channel_id}: {e}")
        else:
            print(f"Không tìm thấy channel với ID {channel_id}")

    print("Đã gửi tất cả tin nhắn.")
    await client.close()  # Đóng client sau khi gửi tất cả tin nhắn

# Khởi động bot
client.run(CONFIG["TOKEN"])
