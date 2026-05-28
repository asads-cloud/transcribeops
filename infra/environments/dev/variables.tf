variable "aws_region" {
  description = "AWS region for dev resources"
  type        = string
  default     = "eu-west-2"
}

variable "project_name" {
  description = "Project name used for resource naming"
  type        = string
  default     = "transcribeops"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}