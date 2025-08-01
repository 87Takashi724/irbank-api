from flask import Flask, request, jsonify
import requests
import pandas as pd

app = Flask(__name__)

@app.route('/irbank/financial', methods=['GET'])
def get_financials():
    code = request.args.get('code')
    url = "https://irbank.net/download/fy-profit-and-loss.json"
    res = requests.get(url)
    data = pd.DataFrame(res.json())
    df = data[data["証券コード"] == code]
    return jsonify(df.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
