resource "aws_scheduler_schedule" "state_machine_scheduler" {
  name = "State-Machine-scheduler"

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression = "rate(5 minutes)"

  target {
    arn      = aws_sfn_state_machine.step_function_state_machine.arn
    role_arn = aws_iam_role.eventbridge_scheduler_iam_role.arn

    input = jsonencode({
      Payload = "Starting the Extact Lambda"
    })
  }
}

output "EventBridgeSchedulerArn" {
  value       = aws_scheduler_schedule.state_machine_scheduler.arn
  description = "EventBridge my-scheduler ARN"
}

output "StateMachineArn" {
      value       = aws_sfn_state_machine.step_function_state_machine.arn
  description = "Step Function my-state-machine ARN"
}
