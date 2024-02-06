@app.route('/stock_data', methods=['GET'])
def get_stock_data():
    try:
        # Modify the query to fetch relevant stock data from the stock_trade table
        query = "SELECT date, open, high, low, close, volume FROM stock_trade"
        result = execute_query(query)

        # Return the stock data as JSON
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})