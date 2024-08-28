resource "aws_cloudwatch_log_group" "state_machine_log_group" {
    name = "/aws/lambda/${var.lambda_name}-state-machine"
    retention_in_days = 7 # CHANGE?
    }

# To start the execution of a state machine from a schedule
resource "aws_cloudwatch_event_rule" "state_machine_trigger" {
    name = "every_5_minutes_rule"
    description = "trigger state machine every 5 minutes"
    schedule_expression = "rate(5 minutes)"
}
# Select the service (the particular step function) you wish to start (JM)
resource "aws_cloudwatch_event_target" "state_machine_target" {
    target_id = "SendtoStepFunctions"
    rule        = aws_cloudwatch_event_rule.state_machine_trigger.name
    arn         = aws_sfn_state_machine.step_function_state_machine.arn
    role_arn    = aws_iam_role.state_machine_role.arn
}

# We might not need a CW rule anymore knowing that Step Functions is going to be
# triggered every 5 minutes, not the first lambda
# 
#  create aws cloude watch event rule to call every 5 min
# resource "aws_cloudwatch_event_rule" "every_5_minutes" {
#   name        = "every_5_minutes_rule"
#   description = "trigger lambda every 5 minute"

#   schedule_expression = "rate(5 minutes)"
  
# }

# #  adding extract lambda to the Cloudwatch event 
# resource "aws_cloudwatch_event_target" "lambda_target" {
#   rule      = aws_cloudwatch_event_rule.every_5_minutes.name
#   target_id = "SendToLambda"
#   arn       = aws_lambda_function.extract_lambda.arn

# }