@app.route("/debug", methods=["GET"])
def debug():
    import requests
    import pandas as pd
    url = "https://irbank.net/download/fy-profit-and-loss.json"
    data = requests.get(url).json()
    df = pd.DataFrame(data)
    return jsonify({
        "columns": list(df.columns),
        "num_records": len(df),
        "sample_first": df.head(3).to_dict(orient="records")
    })
