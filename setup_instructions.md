# Setup Instructions for Veo Proxy Server

## Enable Vertex AI API

You need to enable the Vertex AI API for your project. The error message provides a direct link:

1. Visit: https://console.developers.google.com/apis/api/aiplatform.googleapis.com/overview?project=daring-runway-465515-i2

2. Click "Enable API" button

3. Wait a few minutes for the changes to propagate

## Alternative: Using gcloud CLI

If you have the gcloud CLI installed, you can enable the API with:

```bash
gcloud services enable aiplatform.googleapis.com --project=daring-runway-465515-i2
```

## Verify Service Account Permissions

After enabling the API, ensure your service account has the necessary permissions:

1. Go to IAM & Admin in Google Cloud Console
2. Find your service account: `google-veo-3-app@daring-runway-465515-i2.iam.gserviceaccount.com`
3. Ensure it has one of these roles:
   - `Vertex AI User` (recommended)
   - `Vertex AI Developer`
   - `Editor` or `Owner` (broader permissions)

## Test the Setup

After enabling the API and waiting a few minutes:

```bash
# Test the proxy server
python test_proxy.py
```

## Additional APIs that might be needed

Depending on your usage, you might also need to enable:
- Cloud Storage API (if using GCS for output)
- Cloud Resource Manager API

Enable them with:
```bash
gcloud services enable storage-api.googleapis.com --project=daring-runway-465515-i2
gcloud services enable cloudresourcemanager.googleapis.com --project=daring-runway-465515-i2
```