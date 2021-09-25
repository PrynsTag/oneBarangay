#!/bin/bash
echo """---
runtime: python39
env: standard
instance_class: F1
inbound_services:
  - warmup
entrypoint: python main.py

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
  GOOGLE_STORAGE_CREDENTIALS: \"$GOOGLE_STORAGE_CREDENTIALS\"
  CIRCLE_TOKEN: \"$CIRCLE_TOKEN\"
  CLOUD_STORAGE_KEY: \"$CLOUD_STORAGE_KEY\"
  COVERALLS_REPO_TOKEN: \"$COVERALLS_REPO_TOKEN\"
  DJANGO_SECRET_KEY: \"$DJANGO_SECRET_KEY\"
  DJANGO_SETTINGS_MODULE: \"$DJANGO_SETTINGS_MODULE\"
  GCLOUD_AUTH_KEY: \"$GCLOUD_AUTH_KEY\"
  GOOGLE_COMPUTE_ZONE: \"$GOOGLE_COMPUTE_ZONE\"
  GOOGLE_PROJECT_ID: \"$GOOGLE_PROJECT_ID\"
  GS_STATIC_BUCKET_NAME: \"$GS_STATIC_BUCKET_NAME\"
  GS_MEDIA_BUCKET_NAME: \"$GS_MEDIA_BUCKET_NAME\"
  JIRA_API_TOKEN: \"$JIRA_API_TOKEN\"
  AZURE_FORM_RECOGNIZER_KEY: \"$AZURE_FORM_RECOGNIZER_KEY\"
  AZURE_FORM_RECOGNIZER_ENDPOINT: \"$AZURE_FORM_RECOGNIZER_ENDPOINT\"
  CUSTOM_TRAINED_MODEL_ID: \"$CUSTOM_TRAINED_MODEL_ID\"
  CONTAINER_SAS_URL: \"$CONTAINER_SAS_URL\"

automatic_scaling:
  min_idle_instances: automatic
  max_idle_instances: automatic
  min_pending_latency: automatic
  max_pending_latency: automatic
  target_cpu_utilization: 0.75
  max_instances: 1"""
