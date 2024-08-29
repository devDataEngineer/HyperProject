#  making .zip file of transform lambda python code and store in terraform file
data "archive_file" "transform_layer" {
  type             = "zip"
  source_dir       = "${path.module}/../src/transformlambda"
  output_path      = "${path.module}/../src/transform_lambda_func_payload.zip"
}



resource "aws_lambda_function" "transform_lambda" {
  filename          = "${path.module}/../src/transform_lambda_func_payload.zip" 
  function_name     = "${var.lambda_name}-transform"
  role              = aws_iam_role.iam_for_transform_lambda.arn
  handler           = "transform.lambda_handler"
  runtime           = var.python_runtime
  source_code_hash  = data.archive_file.transform_layer.output_base64sha256
  layers            = [aws_lambda_layer_version.lambda-layer.arn]
  depends_on        = [aws_sns_topic.email_notification_transform_lambda]
  environment {
    variables   = {
      TOPIC_ARN = aws_sns_topic.email_notification_transform_lambda.arn,
       # get sns topic arn and assing to env variable TOPIC_ARN
    }
  }
  timeout = 180
  memory_size = 256
}

resource "aws_cloudwatch_log_group" "transform_lambda_cw_group"{
  name = "/aws/lambda/${var.lambda_name}-transform"
}