## Instructions

### Log into ECR and create repo
Prior to pushing a new image to the ECR the repository must be created

### Login to the ECR
```
aws ecr get-login --region eu-west-1 --no-include-email | sh
```

### Build docker images and push it to the ECR
```
cd ../docker
docker build -t 111177312954.dkr.ecr.eu-west-1.amazonaws.com/aistemos/dev/airflow:dev .
docker push 111177312954.dkr.ecr.eu-west-1.amazonaws.com/aistemos/dev/airflow:dev
```

### Update helm with new image details
Chart.yaml
```
version: dev
```
values.yaml
```
aws:
  region: eu-west-1
  iamRole: AistemosEKSNodeRole
image:
  repository: "111177312954.dkr.ecr.eu-west-1.amazonaws.com/aistemos/dev/airflow"
  tag: "dev"
```
