from ddgs import DDGS

def get_linkedin_url(name):
    query = f"{name} site:linkedin.com/in/"
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=5))
        if results:
            for r in results:
                link = r.get("href") or r.get("link") or r.get("url")
                if link and "linkedin.com/in/" in link:
                    return {"name": name, "linkedin_url": link}
        return {"name": name, "linkedin_url": "Not found"}

# Test with multiple names
names = ["Shri Krishna Pandey", "Pratham Bhalla", "Sundar Pichai", "Elon Musk"]
for name in names:
    print(get_linkedin_url(name))
