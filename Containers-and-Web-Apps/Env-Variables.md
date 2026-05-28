### Injecting Environment Variables into Azure Web Apps

Change the following piece of code in `app.py` to read the configuration from environment variables:

```python
AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_API_URL")
AZURE_OPENAI_API_KEY = os.environ.get("AZURE_API_KEY")
AZURE_OPENAI_MODEL_NAME = os.environ.get("AZURE_MODEL_NAME")
```

Rebuild the Docker image and push it to ACR again:

```bash
docker build . -t aoaipythonapp:v2
docker tag aoaipythonapp:v2 $ACR_NAME.azurecr.io/aoaipythonapp:v2
docker push $ACR_NAME.azurecr.io/aoaipythonapp:v2
```

Then, update the image and environment variables in Azure Web App to use the new image and environment variables. You can do this through the Azure Portal - helps you visualize the changes and makes up for a better learning experience.