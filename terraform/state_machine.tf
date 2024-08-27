
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
{
    "Comment": "A description of my state machine",
    "StartAt": "Lambda Invoke",
    "States": {
        "Lambda Invoke": {
        "Type": "Task",
        "Resource": "arn:aws:states:::lambda:invoke",
        "OutputPath": "$.Payload",
        "Parameters": {
            "Payload.$": "$",
            "FunctionName": "${LambdaFunction}"
        },
        "End": true
        }
    }
}


# # State machine definition file with the variables to replace
# Points to exported definition JSON file with variables to replace (must parameterise these)
data "template_file" "state_machine_definition_file" {
    template = file("statemachines/statemachine.asl.json") # OR "${path.module}/definition_name.json"
    vars = {
        LambdaFunction  = aws_lambda_function.test_lambda.arn # CHANGE          
    }
}

# Create AWS Step Functions state machine
resource "aws_sfn_state_machine" "step_function_state_machine" {
    name_prefix = var.state_machine_name # Add to vars
    definition    = data.template_file.state_machine_definition_file.rendered
    type          = "EXPRESS" # N.B. The logging_configuration parameter is only valid when type is set to EXPRESS
    role_arn      = aws_iam_role.state_machine_role.arn
    # Example from docs for logging:
    logging_configuration {
    log_destination        = "${aws_cloudwatch_log_group.state_function_log_group.arn}:*"
    include_execution_data = true
    level                  = "ALL"
  }
}

# EXAMPLE FROM LECTURE FOR REFERENCE

# resource "aws_sfn_state_machine" "step_function_state_machine" {
#     name_prefix = var.bucket_prefix 
#     definition = templatefile("${path.module}/..pipeline/pipeline.json",
#     {   special_file_name  = var.special_file,
#         aws_region          = data.aws_region.current.name,
#         aws_account_num     = data.aws_caller_identity.current.account_id, 
#         counter_lambda_     = var.lambda_counter,
#         reader_lambda       = var.lambda_reader,
#     double_lambda = var.lambda_double }) 
#     role_arn      = aws_iam_role.step_function_role.arn 
# }


# IAM role for Step Functions state machine
resource "aws_iam_role" "state_machine_role" {
name              = "StepFunctions-Terraform-Role-${random_string.random.id}" # CHANGE
assume_role_policy = 
{
"Version" : "2012-10-17",
"Statement" : [
    {
    "Effect" : "Allow",
    "Principal" : {
        "Service" : "states.amazonaws.com"
    },
    "Action" : "sts:AssumeRole"
        }]
    }
}

data "aws_iam_policy_document" "state_machine_role_policy" {
  statement {
    effect = "Allow"
    actions = [
      "lambda:InvokeFunction"
    ]
    resources = ["${aws_lambda_function.[[myFunction]].arn}:*"] # this example would grant your state machine access to invoke 'myFunction'
  }
}

# IAM policy for Step Functions state machine - covers access to all resources invoked or used by the step function
resource "aws_iam_role_policy" "state_machine_policy" {
role   = aws_iam_role.state_machine_role.id
policy = {
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
    "Resource" : "*" #  ["${aws_lambda_function.[[myFunction]].arn}:*"] # example grants your state machine access to invoke 'myFunction'
    }]
    }
}

# May need a policy for writing to Cloudwatch logs
resource "aws_cloudwatch_log_group" "state_machine_log_group" {
    name_prefix = "/aws/vendedlogs/states/demo-state-machine-" # CHANGE
    retention_in_days = 1 # CHANGE?
    }


# To start the execution of a state machine from a schedule
resource "aws_cloudwatch_event_rule" "state_machine_trigger" {
    name_prefix = "trigger-${var.state_machine_name}"
    event_pattern    = jsonencode({
        source       = ["aws.s3"], # CHANGE
        detail-type  = ["Object Created"], # CHANGE
        detail = {
            bucket   = {
                name = ["${aws_s3_bucket.data_bucket.id}"] # CHANGE
            }
        }
    })
}
# Select the service (the particular step function) you wish to start (JM)
resource "aws_cloudwatch_event_target" "state_machine_target" {
    rule = aws_cloudwatch_event_rule.state_machine_trigger.name
    arn = aws_sfn_state_machine.step_function_state_machine.arn
    role_arn = aws_iam_role.eventbridge_rule_role.TOPIC_ARN
}

