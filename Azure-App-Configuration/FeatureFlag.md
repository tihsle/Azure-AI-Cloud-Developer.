## Enable Feature Flag with Azure App Configuration

### Build and Publish application to Azure Web App

Build the docker image for the application `ChatBackend` contained in the same working folder as this file:
```bash
# Set the export variable to store the name of the Azure Container Registry
export ACR_NAME="YOUR-ACR-NAME"

# Push image to ACR after building via ACR tasks
az acr login --name $ACR_NAME
az acr build --registry $ACR_NAME --image appconfigdemo:v1 .
```

When publishing to Azure Web App, be sure to create the following environment variable:
```bash
AZURE_APPCONFIG_ENDPOINT="YOUR-AZURE-APP-CONFIG-ENDPOINT-VALUE"
```

Assign the system assigned managed identity of the web app the role of `App Config Data Reader` on the Azure App Configuration resource.

### Create a Feature Flag and Key-Value Pair

In your Azure App Configuration resource create a new feature flag named `UseNewChatModel` and a new key-value pair named `AzureOpenAI:NewModelName`
