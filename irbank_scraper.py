import requests
from bs4 import BeautifulSoup

def scrape_irbank(code):
    url = f"https://irbank.net/{code}/financial"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        return {"error": f"Failed to fetch: {e}"}

    soup = BeautifulSoup(response.text, "html.parser")
    data = {}

    try:
        for row in soup.select("table tr"):
            th = row.find("th")
            tds = row.find_all("td")
            if th and tds:
                label = th.text.strip()
                values = [td.text.strip() for td in tds]
                if '売上高' in label:
                    data["売上高"] = values
                elif '純利益' in label:
                    data["純利益"] = values
                elif 'ROE' in label:
                    data["ROE"] = values
    except Exception as e:
        return {"error": str(e)}

    return data
