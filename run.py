#%%
import os
import yaml
import time, datetime
from src.science_agent.sciagent import run_task
from src.science_agent.email import emailbox
from src.science_agent.teleg import telebot
def get_all_filenames(folder_path):
    filenames = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return filenames

config_file_path = "./config.yaml"
with open(config_file_path, "r", encoding="utf-8") as file:
    config_ = yaml.safe_load(file)

repeat_time = config_["system_config"]["repeat_time"]
if repeat_time == 0:
    repeat = False
else:
    repeat = True

# email config
email_smtp_server = config_['email_config']["smtp_server"]
email_smtp_port = config_['email_config']["smtp_port"]
email_sender = config_['email_config']["sender"]
email_password = config_['email_config']["password"]
email_receiver = config_['email_config']["receiver"]
if not (email_smtp_server or email_smtp_port or email_sender or email_sender or email_password or email_receiver):
    print("Email deactivated.")
    emailbox_ = None
else:
    print("Email activated.")
    emailbox_ = emailbox(email_smtp_server,email_smtp_port,email_sender,email_password)

# telegram config
telegram_bot_token = config_["telegram_config"]["bot_token"]
telegram_bot_chatid = config_["telegram_config"]["chat_id"]
if not (telegram_bot_token or telegram_bot_chatid):
    print("Telegram deactivated.")
    telegram_ = None
else:
    print("Telegram activated.")
    telegram_ = telebot(telegram_bot_token, telegram_bot_chatid)
    
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
#print(f"Running searching task every {repeat_time} hours.")
last_start_time = datetime.datetime.now()

while True:
    next_scheduled_time = last_start_time + datetime.timedelta(hours=repeat_time)
    now = datetime.datetime.now()
    #print(f"Time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    res = []
    for idx, task in enumerate(task_config, start = 1):
        print(f"Task: {idx}")
        task.update({"elsevier_api":api_key})
        task.update({"pwd":os.path.dirname(os.path.abspath(__file__))})
        res.append(run_task(task))
    # send email
    body_content = []
    for idx, result in enumerate(res,start=1):
        body_content.append(f"Task {idx}")
        body_content.append(f"Task description: {task_config[idx-1]["task_description"]}")
        for idx_res, search_content in enumerate(result,start=1):
            body_content.append(f"{idx_res}. ")
            body_content.append(f"Agent summary: {search_content["agent summary"]}")
            body_content.append(search_content["paper info"])
    body = "\n".join(body_content)
    if emailbox_:
        emailbox_.send_email("Searching results from science agent",body,email_receiver)
    if telegram_:
        telegram_.send_message(body)
    print(body)
    print("Tasks completed.")
    print(f"Next Searching Time: {next_scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}")
    if now < next_scheduled_time:
        wait_seconds = (next_scheduled_time - now).total_seconds()
        time.sleep(wait_seconds)
    last_start_time = datetime.datetime.now()
    if not repeat:
        break
# %%
