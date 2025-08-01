from flask import Flask, jsonify, request
import requests
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    return "IR BANK API is running!"

@app.route("/debug")
def debug():
    try:
        res = requests.get("https://irbank.net/download/fy-profit-and-loss.json")
        data = res.json()
        df = pd.DataFrame(data)
        return jsonify({
            "columns": list(df.columns),
            "num_records": len(df),
            "sample_first_3": df.head(3).to_dict(orient="records")
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/irbank/financial", methods=["GET"])
def get_financial():
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "code parameter is required"}), 400

    try:
        res = requests.get("https://irbank.net/download/fy-profit-and-loss.json")
        df = pd.DataFrame(res.json())
        matched = df[df["証券コード"].astype(str) == str(code)]
        return jsonify(matched.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
