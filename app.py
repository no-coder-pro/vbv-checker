import os
from flask import Flask, request, jsonify, send_from_directory
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_KEY = "VDX-SHA2X-NZ0RS-O7HAM"
BASE_URL = "https://api.voidapi.xyz/v2/vbv"

@app.route('/', methods=['GET'])
def index():
    return send_from_directory(os.getcwd(), 'index.html')

@app.route('/lookup', methods=['GET'])
def lookup():
    card = request.args.get('auth')
    if not card:
        return jsonify({"success": False, "message": "Card details required"}), 400
    
    try:
        # Construct the API URL
        api_url = f"{BASE_URL}?key={API_KEY}&card={card}"
        
        # Call the external API
        response = requests.get(api_url)
        data = response.json()
        
        if data.get("success"):
            vbv_data = data.get("data", {})
            status = vbv_data.get("status", "")
            
            if "successful" in status.lower():
                return jsonify({
                    "status": "success",
                    "message": f"VBV Approved | {status}"
                })
            else:
                return jsonify({
                    "status": "declined",
                    "message": f"VBV Dead | {status}"
                })
        else:
            return jsonify({
                "status": "error",
                "message": data.get("message", "API request failed")
            })

    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
