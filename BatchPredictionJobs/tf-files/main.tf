provider "google" {
  project = "your-project-id"
  region  = var.region
}


module "cloud_function" {
  source                     = "./modules/cloud_func_triggered_by_bucket_obj_creation"
  name                       = var.name
  region                     = var.region
  description                = "Cloud Function to create job predictions"
  memory                     = var.memory
  execution_timeout          = var.execution_timeout
  source_bucket              = "" #bucket where the source code is stored
  source_object_name         = ""
  source_path                = "src.zip"
  runtime                    = "python310"
  entry_point                = "batch_predictions"
  trigger_bucket             = var.trigger_bucket
  service_account_email      = var.service_account_email
}