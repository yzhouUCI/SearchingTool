#%%
import requests
import json
import subprocess
from datetime import datetime, timedelta

class Elsevier:
    def __init__(self,api_key):
        self.apikey = api_key
    def get_info_author(self, affiliation_id = None, author_id = None):
        if not (affiliation_id or author_id):
            return None
        url = "https://api.elsevier.com/content/search/author"
        # ref: https://dev.elsevier.com/documentation/AuthorSearchAPI.wadl
        query_parts = []
        if affiliation_id:
            query_parts.append(f"AF-ID({affiliation_id})")
        if author_id:
            query_parts.append(f"AU-ID({author_id})")
        query = " AND ".join(query_parts)
        params = {
            "query": query,
            "apiKey": self.apikey
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            #entries = data.get('search-results', {}).get('entry', [])
            return data
        else:
            print("Fail: ", response.status_code)
            return None
    def get_all_search_results(self, query, max_count=1000):
        url = "https://api.elsevier.com/content/search/scopus"
        cursor = "*"
        all_entries = []
        while True:
            params = {
                "query": query,
                "apiKey": self.apikey,
                "httpAccept": "application/json",
                "cursor": cursor,
                "view": "COMPLETE",
                "sort" : "coverDate"
            }
            response = requests.get(url, params=params)
            if response.status_code != 200:
                print("Fail: ", response.status_code)
                break
            data = response.json()
            entries = data.get("search-results", {}).get("entry", [])
            if entries:
                all_entries.extend(entries)
            else:
                break
            if len(all_entries) > max_count:
                break
            next_cursor = data.get("search-results", {}).get("cursor", {}).get("@next")
            cursor = next_cursor
        elsevier2agent_entry = []
        for i in range(len(all_entries)):
            if i >= max_count:
                break
            elsevier2agent_entry.append(
                {
                    "title" : all_entries[i].get("dc:title", "no title"),
                    "date" : all_entries[i].get("prism:coverDate", "no date"),
                    "doi" : all_entries[i].get("prism:doi", "no doi"),
                    "abstract" : all_entries[i].get("dc:description", "no abstract"),
                    "publisher" : all_entries[i].get("prism:publicationName", "no publisher")
                }
            )
        return elsevier2agent_entry
    
def generate_query(keywords, author_id = None, affiliation_id = None, affiliation = None, author_name = None, doctype = None, isbn = None, issn = None, minyear=None):
    query = []
    if not (keywords or author_id or affiliation_id or affiliation or author_name or doctype or isbn or issn or minyear):
        print("One keyword at least!")
        return None
    
    if keywords:
        if isinstance(keywords, list):
            key_ = " OR ".join(keywords)
            query.append(f"KEY({key_})")
        else:
            query.append(f"KEY({keywords})")

    if author_id:
        if isinstance(author_id, list):
            auid = " OR ".join(author_id)
            query.append(f"AU-ID({auid})")
        else:
            query.append(f"AU-ID({author_id})")
    
    if affiliation_id:
        if isinstance(affiliation_id, list):
            afid = " OR ".join(affiliation_id)
            query.append(f"AF-ID({afid})")
        else:
            query.append(f"AF-ID({affiliation_id})")
    
    if affiliation:
        if isinstance(affiliation, list):
            affi = " OR ".join(affiliation)
            query.append(f"AFFIL({affi})")
        else:
            query.append(f"AFFIL({affiliation})")

    if author_name:
        if isinstance(author_name, list):
            atna = " OR ".join(author_name)
            query.append(f"AUTHOR-NAME({atna})")
        else:
            query.append(f"AUTHOR-NAME({author_name})")
    
    if doctype:
        if isinstance(doctype, list):
            doct = " OR ".join(doctype)
            query.append(f"DOCTYPE({doct})")
        else:
            query.append(f"DOCTYPE({doctype})")
    
    if isbn:
        if isinstance(isbn, list):
            isbn_ = " OR ".join(isbn)
            query.append(f"ISBN({isbn_})")
        else:
            query.append(f"ISBN({isbn})")
    
    if issn:
        if isinstance(issn, list):
            issn_ = " OR ".join(issn)
            query.append(f"ISSN({issn_})")
        else:
            query.append(f"ISSN({issn})")

    if minyear:
        query.append(f"PUBYEAR > {minyear}")

    all_query = " AND ".join(query)
    return all_query

def test_API(api_key):
    url = "https://api.elsevier.com/content/search/author"
    params = {
            "query": "AU-ID(7005041797)",
            "apiKey": api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return True
    else:
        return False