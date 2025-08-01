from bs4 import BeautifulSoup

@app.route("/api/financials/<code>")
def get_financials(code):
    url = f"https://irbank.net/{code}/fy"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    try:
        table = soup.select_one("table")  # 最初のテーブルを取得
        headers = [th.text.strip() for th in table.select("thead th")]
        rows = []
        for tr in table.select("tbody tr"):
            cells = [td.text.strip() for td in tr.select("td")]
            if cells:
                rows.append(dict(zip(headers, cells)))

        return jsonify({"code": code, "financials": rows})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
