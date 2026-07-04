import os
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import Flask-CORS
from openai import AzureOpenAI
from azure.appconfiguration.provider import load, SettingSelector, WatchKey
from azure.identity import DefaultAzureCredential
from featuremanagement import FeatureManager
import logging

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes and origins

# creating the App Configuration Selector Object
selects = [
    SettingSelector(key_filter="AzureOpenAI:*", label_filter="\0"),
    SettingSelector(key_filter="AzureOpenAI:*", label_filter="Production")
]

# Using the System Assigned Identity Credential
credential = DefaultAzureCredential()

# Creating the App Configuration Loader Client Object
config = load(
    endpoint = os.getenv("AZURE_APPCONFIG_ENDPOINT"),
    credential=credential,
    selects = selects,
    feature_flag_enabled = True,
    feature_flag_refresh_enabled = True,
    refresh_on = [WatchKey("Sentinel")],
    keyvault_credential=credential,
    refresh_interval = 30
)

# Creating the Feature Manager Object
feature_manager = FeatureManager(config)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        config.refresh()
        if feature_manager.is_enabled("UseNewChatModel"):
            azure_openai_endpoint = config["AzureOpenAI:Endpoint"]
            azure_openai_api_key = config["AzureOpenAI:Key"]
            chat_completions_model_name = config["AzureOpenAI:NewModelName"]

            # creating the Azure OpenAI Client
            client = AzureOpenAI(
                api_version = "2024-06-01",
                azure_endpoint=azure_openai_endpoint,
                api_key=azure_openai_api_key
            )

            data = request.get_json()
            user_message = data.get("message", "")

            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_message},
                ],
                temperature=0.7,
                model=chat_completions_model_name
            )

            return jsonify({
                "model": response.model,
                "reply": response.choices[0].message.content
            })
        else:
            azure_openai_endpoint = config["AzureOpenAI:Endpoint"]
            azure_openai_api_key = config["AzureOpenAI:Key"]
            chat_completions_model_name = config["AzureOpenAI:ModelName"]

            # creating the Azure OpenAI Client
            client = AzureOpenAI(
                api_version = "2024-06-01",
                azure_endpoint=azure_openai_endpoint,
                api_key=azure_openai_api_key
            )

            data = request.get_json()
            user_message = data.get("message", "")

            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_message},
                ],
                temperature=0.7,
                model=chat_completions_model_name
            )

            return jsonify({
                "model": response.model,
                "reply": response.choices[0].message.content
            })
    except Exception as ex:
        logging.info("Encountered error: {}".format(str(ex)))
        return jsonify({
            "error": f"error: {str(ex)}"
        })
        


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)