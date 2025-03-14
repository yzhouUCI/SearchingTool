from telegram import Bot
import asyncio
import time, datetime
import re
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

    def sendgraph(self, graphmaker, task_configs, task_results):
        html = graphmaker.result2html(task_configs, task_results)
        page = graphmaker.makepage(html)
        self.send_message(page['url'])

from telegraph import Telegraph

class telegraphmaker():
    def __init__(self, access_token, author_name):
        self.telegraph = Telegraph(access_token=access_token)
        self.access_token = access_token
        self.author_name = author_name

    def makepage(self, content):
        title = datetime.datetime.now().strftime('%Y-%m-%d %H:%M') + " Searching results"
        page = self.telegraph.create_page(
            title=title,
            author_name=self.author_name,
            html_content=content,
            return_content=True
        )
        return page

    def result2html(self, task_configs, task_results):
        html = ""
        for idx, task in enumerate(task_configs):
            html += f"<h3>Task {idx+1}</h3>\n"
            task_description = task.get('task_description', '')
            html += f"<p><strong>Description:</strong> {task_description}</p>\n"
            results = task_results[idx]
            for idx_res, res in enumerate(results, start=1):
                ai_summary = res.get("summary", "")
                entry = res.get("paper_info", "")
                html += f'<h3 style="color:red">{entry.get("title", "No title")}</h3>\n'
                html += f"<p><strong>Publisher:</strong> {entry.get("publisher", "Unknown pubulisher")}</p>\n"
                pubdate = entry.get("date", "None")
                html += f"<p><strong>Published date:</strong> {pubdate}</p>\n"
                doi = entry.get("doi", "No doi")
                html += f"<p><strong>doi</strong>: <a href='http://dx.doi.org/{doi}' target='_blank'>{doi}</a></p>\n"
                html += f"<p><strong>Summary:</strong> {ai_summary}</p>\n"
                html += "<hr>\n"
            html += "<hr>\n"
        html = re.sub(r'<sup[^>]*>', '', html)
        html = re.sub(r'</sup>', '', html)
        return html
    
def createTelegraphAccount(author_name):
    telegraph = Telegraph()
    account = telegraph.create_account(short_name="Maybeclever", author_name=author_name)
    access_token = account["access_token"]
    return access_token
