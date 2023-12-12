resource "google_storage_bucket_object" "object" {
  name   = "${var.source_object_name}.${filemd5(var.source_path)}"
  bucket = var.source_bucket
  source = var.source_path  
}


resource "google_cloudfunctions2_function" "function" {
  name                  = var.name
  location              = var.region
  description           = var.description
  build_config {
    runtime     = var.runtime
    entry_point = var.entry_point
    source {
      storage_source {
        bucket = var.source_bucket
        object = google_storage_bucket_object.object.name
      }
    }
  }

  service_config {
    max_instance_count             = var.max_instance_count
    min_instance_count             = var.min_instance_count
    available_memory               = var.memory
    timeout_seconds                = var.execution_timeout
    ingress_settings               = "ALLOW_ALL"
    all_traffic_on_latest_revision = true
    service_account_email          = var.service_account_email
  } 

  event_trigger {
    trigger_region        = var.region
    event_type            = "google.cloud.storage.object.v1.finalized"
    retry_policy          = "RETRY_POLICY_DO_NOT_RETRY"
    service_account_email = var.service_account_email
    event_filters {
      attribute = "bucket"
      value     = var.trigger_bucket
    }
  }
}