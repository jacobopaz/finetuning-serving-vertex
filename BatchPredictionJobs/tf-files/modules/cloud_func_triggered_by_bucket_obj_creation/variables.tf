variable "name" {
  description = "Name of the Cloud Function."
  type        = string
}

variable "description" {
  description = "Description of the Cloud Function."
  type        = string
  default     = "A Google Cloud Function managed by Terraform"
}

variable "region" {
    description = "Region of the Cloud Function."
    type        = string
    default     = "europe-west4"
}

variable "source_bucket" {
  description = "Bucket where the source code of the function is."
  type        = string
}

variable "source_object_name" {
  description = "Name of the object inside the source bucket where the source code is."
  type        = string
}

variable "source_path" {
  description = "Local path where the source code is."
  type        = string
}

variable "max_instance_count" {
  description = "Maximum number of Cloud Functions instances."
  type        = number
  default     = 3000
}

variable "min_instance_count" {
  description = "Minimum number of Cloud Functions instances."
  type        = number
  default     = 0
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

variable "runtime" {
  description = "Runtime of the Cloud Function."
  type        = string
  default     = "python310"
}

variable "entry_point" {
  description = "Name of the function to execute when the Cloud Function is triggered."
  type        = string
}

variable "trigger_bucket" {
  description = "Name of the bucket that triggers the Cloud Function."
  type        = string
}

variable "service_account_email" {
  description = "The email of the service account associated with the Cloud Function."
  type        = string
}