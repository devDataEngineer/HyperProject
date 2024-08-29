#  making .zip file of lambda python code and store in terraform file
data "archive_file" "extract_layer" {
  type        = "zip"
  source_dir  = "${path.module}/../src/extractlambda"
  output_path = "${path.module}/../src/lambda_function_payload.zip"
}

resource "aws_lambda_layer_version" "lambda-layer" {
  s3_bucket           = "team-hyper-accelerated-dragon-bucket-lambda-layer"
  s3_key              = "lambda-layer.zip"
  layer_name          = "lambda-layer"
  compatible_runtimes = [var.python_runtime]
}

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
  timeout = 300 
  # set the value to 5 minutes to be extra sure lambda does not fail
}

resource "aws_cloudwatch_log_group" "extract_lambda_cw_group"{
  name = "/aws/lambda/${var.lambda_name}-extract"
}


