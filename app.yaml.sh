#!/bin/bash
echo """---
runtime: python39
env: standard
instance_class: F4_1G
inbound_services:
  - warmup
entrypoint: gunicorn main:app -w 8 -k uvicorn.workers.UvicornWorker

handlers:
  - url: /favicon.ico
    static_files: one_barangay/templates/favicon.ico
    upload: one_barangay/templates/favicon.ico

  - url: /robots.txt
    static_files: one_barangay/templates/robots.txt
    upload: one_barangay/templates/robots.txt

  - url: /humans.txt
    static_files: one_barangay/templates/humans.txt
    upload: one_barangay/templates/humans.txt

env_variables:
  APP_ENGINE_ALLOWED_HOST: \"$APP_ENGINE_ALLOWED_HOST\"
  CIRCLE_TOKEN: \"$CIRCLE_TOKEN\"
  COVERALLS_REPO_TOKEN: \"$COVERALLS_REPO_TOKEN\"
  DJANGO_SECRET_KEY: \"$DJANGO_SECRET_KEY\"
  DJANGO_SETTINGS_MODULE: \"$DJANGO_SETTINGS_MODULE\"
  JIRA_API_TOKEN: \"$JIRA_API_TOKEN\"

  GCLOUD_AUTH_KEY: \"$GCLOUD_AUTH_KEY\"
  GOOGLE_COMPUTE_ZONE: \"$GOOGLE_COMPUTE_ZONE\"
  GOOGLE_PROJECT_ID: \"$GOOGLE_PROJECT_ID\"
  SECRET_MANAGER_PROJECT_ID: \"$SECRET_MANAGER_PROJECT_ID\"
  CLOUD_STORAGE_KEY: \"$CLOUD_STORAGE_KEY\"

  GS_STATIC_BUCKET_NAME: \"$GS_STATIC_BUCKET_NAME\"
  GS_MEDIA_BUCKET_NAME: \"$GS_MEDIA_BUCKET_NAME\"
  FILE_BUCKET_FOLDER: \"$FILE_BUCKET_FOLDER\"
  MEDIA_BUCKET_FOLDER: \"$MEDIA_BUCKET_FOLDER\"
  SETTINGS_NAME: \"$SETTINGS_NAME\"
  GOOGLE_STORAGE_CREDENTIALS: \"$GOOGLE_STORAGE_CREDENTIALS\"

  AZURE_FORM_RECOGNIZER_KEY: \"$AZURE_FORM_RECOGNIZER_KEY\"
  AZURE_FORM_RECOGNIZER_ENDPOINT: \"$AZURE_FORM_RECOGNIZER_ENDPOINT\"
  CUSTOM_TRAINED_MODEL_ID: \"$CUSTOM_TRAINED_MODEL_ID\"
  CONTAINER_SAS_URL: \"$CONTAINER_SAS_URL\"

  AZURE_STORAGE_CONTAINER_SAS: \"$AZURE_STORAGE_CONTAINER_SAS\"
  AZURE_STORAGE_CONTAINER_NAME: \"$AZURE_STORAGE_CONTAINER_NAME\"
  AZURE_STORAGE_BLOB_NAME: \"$AZURE_STORAGE_BLOB_NAME\"

automatic_scaling:
  max_instances: 2
  min_idle_instances: 0
  max_idle_instances: 0
  min_pending_latency: 900ms
  max_pending_latency: automatic
  target_cpu_utilization: 0.95
  target_throughput_utilization: 0.95
  max_concurrent_requests: 80"""
