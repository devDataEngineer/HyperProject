#  making .zip file of load lambda python code and store in terraform file
data "archive_file" "load_layer" {
  type             = "zip"
  source_dir       = "${path.module}/../src/loadlambda"
  output_path      = "${path.module}/../src/load_lambda_func_payload.zip"
}

resource "aws_lambda_function" "load_lambda" {
  filename          = "${path.module}/../src/load_lambda_func_payload.zip" 
  function_name     = "${var.lambda_name}-load"
  role              = aws_iam_role.iam_for_load_lambda.arn
  handler           = "load.lambda_handler"
  runtime           = var.python_runtime
  source_code_hash  = data.archive_file.load_layer.output_base64sha256
  layers            = [aws_lambda_layer_version.lambda-layer.arn]
  depends_on        = [aws_sns_topic.email_notification_load_lambda]
  environment {
    variables   = {
      TOPIC_ARN = aws_sns_topic.email_notification_load_lambda.arn
       # get sns topic arn and assing to env variable TOPIC_ARN 
    }
  }
  timeout = 900 
}

resource "aws_cloudwatch_log_group" "load_lambda_cw_group"{
  name = "/aws/lambda/${var.lambda_name}-load"
}