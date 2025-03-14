#%%
import os
import yaml
import time, datetime
from src.science_agent.sciagent import run_task
from src.science_agent.email import emailbox
from src.science_agent.teleg import telebot
from src.science_agent.teleg import telegraphmaker, createTelegraphAccount
def get_all_filenames(folder_path):
    filenames = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return filenames

config_file_path = "./config.yaml"
with open(config_file_path, "r", encoding="utf-8") as file:
    config_ = yaml.safe_load(file)

time_interval = config_["system_config"]["time_interval"]
if time_interval == 0:
    repeat = False
else:
    repeat = True

# Telegram config
telegram_bot_token = config_["telegram_config"]["bot_token"]
telegram_bot_chatid = config_["telegram_config"]["chat_id"]
if not (telegram_bot_token or telegram_bot_chatid):
    print("Telegram deactivated.")
    telegram_ = None
    telegraph = None
else:
    print("Telegram activated.")
    telegram_ = telebot(telegram_bot_token, telegram_bot_chatid)
    telegram_graph_token = config_["telegram_config"]["graph_token"]
    telegram_graph_name = config_["telegram_config"]["graph_name"]
    if not telegram_graph_token:
        telegram_graph_token = createTelegraphAccount("Intelligence")
        telegram_graph_name = "Intelligence"
        print(f"Please add this token in your config file. Token:{telegram_graph_token}, name:{telegram_graph_name}")
    telegraph = telegraphmaker(telegram_graph_token, telegram_graph_name)

# Elsevier config
api_key = config_["elsevier_config"]["API_key"]
task_folder = "./task"
task_config = []
task_folder_filenames = get_all_filenames(task_folder)
for file_ in task_folder_filenames:
    if not file_.endswith(".yaml"):
        continue
    with open(f"{task_folder}/{file_}", "r", encoding="utf-8") as file:
        task_config.append(yaml.safe_load(file))
print(f"{len(task_config)} task config(s) loaded.")
last_start_time = datetime.datetime.now()
#%%
while True:
    next_scheduled_time = last_start_time + datetime.timedelta(hours=time_interval)
    now = datetime.datetime.now()
    res = []
    print(f"Tasks started.")
    for idx, task in enumerate(task_config, start = 1):
        task.update({"elsevier_api":api_key})
        task.update({"pwd":os.path.dirname(os.path.abspath(__file__))})
        res.append(run_task(task))
    if telegram_:
        telegram_.sendgraph(telegraph, task_config,res)
    print(f"Tasks finished, next time: {next_scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}")
    if not repeat:
        break
    if now < next_scheduled_time:
        wait_seconds = (next_scheduled_time - now).total_seconds()
        time.sleep(wait_seconds)
    last_start_time = datetime.datetime.now()
    if not repeat:
        break