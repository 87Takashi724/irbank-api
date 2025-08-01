from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def index():
    return "IR Bank Scraper API is up!"

@app.route("/api/financials/<code>", methods=["GET"])
def get_financials(code):
    url = f"https://irbank.net/{code}/fy"
    res = requests.get(url)
    if res.status_code != 200:
        return jsonify({"error": f"HTTP status {res.status_code}"}), 500

    soup = BeautifulSoup(res.text, "html.parser")
    table = soup.select_one("table")
    if not table:
        return jsonify({"error": "Financial table not found"}), 404

    headers = [th.text.strip() for th in table.select("thead th")]
    rows = []
    for tr in table.select("tbody tr"):
        cells = [td.text.strip() for td in tr.select("td")]
        if cells and len(cells) == len(headers):
            rows.append(dict(zip(headers, cells)))

    return jsonify({"code": code, "financials": rows})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
