## Pushing AI Application to Azure Container Registry (ACR)

![Docker_to_ACR](./Images/Docker_to_ACR.png)

### Build the Docker Image

```bash
docker build -t aoaichatapp:latest .
```

Run the Docker image locally to test:
```bash
docker run -p 5000:80 aoaichatapp:latest
```

### Push the Docker Image to Azure Container Registry (ACR)

```bash
export ACR_NAME=<your-acr-name>

az acr login --name $ACR_NAME
docker tag aoaichatapp:latest $ACR_NAME.azurecr.io/aoaichatapp:latest
docker push $ACR_NAME.azurecr.io/aoaichatapp:latest
```


