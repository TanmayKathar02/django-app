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

* **A Django Project**: The Django project you intend to containerize and deploy. (This README assumes you have a Django project ready in the same directory as these files).

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

The following environment variables are crucial for the Django application and PostgreSQL database. These will be stored in `secret.yaml`.

* **`SECRET_KEY`**: A strong, unique secret key for your Django project.

* **`DB_NAME`**: The name of your PostgreSQL database (e.g., `mydjangodb`).

* **`DB_USER`**: The username for your PostgreSQL database (e.g., `django_user`).

* **`DB_PASSWORD`**: The password for your PostgreSQL database user.

* **`DB_HOST`**: The hostname for the PostgreSQL service (e.g., `postgres-service`).

* **`DB_PORT`**: The port for PostgreSQL (e.g., `5432`).

### `secret.yaml` (Example Structure)

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: django-secrets
type: Opaque
data:
  # Base64 encoded values for security
  # Use 'echo -n "your_secret_key" | base64' to generate these
  DJANGO_SECRET_KEY: <base64_encoded_django_secret_key>
  DB_NAME: <base64_encoded_db_name>
  DB_USER: <base64_encoded_db_user>
  DB_PASSWORD: <base64_encoded_db_password>
  DB_HOST: <base64_encoded_db_host> # e.g., postgres-service
  DB_PORT: <base64_encoded_db_port> # e.g., 5432
```

## Step-by-Step Deployment

Follow these steps to deploy your Django application on Minikube:

1. **Clone this repository** (or ensure your Django project and these files are in the same directory).

2. **Update `Dockerfile`**:

   * Open `Dockerfile` and replace `your_project_name` with the actual name of your Django project.

   * Ensure your `requirements.txt` is up-to-date with all Django project dependencies.

3. **Build the Docker Image**:
   Navigate to the root of your Django project (where the `Dockerfile` is located) and build the image:

   ```bash
   docker build -t django-app:latest .
   ```

4. **Load the Docker Image into Minikube**:
   Minikube needs access to the image you just built.

   ```bash
   minikube image load django-app:latest
   ```

5. **Configure `secret.yaml`**:

   * Open `secret.yaml`.

   * Generate base64 encoded values for `DJANGO_SECRET_KEY`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, and `DB_PORT`.

   * Replace the `<base64_encoded_...>` placeholders with your generated values.

6. **Apply Kubernetes Manifests**:
   Apply the YAML files in the following order:

   ```bash
   kubectl apply -f pvc.yaml
   kubectl apply -f postgres-deployment.yaml
   kubectl apply -f postgres-service.yaml
   kubectl apply -f secret.yaml
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

* **Environment Variables**: Environment variables are injected into the Django pod via the `secret.yaml`. Ensure your Django `settings.py` is configured to read these variables (e.g., using `os.environ.get('DB_NAME')`).

* **Production Readiness**: This setup is for local development with Minikube. For production environments, consider using a more robust WSGI server (like Gunicorn or uWSGI), a dedicated static file server (like Nginx), and a managed database service.

* **Debugging**: If you encounter issues, you can check logs of your pods:

  ```bash
  kubectl logs <pod-name>
  ```

  Replace `<pod-name>` with the actual name of your Django or PostgreSQL pod. You can also describe pods for more details:

  ```bash
  kubectl describe pod <pod-name>
  
