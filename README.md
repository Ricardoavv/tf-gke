This project is an AI that can apply .tfvars to changes the resources values of a kubernetes cluster in Google cloud platform 
Requirements: install the following tools, google cloud CLI, python and terraform

First step deploy the infrastructure
Run the following commands in a terminal where the whole project is :

- gcloud auth login
- cd terraform
- terraform init
- terraform plan 
- terraform apply 
- cd ..

This commands log you in Google cloud console, position in the working directory where the configuration files are for the
infrastructure and then initialize a Terraform working directory,create an execution plan, 
apply the Terraform configuration defined.
(this can last a while )

Second step, access to the kubernetes cluster.
Run this command
- gcloud container clusters get-credentials [CLUSTER-NAME] --zone us-central1-a --project [PROJECT-ID]

Third step, Create the deployment for the node-exporter

- cd k8s
- cd node-exporter
- kubectl create -f 0-namespace.yaml
- kubectl create -f 1-service-account.yaml
- kubectl create -f 2-cluster-role.yaml
- kubectl create -f 3-cluster-role-binding.yaml
- kubectl create -f 4-daemonset.yaml
- kubectl create -f 5-pod-monitoring.yaml
- cd ..

Fourth step, Create the deployment for the prometheus-ui

- cd prometheus-ui
- kubectl create -f 0-service-account.yaml
- kubectl create -f 1-deployment.yaml
- kubectl create -f 2-service.yaml
- cd ..
- kubectl -n monitoring port-forward svc/frontend 9090

you can go to your browser and type https://localhost:9090 and verify if the UI is linked to your local port 9090

Fifth step, go to this link and follow the steps
Must skip the step of creating a cluster because, we did it with terraform in the first step
And also the set environment step must be skip

- https://cloud.google.com/architecture/distributed-load-testing-using-gke

Once you complete and everything is ok you can continue with the next step

Sixth step
Run this command  in the working directory of AI

- pip3 install prometheus-api-client google-auth google-auth-httplib2 google-auth-oauthlib tensorflow subprocess

Seventh execute the AI 

- pyton3 AI.py

Finally you can see the matrics of your cluster, remember that Fifth step is going to generate resource consumption. 
If you set lotus to use a lot of resources, and then run the AI
you should see and execution plan of the changes are going to be apply in your infrastructure