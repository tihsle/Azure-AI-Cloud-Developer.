## Function App with an Input and Output Binding

In the same `function_app.py` file, add the service bus queue triggered function code with an input and output binding:
```python
@app.service_bus_queue_trigger(
    arg_name="msg",
    queue_name="YOUR-SERVICE-BUS-QUEUE-NAME",
    connection="SERVICE_BUS_CONNECTION"
)
@app.blob_output(
    arg_name="outputblob",
    path="descriptions/{rand-guid}.txt",
    connection="STORAGE_ACCOUNT_CONNECTION"
)
def generate_image_description(
    msg: func.ServiceBusMessage,
    outputblob: func.Out[str]
):
    logging.info("Service Bus Triggered Function processed a message")
    
    # extracting the blob_url from the queue payload
    payload = json.loads(
        msg.get_body().decode("utf-8")
    )

    image_url = payload["data"]["url"]
    
    # loading the environment variables
    azure_openai_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    azure_openai_api_key = os.environ["AZURE_OPENAI_API_KEY"]
    chat_completions_model = os.environ["CHAT_COMPLETIONS_MODEL"]

    azure_openai_client = AzureOpenAI(
        azure_endpoint = azure_openai_endpoint,
        api_version = "2024-06-01",
        api_key = azure_openai_api_key
    )

    response = azure_openai_client.chat.completions.create(
        model = chat_completions_model,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI assistant"
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Describe this image"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        }
                    }
                ]
            }
        ],
        temperature = 0.7
    )

    image_description = response.choices[0].message.content

    outputblob.set(
        image_description
    )

    logging.info(
        f"image description generated: {image_description}"
    )
```

Publish the function app to azure portal through CLI and you shall now see two functions running within the same function app resource:
```bash
func azure functionapp publish <FUNCTION_APP_NAME_ON_AZURE>
```

Make sure you sent in the following environment variables:
```bash
SERVICE_BUS_CONNECTION="YOUR-SERVICE-BUS-CONNECTION-STRING"
STORAGE_ACCOUNT_CONNECTION="YOUR-STORAGE-ACCOUNT-CONNECTION-STRING"
```