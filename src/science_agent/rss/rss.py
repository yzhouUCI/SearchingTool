import feedparser

def rss_get_entry(rss_url):
    feed = feedparser.parse(rss_url)
    if feed.bozo:
        print("RSS parsing failed:", feed.bozo_exception)
        return []
    rss2agent_entry = []
    for i in range(len(feed.entries)):
        date = feed.entries[i].get("date", "N")
        if date == "N":
            date = feed.entries[i].get("dc:date", "no date")
        doi =  feed.entries[i].get("doi", "N")
        if doi == "N":
            doi =  feed.entries[i].get("prism_doi", "N")
        if doi == "N":
            doi =  feed.entries[i].get("prism:doi", "no doi")
        
        publisher = feed.entries[i].get("prism:publicationName", "N")
        if publisher == "N":
            publisher = feed.entries[i].get("prism_publicationname", "no publisher")
        rss2agent_entry.append(
            {
                "title" : feed.entries[i].get("title", "no title"),
                "date" : date,
                "doi" : doi,
                "abstract" : feed.entries[i].get("summary", "no abstract"),
                "publisher" : publisher
            }
        )
    return rss2agent_entry