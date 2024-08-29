resource "aws_sfn_state_machine" "step_function_state_machine" {
    name = "${var.lambda_name}-state-machine" 
    role_arn      = aws_iam_role.state_machine_role.arn 
    definition = <<EOF
    {
    "Comment": "A description of my state machine",
    "StartAt": "Invoke EXTRACT lambda",
    "States": {
        "Invoke EXTRACT lambda": {
        "Type": "Task",
        "Resource": "arn:aws:states:::lambda:invoke",
        "OutputPath": "$.Payload",
        "Parameters": {
            "Payload.$": "$",
            "FunctionName": "arn:aws:lambda:eu-west-2:590183970951:function:hyper-accelerated-dragon-lambda-extract:$LATEST"
            },
        "Next": "Invoke TRANSFORM Lambda"
        },
        "Invoke TRANSFORM Lambda": {
        "Type": "Task",
        "Resource": "arn:aws:states:::lambda:invoke",
        "OutputPath": "$.Payload",
        "Parameters": {
            "Payload.$": "$",
            "FunctionName": "arn:aws:lambda:eu-west-2:590183970951:function:hyper-accelerated-dragon-lambda-transform:$LATEST"
        },
        "Retry": [
        {
          "ErrorEquals": [
            "Lambda.ServiceException",
            "Lambda.AWSLambdaException",
            "Lambda.SdkClientException",
            "Lambda.TooManyRequestsException"
          ],
          "IntervalSeconds": 1,
          "MaxAttempts": 3,
          "BackoffRate": 2
        }
        ],
        "Next": "Invoke LOAD Lambda"
        },
        "Invoke LOAD Lambda": {
        "Type": "Task",
        "Resource": "arn:aws:states:::lambda:invoke",
        "OutputPath": "$.Payload",
        "Parameters": {
        "Payload.$": "$",
        "FunctionName": "arn:aws:lambda:eu-west-2:590183970951:function:hyper-accelerated-dragon-lambda-load:$LATEST"
        },
        "Retry": [
        {
          "ErrorEquals": [
            "Lambda.ServiceException",
            "Lambda.AWSLambdaException",
            "Lambda.SdkClientException",
            "Lambda.TooManyRequestsException"
          ],
          "IntervalSeconds": 1,
          "MaxAttempts": 3,
          "BackoffRate": 2
            }
            ],
            "End": true
            }
        }
    }
    EOF

    logging_configuration {
    log_destination        = "${aws_cloudwatch_log_group.state_machine_log_group.arn}:*"
    include_execution_data = true
    level                  = "ALL"
  }
}