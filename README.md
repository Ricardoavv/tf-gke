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

this commands log you in Google cloud console, position in the working directory where the configuration files are for the
infrastructure and then initialize a Terraform working directory,create an execution plan, 
apply the Terraform configuration defined.
(this can last a while )

Second step, access to the kubernetes cluster.
run this command
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

fourth step, Create the deployment for the prometheus-ui

- cd prometheus-ui
- kubectl create -f 0-service-account.yaml
- kubectl create -f 1-deployment.yaml
- kubectl create -f 2-service.yaml
- cd ..

kubectl -n monitoring port-forward svc/fronted 9090
