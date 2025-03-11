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
        title = entry.get("dc:title", "No title")
        abstract = entry.get("dc:description", "No description")
        publisher = entry.get("prism:publicationName", "Unknown pubulisher")
        pubdate = entry.get("prism:coverDate", "Unknown date")
        doi = entry.get("prism:doi", "No doi")
        entry_text = f"Paper {idx}:\nTitle: {title}\nAbstract: {abstract}\nPublisher: {publisher}\nPubilished date: {pubdate}\nDoi: {doi}"
        formatted_entries.append(entry_text)
    return formatted_entries

def structured_search_results_noabstract(entries):
    formatted_entries = []
    for idx, entry in enumerate(entries, start=1):
        title = entry.get("dc:title", "No title")
        publisher = entry.get("prism:publicationName", "Unknown pubulisher")
        pubdate = entry.get("prism:coverDate", "Unknown date")
        doi = entry.get("prism:doi", "No doi")
        entry_text = f"Title: {title}\nPublisher: {publisher}\nPubilished date: {pubdate}\nDoi: {doi}"
        formatted_entries.append(entry_text)
    return formatted_entries