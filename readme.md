# Science Agent
## Main
1. Search articles based on Elsevier's database
2. LLM-based filtering
3. Email results periodically
4. Chinese support

## Requirements
1. Environment  
```shell
pip install ollama
pip install requests
pip install pyyaml
pip install python-telegram-bot
```
2. Get Elsevier APIs key  
https://dev.elsevier.com/apikey/manage

3. Pull a LLM using ollama  
https://ollama.com/

4. (optional) Telegram support  
You can use BotFather to create a bot and have a bot token. You can use third-party services like @userinfobot in Telegram to get your chat id.

5. (abandoned) Email support  

6. Edit 'config.yaml'.  
repeat_time是搜索间隔时间。其他的按自己的信息填写。
7. Edit task1.yaml. Support multiple searching tasks.  
在author_list中需要填写作者的id，可以在 https://www.scopus.com/search/form.uri?display=basic&zone=header&origin=searchbasic#author 里面查询。publisher是期刊的ISSN号。文件中换行分隔。有多种不同搜索需求的，可以添加多个task.yaml文件。
