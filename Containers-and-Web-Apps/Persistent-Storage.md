### Persistent Storage in Azure Web Apps

#### Add a Chat Record 

Replace the code inn `app.py` with the following code to add a chat record to Persistent Storage in Azure Web Apps:

```python
import os
import json
from datetime import datetime
from flask import Flask, request, jsonify
from openai import AzureOpenAI
from dotenv import load_dotenv

app = Flask(__name__)

# Read configuration from environment variables
load_dotenv()

AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_API_URL")
AZURE_OPENAI_API_KEY = os.environ.get("AZURE_API_KEY")
AZURE_OPENAI_MODEL_NAME = os.environ.get("AZURE_MODEL_NAME")
AZURE_OPENAI_API_VERSION = "2024-06-01"

# Persistent storage path in Azure App Service
CHAT_HISTORY_DIR = "/home/chat_history"

# Create directory if it does not exist
os.makedirs(CHAT_HISTORY_DIR, exist_ok=True)

client = AzureOpenAI(
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
)

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    user_message = data.get("message", "")

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": user_message
            },
        ],
        max_tokens=500,
        temperature=0.7,
        model=AZURE_OPENAI_MODEL_NAME,
    )

    assistant_reply = response.choices[0].message.content

    # Create chat record
    chat_record = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_message": user_message,
        "assistant_reply": assistant_reply
    }

    # Save chat history to persistent storage
    filename = f"chat_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.json"

    file_path = os.path.join(CHAT_HISTORY_DIR, filename)

    with open(file_path, "w") as file:
        json.dump(chat_record, file, indent=4)

    return jsonify({
        "model": response.model,
        "reply": assistant_reply,
        "saved_file": file_path
    })


@app.route("/history", methods=["GET"])
def history():

    files = os.listdir(CHAT_HISTORY_DIR)

    return jsonify({
        "stored_files": files
    })

@app.route("/health", methods=["GET"])
def health_check():
    return {'status': 'healthy'}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

Build and deploy the application to Azure Web App:
```bash
docker build . -t aoaipythonapp:v3

az acr login --name $ACR_NAME
docker tag aoaipythonapp:v3 $ACR_NAME.azurecr.io/aoaipythonapp:v3
docker push $ACR_NAME.azurecr.io/aoaipythonapp:v3
```

#### Enable persistent storage using CLI:
Go to App Settings in the Environment Variables section and add the following setting to enable persistent storage in Azure Web Apps:

```bash
WEBSITE_ENABLE_APP_SERVICE_STORAGE=true
```

#### Test the Application
try some queries:
```bash
curl -X POST https://<web-app-name>.azurewebsites.net/chat -H "Content-Type: application/json" -d "{\"message\":\"Can you please suggest some places to travel in India?\"}"
```

Then, check the chat history stored in Azure Web Apps:

```bash
curl -X GET https://<web-app-name>.azurewebsites.net/history
```

