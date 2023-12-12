variable "name" {
  description = "Name of the Cloud Function."
  type        = string
  default     = "batch_prediction_jobs_zephyr"
}

variable "region" {
    description = "Region of the Cloud Function."
    type        = string
    default     = "europe-west4"
}

variable "memory" {
  description = "Amount of memory available to the function."
  type        = string
  default     = "512M"
}

variable "execution_timeout" {
  description = "Maximum execution duration of the Cloud Function."
  type        = number
  default     = 540
}

variable "trigger_bucket" {
  description = "Name of the bucket that triggers the Cloud Function."
  type        = string
  default     = "yourtriggerbucket"
}

variable "service_account_email" {
  description = "The email of the service account associated with the Cloud Function."
  type        = string
}