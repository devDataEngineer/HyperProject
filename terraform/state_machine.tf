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
  
# IAM role for Step Functions state machine
resource "aws_iam_role" "state_machine_role" {
name              = "StepFunctions-Terraform-Role" # CHANGE
assume_role_policy = <<EOF
{
"Version" : "2012-10-17",
"Statement" : [
    {
    "Effect" : "Allow",
    "Principal" : {
        "Service" : "states.amazonaws.com"
    },
    "Action" : "sts:AssumeRole"
        },
    {
    "Effect" : "Allow",
    "Principal" : {
        "Service" : "scheduler.amazonaws.com"
    },
    "Action" : "sts:AssumeRole"
        }]
    }
    EOF
}

# IAM policy for Step Functions state machine - covers access to all resources invoked or used by the step function
resource "aws_iam_role_policy" "state_machine_policy" {
role   = aws_iam_role.state_machine_role.id
policy = <<EOF
{
"Version" : "2012-10-17",
"Statement" : [
    {
    "Effect" : "Allow",
    "Action" : [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents",
        "logs:CreateLogDelivery",
        "logs:GetLogDelivery",
        "logs:UpdateLogDelivery",
        "logs:DeleteLogDelivery",
        "logs:ListLogDeliveries",
        "logs:PutResourcePolicy",
        "logs:DescribeResourcePolicies",
        "logs:DescribeLogGroups",
        "cloudwatch:PutMetricData",
        "lambda:InvokeFunction",

        "cloudwatch:CreateLogDelivery",
        "cloudwatch:GetLogDelivery",
        "cloudwatch:UpdateLogDelivery",
        "cloudwatch:DeleteLogDelivery",
        "cloudwatch:ListLogDeliveries",
        "cloudwatch:PutResourcePolicy",
        "cloudwatch:DescribeResourcePolicies",
        "cloudwatch:DescribeLogGroups",
        
        "xray:PutTraceSegments",
        "xray:PutTelemetryRecords",
        "xray:GetSamplingRules",
        "xray:DescribeLogGroups"
    ],
    "Resource" : "*" 
    }]
    }
    EOF
}


# SUGGESTED DIRECTORY/FILE SET_UP

# src (DIR)
# stepfunctions-tf (DIR)> 
#     main.tf (exists)
#     outputs.tf
#     variables.tf (exists)



# statemachines (DIR) > statemachines/statemachine.asl.json
    # This is where the orchestration logic will reside, so best to keep it separated from the infrastructure code
    #  holds our Amazon States Language (ASL) JSON code describing the Step Functions state machine definition


# Edit the file statemachines/statemachine.asl.json, and add the following code:
# {
#   "Comment": "A description of my state machine",
#   "StartAt": "Invoke EXTRACT lambda",
#   "States": {
#     "Invoke EXTRACT lambda": {
#       "Type": "Task",
#       "Resource": "arn:aws:states:::lambda:invoke",
#       "OutputPath": "$.Payload",
#       "Parameters": {
#         "Payload.$": "$",
#         "FunctionName": "arn:aws:lambda:eu-west-2:590183970951:function:hyper-accelerated-dragon-lambda-extract:$LATEST"
#       },
#       "Next": "Invoke TRANSFORM Lambda"
#     },
#     "Invoke TRANSFORM Lambda": {
#       "Type": "Task",
#       "Resource": "arn:aws:states:::lambda:invoke",
#       "OutputPath": "$.Payload",
#       "Parameters": {
#         "Payload.$": "$",
#         "FunctionName": "arn:aws:lambda:eu-west-2:590183970951:function:hyper-accelerated-dragon-lambda-transform:$LATEST"
#       },
#       "Retry": [
#         {
#           "ErrorEquals": [
#             "Lambda.ServiceException",
#             "Lambda.AWSLambdaException",
#             "Lambda.SdkClientException",
#             "Lambda.TooManyRequestsException"
#           ],
#           "IntervalSeconds": 1,
#           "MaxAttempts": 3,
#           "BackoffRate": 2
#         }
#       ],
#       "Next": "Invoke LOAD Lambda"
#     },
#     "Invoke LOAD Lambda": {
#       "Type": "Task",
#       "Resource": "arn:aws:states:::lambda:invoke",
#       "OutputPath": "$.Payload",
#       "Parameters": {
#         "Payload.$": "$",
#         "FunctionName": "arn:aws:lambda:eu-west-2:590183970951:function:hyper-accelerated-dragon-lambda-load:$LATEST"
#       },
#       "Retry": [
#         {
#           "ErrorEquals": [
#             "Lambda.ServiceException",
#             "Lambda.AWSLambdaException",
#             "Lambda.SdkClientException",
#             "Lambda.TooManyRequestsException"
#           ],
#           "IntervalSeconds": 1,
#           "MaxAttempts": 3,
#           "BackoffRate": 2
#         }
#       ],
#       "End": true
#     }
#   }
# }


# # State machine definition file with the variables to replace
# Points to exported definition JSON file with variables to replace (must parameterise these)
# data "template_file" "state_machine_definition_file" {
#     template = file("statemachines/statemachine.asl.json") # OR "${path.module}/definition_name.json"
#     vars = {
#         LambdaFunction  = aws_lambda_function.test_lambda.arn # CHANGE          
#     }
# }

# Create AWS Step Functions state machine
# resource "aws_sfn_state_machine" "step_function_state_machine" {
#     name_prefix = vars.state_machine_name # Add to vars
#     definition    = data.template_file.state_machine_definition_file.rendered
#     type          = "EXPRESS" # N.B. The logging_configuration parameter is only valid when type is set to EXPRESS
#     role_arn      = aws_iam_role.state_machine_role.arn
#     # Example from docs for logging:
#     logging_configuration {
#     log_destination        = "${aws_cloudwatch_log_group.state_function_log_group.arn}:*"
#     include_execution_data = true
#     level                  = "ALL"
#   }
# }

# May need a policy for writing to Cloudwatch logs


# resource "aws_cloudwatch_event_target" "state_machine_target" {
#     rule        = aws_cloudwatch_event_rule.state_machine_trigger.name
#     arn         = aws_sfn_state_machine.step_function_state_machine.arn
#     role_arn    = aws_iam_role.eventbridge_rule_role.TOPIC_ARN
# }

# resource "aws_iam_role_policy_attachment" "step_function_role_attachment" {
#   role       = aws_iam_role.sfn_iam_role.name
#   policy_arn = "arn:aws:iam::aws:policy/service-role/AWSStepFunctionsFullAccess"
# }

# Create new Step Function State Machine
# resource "aws_sfn_state_machine" "sfn_state_machine" {
#   name     = "my-state-machine"
#   role_arn = aws_iam_role.sfn_iam_role.arn

#   definition = <<EOF
# {
#   "Comment": "A Hello World example of the Amazon States Language",
#   "StartAt": "HelloWorld",
#   "States": {
#     "HelloWorld": {
#       "Type": "Pass",
#       "End": true
#     }
#   }
# }
# EOF
# }


