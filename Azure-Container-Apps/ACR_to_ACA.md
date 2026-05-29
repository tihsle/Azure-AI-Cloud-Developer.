## ACR (Azure Container Registry) to ACA (Azure Container Apps)

![ACR_to_ACA](./Images/ACR_to_ACA.png)

### Create a Container Apps Environment

We will now create a container apps environment that will host our Container App.

### Follow the steps laid down in the visuals below:

![step1](./Images/step1.png)
---
![step2](./Images/step2.png)
---
![step3](./Images/step3.png)

### Create a Container App

Now we will create a container app inside the newly created container app environment that will host our image that is contained in our Azure Container Registry (ACR).

![step4](./Images/step4.png)
---
![step5](./Images/step5.png)
---
![step6](./Images/step6.png)
---
![step7](./Images/step7.png)

### Accessing our Chat Application

Once your container app gets provisioned, you can go to the `Revisions and replicas` tab to view the Application's FQDN, navigating to which will lead you to land on your chat application's homepage.

![step8](./Images/step8.png)
---
![step9](./Images/step9.png)
---
![step10](./Images/step10.png)

You can also view the logs of the running version of your container app;
![step11](./Images/step11.png)

### Summary

In this lab, we successfully deployed a containerized chat application from Azure Container Registry (ACR) to Azure Container Apps (ACA). We created a container apps environment, set up a container app, and configured the necessary settings to ensure our application runs smoothly. Finally, we accessed our application and verified its functionality.