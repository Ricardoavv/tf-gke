provider "google" {
  project = "tf-ai-gke"
  region = "us-cental1"
}

terraform {
  backend "gcs" {
    bucket = "tf-gke-backend"
    prefix = "terraform/state"
  }
  required_providers {
    google = {
        source = "hashicorp/google"
        version = "~> 4.0"
    }
  }
}

