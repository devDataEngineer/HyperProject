# #  create aws cloude watch event rule to call every 5 min
resource "aws_cloudwatch_event_rule" "every_5_minutes" {
  name        = "every_5_minutes_rule"
  description = "trigger lambda every 5 minute"

  schedule_expression = "rate(5 minutes)"
  
}

#  adding extract lambda to the Cloudwatch event 
resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.every_5_minutes.name
  target_id = "SendToLambda"
  arn       = aws_lambda_function.extract_lambda.arn

}

