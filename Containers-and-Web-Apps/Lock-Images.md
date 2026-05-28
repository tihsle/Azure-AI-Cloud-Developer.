## Lock and Unlock Images in ACR

### Lock an ACR Image
```bash
az acr repository update \
    --name $ACR_NAME \
    --image aoaipythonapp:v1 \
    --write-enabled false
```

### Unlock an ACR Image
```bash
az acr repository update \
    --name $ACR_NAME \
    --image aoaipythonapp:v1 \
    --write-enabled true
```