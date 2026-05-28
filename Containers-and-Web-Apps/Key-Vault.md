### Using Azure Key Vault Secret Store for Azure Web Apps

1) Create an Azure Key Vault and add secret for your Azure OpenAI API Key.

2) Assign the "Key Vault Secrets User" role to the Azure Web App's managed identity for the Key Vault.

3) Update the Environment Variables in Azure Web App to reference the Key Vault secret using the following syntax:`@Microsoft.KeyVault(SecretUri=https://<your-vault-name>.vault.azure.net/secrets/<secret-name>/)`

Restart the App and you should see the application working with the secrets from Azure Key Vault!
```
curl -X POST http://your-webapp-url/chat -H "Content-Type: application/json" -d "{\"message\":\"Can you please suggest some places to travel in India?\"}"
```