## Creating an HTTP Triggered OpenAI Chat Function App

make sure the following import statements are loaded in `function_app.py`:
```python
import os
from openai import AzureOpenAI
import json
```

paste the following python code in `function_app.py`:
```python
    logging.info('Python HTTP trigger function processed a request.')
    
    # loading the environment variables
    azure_openai_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    azure_openai_api_key = os.environ["AZURE_OPENAI_API_KEY"]
    chat_completions_model = os.environ["CHAT_COMPLETIONS_MODEL"]

    # extracting the user query from the request payload
    req_body = req.get_json()
    user_query = req_body.get("user_query")

    
    if user_query:
        # creating the Azure OpenAI Client 
        azure_openai_client = AzureOpenAI(
            azure_endpoint = azure_openai_endpoint,
            api_version = "2024-06-01",
            api_key = azure_openai_api_key
        )
        
        # sending a request to the chat completions model deployment
        response = azure_openai_client.chat.completions.create(
            model = chat_completions_model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant"
                },
                {
                    "role": "user",
                    "content": user_query
                }
            ],
            temperature = 0.7
        )
        
        # extracting the assistant response text from the api response
        assistant_reponse_text = response.choices[0].message.content
        
        # returning the assistant response text as an http call output
        return func.HttpResponse(assistant_reponse_text)
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a user_query in the query string or in the request body for a personalized response.",
             status_code=200
        )
```

make sure the `requirements.txt` file has the following dependencies listed:
```python
azure-functions==2.1.0
openai==2.38.0
```

Run the following set of commands to finally publish the function app to azure:
```bash
func azure functionapp publish <FUNCTION_APP_NAME_ON_AZURE>
```