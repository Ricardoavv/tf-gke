locals {
  project_id = "TODO"  #TODO=replace with your project id
}

provider "google" {
  project = local.project_id
  region  = "us-central1" #replae with the region of your project region
}

# Only needed to enable managed prometheus
provider "google-beta" {
  project = local.project_id
  region  = "us-central1" #replae with the region of your project region
}

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.42"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 4.42"
    }
  }

  required_version = "> 1.0.0"
}
