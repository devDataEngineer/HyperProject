#  making .zip file of lambda python code and store in terraform file
data "archive_file" "extract_layer" {
  type        = "zip"
  source_dir = "${path.module}/../src/extractlambda"
  output_path = "${path.module}/../src/lambda_function_payload.zip"
}

resource "aws_lambda_layer_version" "lambda-layer" {
  filename            = "${path.module}/../src//lambda-layer/lambda-layer.zip"
  layer_name          = "lambda-layer"
  compatible_runtimes = [var.python_runtime]
}

# This resource was used to create a lambda layer zip file, but it was created
# manualy
# data "archive_file" "layer_zip" {
#   type        = "zip"
#   source_dir  = "${path.module}/../src/lambda-layer"
#   output_path = "${path.module}/../src/lambda-layer.zip"
#   output_file_mode = "0666"
# }

resource "aws_lambda_function" "extract_lambda" {
  filename          = "${path.module}/../src/lambda_function_payload.zip"
  function_name     = "${var.lambda_name}-extract"
  role              = aws_iam_role.extract_lambda_role.arn
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
  layers = [aws_lambda_layer_version.lambda-layer.arn]
  timeout = 180 
  # set the value to 3 minutes to be extra sure lambda does not fail
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

resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.extract_lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.every_5_minutes.arn
}