from .agent import agent
from .elsevier import elsevier
import os
import datetime
import re
from tqdm import tqdm

def run_task(task_config):
    if task_config["agent_type"] == "basic":
        # test api
        if not elsevier.test_API(task_config["elsevier_api"]):
            ValueError("Cannot connect to Elsevier. Please check your api key and network connection.")
        # model set
        agent_model = agent.SearchingAgent(task_config["model_config"]["model_name"])
        prompt = task_config["model_config"]["model_prompt"]
        agent_model.messages.append(
                    {
                    'role' : 'user',
                    'content': f"Current date is {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}. You are my academic research assistant. My requirement is: [{prompt}]. I will provide you with the title and abstract of an academic paper. Your task is to review the paper and determine if it meets my requirements. It is crucial that your response is in the exact format shown below, with the two parts separated by a semicolon (;): 'summary: [your concise summary of the paper]; required: [Y if it meets the requirements, N if it does not]'. Make sure to follow this format exactly and do not include any additional commentary.",
                }
        )
        pattern = r"^summary:\s*(.+?)\s*;\s*required:\s*(Y|N)$"
        search_engine = elsevier.Elsevier(api_key=task_config["elsevier_api"])
        # load searching config
        pwd = task_config["pwd"]
        # authors
        try:
            author_list_path = os.path.join(pwd,"task",task_config["search_config"]["author_list_file"])
            with open(author_list_path, 'r', encoding='utf-8') as file:
                authors = [line.strip() for line in file if line.strip()]
        except:
            authors = None
        # publisher
        try:
            pub_list_path = os.path.join(pwd,"task",task_config["search_config"]["publisher_file"])
            with open(pub_list_path, 'r', encoding='utf-8') as file:
                publishers = [line.strip() for line in file if line.strip()]
        except:
            publishers = None
        # keywords
        try:
            keywords_file_path = os.path.join(pwd,"task",task_config["search_config"]["keywords_file"])
            with open(keywords_file_path, 'r', encoding='utf-8') as file:
                keywords = [line.strip() for line in file if line.strip()]
        except:
            keywords = None
        # year
        if not task_config["search_config"]["year"]:
            year = datetime.datetime.now().year - 1
        else:
            year = task_config["search_config"]["year"]
        # max_count
        if not task_config["search_config"]["max_count"]:
            max_count = 100
        else:
            max_count = task_config["search_config"]["max_count"]
        # max_output
        if not task_config["model_config"]["output_count"]:
            max_output_count = 10
        else:
            max_output_count = task_config["model_config"]["output_count"]
        # searching 
        query = elsevier.generate_query(keywords=keywords,
                                        author_id=authors,
                                        issn=publishers,
                                        minyear=year
                                        )
        results = search_engine.get_all_search_results(query=query,max_count=max_count)
        print(f"Found {len(results)} articles.")
        formatted_res = agent.structured_search_results(results)
        filtered_papers = []
        for idx, res in enumerate(tqdm(formatted_res, desc="Processing"),start=1):
            i = 1
            while True:
                response = agent_model.chat(res)
                match = re.match(pattern, response)
                if match:
                    summary = match.group(1)
                    required = match.group(2)
                    if required == 'Y':
                        filtered_papers.append({"summary":summary,"paper_info": results[idx-1]})
                    break
                if i > 3:
                    break
                i = i + 1
            if len(filtered_papers) >= max_output_count:
                break
        print(f"Filtered {len(filtered_papers)} articles.")
        return filtered_papers
            