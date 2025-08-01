from flask import Flask, request, jsonify
import requests
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    return "IR Bank API is up and running!"

@app.route("/irbank/financial", methods=["GET"])
def get_financial():
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "code parameter is required"}), 400

    # IRバンクの通期損益データを取得
    url = "https://irbank.net/download/fy-profit-and-loss.json"
    res = requests.get(url)
    res.raise_for_status()

    df = pd.DataFrame(res.json())
    matched = df[df["証券コード"].astype(str) == str(code)]

    # 最大10年分を返す
    result = matched.to_dict(orient="records")
    return jsonify(result)
