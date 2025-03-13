# Maybeclever Paper Filter
## Main
1. All papers come from Elsevier's database, NO FAKE PAPERS AND NO FAKE REFERENCES.
2. LLMs help filter the collected papers.
3. Searching and filtering results will be sent to your Telegram.
4. Work 7/24. Best worker never stops. LoL

## How to use
1. Installation  
    ```uv``` is used here to manage the project. On macOS, it is recommended to use brew for installation.  
    ```shell
    brew install uv
    ```
    Next, install the required Python packages.  
    ```shell
    uv add pyyaml requests ollama # basic requirement
    uv add python-telegram-bot telegraph # Telegram support
    ```

2. Get your Elsevier API  
    https://dev.elsevier.com/apikey/manage  
    Sign in and create an **API key**.  

3. Install Ollama and pull a LLM  
    https://ollama.com/  
    Run ```ollama list``` in your terminal to make sure the **full name** of the large language model.

4. Telegram support   
    BotFather is a very useful tool to create your own chat bot. Using Python to send message in Telegram requires **the bot token** and **Your id**. If you do not konw your id, you can send '/start' to @userinfobot to get it.  

    To improve readability, Telegraph is applied. When running the program for the first time, it will automatically generate a Telegraph API token. Please add it to the ```config.yaml``` file.  

5. Edit your ```config.yaml```.

6. Add searching tasks  
    Each YAML file in the task directory represents a task. Choosing a proper LLM, write a prompt for the LLM and edit your searching options.  

    **Notice**: ```author_list``` needs authors' id in the database. ```publisher_list``` needs ISSN.

7. Let it work
    ```shell
    uv run run.py
    ```
## Examples
1. Focusing on some group, just put their id in the list.
2. You want to know the front of a field from your interested journals? Add all ISSNs in the list and tell AI to find the latest papers.

## Next
1. Local database
2. More flexible searching options
3. RSS support
4. Richer formatted contents and Telegra.ph

## Links
1. https://dev.elsevier.com/apikey/manage
2. https://dev.elsevier.com/tecdoc_search_request.html
3. https://telegra.ph/api
4. https://docs.anythingllm.com/introduction
