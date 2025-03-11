from telegram import Bot
import asyncio

class telebot():
    def __init__(self, bot_token, chat_id):
        self.chat_id = chat_id
        self.bot = Bot(token=bot_token)
    async def _send_message_async(self, message):
        max_length = 4096
        lines = message.splitlines()
        current_chunk = ""
        for line in lines:
            if len(line) > max_length:
                if current_chunk:
                    await self.bot.send_message(chat_id=self.chat_id, text=current_chunk)
                    current_chunk = ""
                for i in range(0, len(line), max_length):
                    part = line[i:i+max_length]
                    await self.bot.send_message(chat_id=self.chat_id, text=part)
                continue
            if current_chunk:
                if len(current_chunk) + 1 + len(line) > max_length:
                    await self.bot.send_message(chat_id=self.chat_id, text=current_chunk)
                    current_chunk = line
                else:
                    current_chunk += "\n" + line
            else:
                current_chunk = line

        if current_chunk:
            await self.bot.send_message(chat_id=self.chat_id, text=current_chunk)
    def send_message(self, message):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            loop.create_task(self._send_message_async(message))
        else:
            asyncio.run(self._send_message_async(message))