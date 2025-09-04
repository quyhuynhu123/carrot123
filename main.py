import discord
import asyncio
import os  # Import thư viện 'os'

async def send_message(client, channel_id, message, delay):
    await asyncio.sleep(delay)
    channel = client.get_channel(channel_id)
    if channel:
        try:
            await channel.send(message)
            print(f"✅ Đã gửi tin nhắn tới channel {channel_id}: {message}")
        except discord.Forbidden:
            print(f"❌ Không có quyền gửi tin nhắn tới channel {channel_id}")
        except discord.HTTPException as e:
            print(f"❌ Lỗi khi gửi tin nhắn tới channel {channel_id}: {e}")
    else:
        print(f"❌ Không tìm thấy kênh với ID {channel_id}")

async def main():
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'Logged in as {client.user}')

        # Định nghĩa các channel và nội dung tương ứng
        content1_channels = [123456789012345678, 876543210987654321, 246801357924680135]  # Thay bằng ID thực
        content2_channels = [246801357924680135, 111111111111111111, 222222222222222222]  # Thay bằng ID thực

        content1 = "📢 Nội dung 1 - gửi đến channel 1,2,3"
        content2 = "📢 Nội dung 2 - gửi đến channel 3,4,5"

        delay = 5  # Delay giữa mỗi tin nhắn, tính bằng giây

        # Gửi nội dung 1 đến các channel chỉ định
        for i, channel_id in enumerate(content1_channels):
            await send_message(client, channel_id, content1, i * delay)

        # Gửi nội dung 2 đến các channel chỉ định
        for i, channel_id in enumerate(content2_channels):
            await send_message(client, channel_id, content2, (len(content1_channels) + i) * delay)

        # Đợi một chút trước khi đóng client
        total_messages = len(content1_channels) + len(content2_channels)
        await asyncio.sleep(total_messages * delay + 2)
        await client.close()

    # Lấy token từ biến môi trường
    TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
    if not TOKEN:
        print("Lỗi: Chưa thiết lập biến môi trường DISCORD_BOT_TOKEN")
        return

    await client.start(TOKEN)

if __name__ == "__main__":
    from keep_alive import keep_alive
    keep_alive()
    asyncio.run(main())

