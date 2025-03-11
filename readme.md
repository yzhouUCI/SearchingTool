# AI辅助文献检索
## 主要功能
1. 基于Elsevier的数据库进行检索
2. LLM辅助文献筛选
3. 可连接Telegram自动推送检索结果，包含AI锐评

## Requirements
1. 环境  
    建议使用conda创建虚拟环境
    ```shell
    pip install ollama
    pip install requests
    pip install pyyaml
    pip install python-telegram-bot
    ```

2. 获取Elsevier APIs key  
    https://dev.elsevier.com/apikey/manage  
    注册后免费获取。获取后填到config.yaml中。

3. 安装ollama及LLM  
    https://ollama.com/

4. (optional) Telegram 支持   
    通过BotFather创建bot并获取相应的token。通过在搜索栏搜索@userinfobot获得自己的id。将这两项填进config.yaml中。效果如图所示：
    ![Telegram](/assets/telegram.png "Telegram")
5. (abandoned) Email支持不了。 

6. 编辑task文件夹下的任务设置文件task1.yaml，文件名随便取，不要改后缀。有不同的检索要求，可以按需求增加任务文件配置文件。检索的条件由文本文件给出，配置文件中指定相应的文本文件名即可。  
    author_list里面需要填写作者的id，具体的id自行在scopus上查询。publisher用于指定期刊范围，需要ISSN号。每行只填写一项，在检索过程中，同类项是OR连接，不同类项是AND连接，表示检索结果必须要满足作者中至少一项，期刊中至少一项，关键词中至少一项等。留空表示无限制。由于数据库限制，时间范围的最小单位是年。根据需求自行选择LLM，注意模型name必须要写全称。提示词根据自己需求写。

7. 运行方式，控制台:
    ```shell
    python run.py
    ```
## Next
没下一步
