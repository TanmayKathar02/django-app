# Django Minikube Deployment

This repository contains the necessary configurations and files to containerize a Django project and deploy it locally using Minikube with PostgreSQL as the database.

## Project Overview

This project demonstrates how to set up a Django application within Docker containers and orchestrate its deployment using Kubernetes on a local Minikube cluster. It includes configurations for the Django application, a PostgreSQL database, persistent storage, and exposing the application via Ingress.

## Deliverables

1. **Dockerfile**: For building the Django application image.

2. **Kubernetes YAML files**:

   * `django-deployment.yaml`

   * `django-service.yaml`

   * `postgres-deployment.yaml`

   * `postgres-service.yaml`

   * `secret.yaml`

   * `ingress.yaml`

   * `pvc.yaml` (for PostgreSQL persistent storage)

3. **README.md**: This file, explaining required environment variables and step-by-step deployment instructions.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

* **Docker**: For building container images.

* **Minikube**: A tool that runs a single-node Kubernetes cluster locally.

* **kubectl**: The Kubernetes command-line tool for interacting with your cluster.

* **A Django Project**: The Django project you intend to containerize and deploy.

## Dockerization

The `Dockerfile` in this repository is designed to build your Django application image. It handles dependency installation, static file collection, and exposes the application on port `8000`.

### `Dockerfile` (Example Structure)

```dockerfile
# Use Python 3.11 slim image
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-openbsd gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app/

# Copy entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose port
EXPOSE 8000

CMD ["/app/entrypoint.sh"]
```

## Kubernetes Manifests

Here's a brief overview of the Kubernetes YAML files provided:

* **`pvc.yaml`**: Defines a Persistent Volume Claim for PostgreSQL to ensure data persistence across pod restarts.

* **`postgres-deployment.yaml`**: Deploys the PostgreSQL database container.

* **`postgres-service.yaml`**: Creates a Service to expose PostgreSQL internally within the Kubernetes cluster, allowing the Django app to connect to it.

* **`secret.yaml`**: Stores sensitive environment variables (like `SECRET_KEY`, database credentials) securely.

* **`django-deployment.yaml`**: Deploys the Django application, referencing the Docker image and injecting environment variables from the secret. It also includes an `initContainer` or `command` to run migrations and collect static files on startup.

* **`django-service.yaml`**: Exposes the Django application internally within the cluster.

* **`ingress.yaml`**: Configures an Ingress resource to expose the Django application externally via `http://demo.local`.

## Minikube Setup

1. **Start Minikube**:

   ```bash
   minikube start
   ```

2. **Enable Ingress Addon**:

   ```bash
   minikube addons enable ingress
   ```

3. **Add Host Entry**: You need to add an entry to your local hosts file (`/etc/hosts` on Linux/macOS, `C:\Windows\System32\drivers\etc\hosts` on Windows) to map `demo.local` to your Minikube IP.

   First, get your Minikube IP:

   ```bash
   minikube ip
   ```

   (Example output: `192.168.49.2`)

   Then, add the following line to your hosts file:

   ```
   192.168.49.2 demo.local
   ```

   Replace `192.168.49.2` with your actual Minikube IP.

## Required Environment Variables

The following environment variables are crucial for the Django application and PostgreSQL database. These will be stored in `secret.yaml` and `configmap.yaml`.

* **`SECRET_KEY`**: A strong, unique secret key for your Django project.

* **`DB_NAME`**: The name of your PostgreSQL database (e.g., `mydjangodb`).

* **`DB_USER`**: The username for your PostgreSQL database (e.g., `django_user`).

* **`DB_PASSWORD`**: The password for your PostgreSQL database user.

* **`DB_HOST`**: The hostname for the PostgreSQL service (e.g., `postgres-service`).

* **`DB_PORT`**: The port for PostgreSQL (e.g., `5432`).

### `Commands to create secret.yaml and configmap.yaml files` 

  ```bash
   kubectl create secret generic django-secrets   --from-literal=SECRET_KEY=enter-your-secret-key  --from-literal=DB_PASSWORD=enter-db-password
   ```
```bash
   kubectl get secret
   ```
 ```bash
   kubectl create configmap django-config   --from-literal=DB_NAME=db-name   --from-literal=DB_USER=db-user   --from-literal=DB_HOST=postgres   --from-literal=DB_PORT=5432
   ```
```bash
   kubectl get configmap
   ```

## Step-by-Step Deployment

Follow these steps to deploy your Django application on Minikube:

1. **Clone this repository** (or ensure your Django project and these files are in the same directory).

2. **`Dockerfile`**:

   * Ensure your `requirements.txt` is up-to-date with all Django project dependencies.

3. **Build the Docker Image**:
   Navigate to the root of your Django project (where the `Dockerfile` is located) and build the image:

   ```bash
   docker build -t django-app:latest .
   ```
   push the image to docker registry

    ```bash
   docker login
   ```
   ```bash
    docker image tag youruser/your-image:1.0.0 youruser/your-image:latest
   ```
   ```bash
   docker push docker-username/django-app:latest
   ```

5. **Load the Docker Image into Minikube**:
   Minikube needs access to the image you just built.

   ```bash
   minikube image load docker-username/django-app:latest
   ```
6. **Create secret and configmap before applying the kubernetes manifests files**:

 ```bash
   kubectl create secret generic django-secrets   --from-literal=SECRET_KEY=enter-your-secret-key  --from-literal=DB_PASSWORD=enter-db-password
   ```
```bash
   kubectl get secret
   ```
 ```bash
   kubectl create configmap django-config   --from-literal=DB_NAME=db-name   --from-literal=DB_USER=db-user   --from-literal=DB_HOST=postgres   --from-literal=DB_PORT=5432
   ```
```bash
   kubectl get configmap
   ```
7. **Edit django-deployment.yaml **:
   Replace the image with your-image
   ```bash
   vi django-deployment.yaml
   ```
   ```
      spec:
      containers:
      - name: django
        image: ship18/django:latest <----- change the image
   ```
   save esc wq!
   
6. **Apply Kubernetes Manifests**:
   Apply the YAML files in the following order:

   ```bash
   kubectl apply -f pvc.yaml
   kubectl apply -f postgres-deployment.yaml
   kubectl apply -f postgres-service.yaml
   kubectl apply -f django-deployment.yaml
   kubectl apply -f django-service.yaml
   kubectl apply -f ingress.yaml
   ```

7. **Verify Deployment**:
   Check the status of your pods:

   ```bash
   kubectl get pods
   ```

   Ensure all pods (Django and PostgreSQL) are running.

   Check the status of your services:

   ```bash
   kubectl get services
   ```

   Check the status of your ingress:

   ```bash
   kubectl get ingress
   ```

8. **Access the Application**:
   Once all pods are running and the Ingress is ready, open your web browser and navigate to:

   ```
   [http://demo.local](http://demo.local)
   ```

   You should see your Django application running.

## Important Notes

* **Migrations and Static Files**: The `Dockerfile` and `django-deployment.yaml` are configured to run `python manage.py migrate` and `python manage.py collectstatic --noinput` automatically when the Django pod starts. This ensures your database schema is up-to-date and static files are collected.

* **Environment Variables**: Environment variables are injected into the Django pod via the `secret.yaml`. Ensure your Django `settings.py` is configured to read these variables.

* **Production Readiness**: This setup is for local development with Minikube. For production environments, consider using a more robust WSGI server (like Gunicorn or uWSGI), a dedicated static file server (like Nginx), and a managed database service.

* **Debugging**: If you encounter issues, you can check logs of your pods:

  ```bash
  kubectl logs <pod-name>
  ```

  Replace `<pod-name>` with the actual name of your Django or PostgreSQL pod. You can also describe pods for more details:

  ```bash
  kubectl describe pod <pod-name>
  
