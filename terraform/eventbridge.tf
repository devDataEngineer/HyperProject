resource "aws_scheduler_schedule" "extract_lambda_schedule" {
  name       = "extract-lambda-schedule" # could be more in line with other names
  group_name = "default"

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression = "rate(5 minutes)"

  target {
    arn      = aws_lambda_function.extract_lambda.arn
    role_arn = aws_iam_role.extract_lambda_role.arn
  }
}
