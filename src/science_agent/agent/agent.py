from ollama import chat
from ollama import ChatResponse
from ollama import Client
class BasicAgent():
    def __init__(self, model):
        self.model = model
        self.client = Client(host='http://localhost:11434', headers={'x-some-header':'some-value'})
        self.messages = []
    def chat(self, content):
        self.messages.append(
            {
                'role' : 'user',
                'content': content,
            }
        )
        response = self.client.chat(model=self.model, messages=self.messages)
        self.messages.append({
            'role' : response['message']['role'],
            'content' : response['message']['content']
        }
        )
        return response['message']['content']

class TranslationAgent(BasicAgent):
    def __init__(self, model):
        super(TranslationAgent, self).__init__(model)
        self.messages.append(
            {
                'role' : 'user',
                'content': "Please translate the following contents into Chinese.",
            }
        )

class SearchingAgent(BasicAgent):
    def chat(self, content):
        self.messages.append(
            {
                'role' : 'user',
                'content': content,
            }
        )
        response = self.client.chat(model=self.model, messages=self.messages)
        self.messages.pop()
        return response['message']['content']
    
def structured_search_results(entries):
    formatted_entries = []
    for idx, entry in enumerate(entries, start=1):
        title = entry.get("title", "No title")
        abstract = entry.get("abstract", "No abstract")
        publisher = entry.get("publiher", "Unknown pubulisher")
        pubdate = entry.get("date", "Unknown date")
        doi = entry.get("doi", "No doi")
        entry_text = f"Paper {idx}:\nTitle: {title}\nAbstract: {abstract}\nPublisher: {publisher}\nPubilished date: {pubdate}\ndoi: {doi}"
        formatted_entries.append(entry_text)
    return formatted_entries
