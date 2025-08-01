def get_financial_data(code):
    url = f"https://irbank.net/{code}/financial"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": "https://irbank.net"
    }

    try:
        time.sleep(5)
        res = requests.get(url, headers=headers, timeout=10)
        res.encoding = res.apparent_encoding
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")
        table = soup.select_one("table")
        if not table:
            return {"error": "財務表が見つかりません"}

        data = {}
        for row in table.select("tr"):
            th = row.find("th")
            tds = row.find_all("td")
            if th and tds:
                label = th.text.strip()
                values = [td.text.strip() for td in tds if td.text.strip()]
                if "売上高" in label:
                    data["売上高"] = values
                elif "純利益" in label:
                    data["純利益"] = values
                elif "ROE" in label:
                    data["ROE"] = values

        return data

    except Exception as e:
        return {"error": str(e)}


