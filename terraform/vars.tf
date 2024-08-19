variable "bucket_prefix" {
  type    = string
  default = "team-hyper-accelerated-dragon-bucket"
}


variable "lambda_name" {
  type    = string
  default = "hyper-accelerated-dragon-lambda"
}

variable "python_runtime" {
  type    = string
  default = "python3.12"
}

variable "ssm_parameter_name" {
  type = string
  default = "dragons_time_param"
}
