## Building Images with ACR Tasks

### Quick Tasks for on-demand builds

The following command builds an image from a local Dockerfile and pushes it to the registry:
```bash
az acr build --registry $ACR_NAME --image aoaipythonapp:acr-tasks .
```