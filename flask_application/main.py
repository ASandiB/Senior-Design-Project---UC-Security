# This code was deployed on Google Cloud Run services to view the door sensor times
# Unfortunately we weren't able to deploy the live frame on this method, so / is empty.
# Written and implemented by Anthony Sandi

import os
from flask import Flask, Response, render_template_string, request, jsonify
import base64
import time
import logging

time_entries = []

app = Flask(__name__)
# Main page which was a placeholder for websockets/requests at some time, but currently inactive for the Demo
@app.route('/')
def index():
    return "WebSocket Server Running"
# Handles the time pings from the Raspberry Pi
@app.route('/time', methods=['GET', 'POST'])
def handle_time():
    global time_entries
    if request.method == 'POST':
        if request.is_json:
            current_time = request.json.get('current_time')
            if current_time:
                time_entries.append(current_time)
                return jsonify({"message": "Time entry added", "current_time": current_time}), 201
            else:
                return jsonify({"error": "'current_time' field is required"}), 400
        else:
            return jsonify({"error": "Invalid JSON"}), 400

    # Create a string of time entries
    time_entries_str = "<br>".join([f"Door opened at: {entry}" for entry in time_entries])

    return f"""
        <html>
            <head>
                <meta http-equiv="refresh" content="5"> <!-- Refresh page every 5 seconds -->
                <style>
                    body {{
                        background-color: black;
                        color: white;
                        font-family: Arial, sans-serif;
                        text-align: center;
                        padding: 20px;
                    }}
                    .header {{
                        font-size: 24px;
                        font-weight: bold;
                        padding: 10px;
                    }}
                    .entries {{
                        font-size: 20px;
                        padding: 10px;
                    }}
                </style>
            </head>
            <body>
                <div class="header">Time Entries:</div>
                <div class="entries">{time_entries_str if time_entries else "No time entries found."}</div>
            </body>
        </html>
    """

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
