resource "aws_ssm_parameter" "ssm_parmeter" {
  name  = var.ssm_parameter_name
  type  = "String"
  value = "315550800"
}