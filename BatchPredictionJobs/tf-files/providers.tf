terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "< 5.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "< 5.0"
    }
  }
  backend "gcs" {
   bucket  = "bucket-to-store-state"
   prefix  = "prefix-in-the-bucket"
 }
  required_version = ">= 0.13"
}