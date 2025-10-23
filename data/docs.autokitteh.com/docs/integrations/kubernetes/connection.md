---
sidebar_label: Connection
description: Initialize a connection with an service account
---

# Connect Your Kubernetes Cluster to Autokitteh

This guide helps you expose your Kubernetes API securely and create a non-expiring kubeconfig file in JSON format for use with Autokitteh.

> This guide is intended for **Autokitteh self-hosted/local version only**.

## Prerequisites

- A running Kubernetes cluster (e.g. Minikube)
- `kubectl` installed and configured

## Step-by-Step Instructions

### Step 1: Create a Kubernetes Service Account

```bash
kubectl create serviceaccount autokitteh
```

### Step 2: Grant Permissions (Cluster-Wide)

```bash
kubectl create clusterrolebinding autokitteh-access-binding \
  --clusterrole=cluster-admin \
  --serviceaccount=default:autokitteh
```

Note: You can replace `cluster-admin` with a custom role for limited access.

### Step 3: Create a Non-Expiring Token

```bash
kubectl apply -f - <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: autokitteh-token
  annotations:
    kubernetes.io/service-account.name: "autokitteh"
type: kubernetes.io/service-account-token
EOF
```

Then wait a few seconds and extract the token:

```bash
kubectl get secret autokitteh-token -o jsonpath="{.data.token}" | base64 --decode
```

Copy and save the token for use in the config file.

### Step 4: Get Your Kubernetes API Server Address

First, get your local API server URL (including the port):

```bash
kubectl config view --minify -o jsonpath="{.clusters[0].cluster.server}"
```

Copy the what shown in the terminal, such as:

```bash
https://127.0.0.1:64742
```

### Step 5: Create the kubeconfig as JSON

Create a file called `k8s-api-config.json` and paste the following, replacing the placeholders:

```json
{
  "apiVersion": "v1",
  "kind": "Config",
  "current-context": "autokitteh-context",
  "clusters": [
    {
      "name": "autokitteh-cluster",
      "cluster": {
        "server": "https://REPLACE_WITH_URL",
        "insecure-skip-tls-verify": true
      }
    }
  ],
  "users": [
    {
      "name": "autokitteh-user",
      "user": {
        "token": "REPLACE_WITH_YOUR_TOKEN"
      }
    }
  ],
  "contexts": [
    {
      "name": "autokitteh-context",
      "context": {
        "cluster": "autokitteh-cluster",
        "user": "autokitteh-user",
        "namespace": "default"
      }
    }
  ]
}
```

Make sure to:

- Replace `https://REPLACE_WITH_URL` with your actual URL from the previous step
- Replace `REPLACE_WITH_YOUR_TOKEN` with the actual token from Step 3

### Step 6: Create the Autokitteh connection

- Create a Kubernetes connection in the Autokitteh UI (web platform)
- Copy the full contents of `k8s-api-config.json` and paste it in the `config_file` field
- Paste it into the **connection variable field** labeled `K8s Config File`

### More Info

For web platform use (not local), you can follow this CNCF guide to expose your Kubernetes API, but this is not safe for production:
https://www.cncf.io/blog/2025/03/12/expose-the-kubernetes-api-and-access-it-anywhere/
