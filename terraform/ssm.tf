resource "aws_ssm_parameter" "ssm_parameter" {
  name  = var.ssm_parameter_name
  type  = "String"
  value = "1990-01-01 10:10:10.111111"
}
