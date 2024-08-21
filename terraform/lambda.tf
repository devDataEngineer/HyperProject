#  making .zip file of lambda python code and store in terraform file
data "archive_file" "extract_layer" {
  type        = "zip"
  source_dir = "${path.module}/../src/extractlambda"
  output_path = "${path.module}/../src/lambda_function_payload.zip"
}

resource "aws_lambda_layer_version" "extract-layer" {
  filename            = "${path.module}/../src/lambda-layer.zip"
  layer_name          = "extract-layer"
  compatible_runtimes = [var.python_runtime]
}

data "archive_file" "layer_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../src/lambda-layer"
  output_path = "${path.module}/../src/lambda-layer.zip"
}

resource "aws_lambda_function" "extract_lambda" {
  filename          = "${path.module}/../src/lambda_function_payload.zip"
  function_name     = "${var.lambda_name}-extract"
  role              = aws_iam_role.extract_lambda_role.arn
  # handler           = "${var.lambda_name}-extract.lambda_handler"
  handler           = "extract.lambda_handler"
  runtime           = var.python_runtime
  source_code_hash  = data.archive_file.extract_layer.output_base64sha256
  depends_on        = [aws_sns_topic.email_notification] # add environment below!
  environment {
    variables = {
      TOPIC_ARN = aws_sns_topic.email_notification.arn,
       # get sns topic arn and assing to env variable TOPIC_ARN
      SSMParameterName = var.ssm_parameter_name # sets SSM parameter name 
    }
  }
  layers = [
    aws_lambda_layer_version.extract-layer.arn
  ]
  timeout = 120
}

resource "aws_cloudwatch_log_group" "extract_lambda_cw_group"{
  name = "/aws/lambda/${var.lambda_name}-extract"
}

#  add permission to extract lambda function to call sns
resource "aws_lambda_permission" "sns_publish" {
    function_name = aws_lambda_function.extract_lambda.function_name
    statement_id  = "AllowSNSPublish"
    action        = "lambda:PublishMessage"
    principal     = "sns.amazonaws.com"
    source_arn    = aws_sns_topic.email_notification.arn
}

resource "aws_lambda_permission" "ssm_GetParameter" {
    function_name = aws_lambda_function.extract_lambda.function_name
    statement_id  = "A"
    action        = "lambda:PublishMessage"
    principal     = "sns.amazonaws.com"
    source_arn    = aws_sns_topic.email_notification.arn
}

#  add permission to extract lambda function to be called by aws cloud watch event rule
# resource "aws_lambda_permission" "allow_eventbridge" {
#   statement_id  = "AllowExecutionFromEventBridge"
#   action        = "lambda:InvokeFunction"
#   function_name = aws_lambda_function.extract_lambda.function_name
#   principal     = "events.amazonaws.com"
#   source_arn    = aws_cloudwatch_event_rule.every_5_minutes.arn
# }

# this bloc creates a deployment package or the layer
# data "archive_file" "transform-lambda" {
#   type             = "zip"
#   output_file_mode = "0666"
#   source_file      = "${path.module}/../src/......"
#   output_path      = "${path.module}/../function.zip"
# }


# resource "aws_lambda_function" "transform_lambda" {
#   function_name = "${var.lambda_name}-transform"
#   role = aws_iam_role.lambda_role.arn
#   }

  # handler = "${path.module}/../function.lambda_handler"
  # # connect the layer outlined above
  # runtime       = var.python_runtime
  #   }


# resource "aws_lambda_function" "load_lambda" {
#   function_name = "${var.lambda_name}-load"
#   role = # aws_iam_role.lambda_role.arn
#   #handler = "${path.module}/../function.lambda_handler"
#   # connect the layer outlined above
#   runtime       = var.python_runtime
#     }


# Commented out after confirming with Cris, because this was another trigger 
# for the Extract Lambda.Previous comment: add permission to transform lambda 
# function to be started by s3 bucket notification

# resource "aws_lambda_permission" "allow_bucket" {
#   statement_id  = "AllowExecutionFromS3Bucket"
#   action        = "lambda:InvokeFunction"
#   function_name = aws_lambda_function.extract_lambda.function_name
#   principal     = "s3.amazonaws.com"
#   source_arn    = aws_s3_bucket.ingestion-bucket.arn
# }




# ------------------TRANSFORM LAMBDA SNS and CW -------------------------------

# create a zip file of transform lambda funciton written in python
data "archive_file" "transform_layer" {
  type        = "zip"
  source_file = "${path.module}/../src/temp_transform_lambda.py"
  output_path = "${path.module}/../src/transform_lambda_function_payload.zip"
}

# transform lambda function 
resource "aws_lambda_function" "transform_lambda" {
  filename      = "${path.module}/../src/transform_lambda_function_payload.zip"
  function_name = "${var.lambda_name}-transform"
  role          = aws_iam_role.extract_lambda_role.arn
  # handler       = "${var.lambda_name}-extract.lambda_handler"
  handler = "temp_transform_lambda.lambda_handler"
  runtime       = var.python_runtime
  source_code_hash = data.archive_file.extract_layer.output_base64sha256
  depends_on    = [aws_sns_topic.email_notification] # add environment below!
  environment {
    variables = {
      TOPIC_ARN = aws_sns_topic.email_notification.arn # get sns topic arn and assing to env variable TOPIC_ARN
    }
  }
}

#  add permission to extract lambda function to be called by aws cloud watch event rule
resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.extract_lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.every_5_minutes.arn
}

#  add permission to transform lambda function to call sns
resource "aws_lambda_permission" "transform_sns_publish" {
    function_name = aws_lambda_function.transform_lambda.function_name
    statement_id  = "AllowSNSPublish"
    action        = "lambda:PublishMessage"
    principal     = "sns.amazonaws.com"
    source_arn    = aws_sns_topic.email_notification.arn
}
