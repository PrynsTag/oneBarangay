#!/bin/bash
echo """---
runtime: python39
env: standard
instance_class: F1
inbound_services:
  - warmup
entrypoint: gunicorn main:app -w 1 -k uvicorn.workers.UvicornWorker

handlers:
  - url: /favicon.ico
    static_files: oneBarangay/templates/favicon.ico
    upload: oneBarangay/templates/favicon.ico

  - url: /robots.txt
    static_files: oneBarangay/templates/robots.txt
    upload: oneBarangay/templates/robots.txt

  - url: /humans.txt
    static_files: oneBarangay/templates/humans.txt
    upload: oneBarangay/templates/humans.txt

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
  GS_BUCKET_NAME: \"$GS_BUCKET_NAME\"

automatic_scaling:
  min_idle_instances: automatic
  max_idle_instances: automatic
  min_pending_latency: automatic
  max_pending_latency: automatic
  target_cpu_utilization: 0.75
  max_instances: 1"""
