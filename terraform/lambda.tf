
data "archive_file" "layer" {
  type        = "zip"
  source_dir = "../src/lambda.py"
  output_path = "lambda_function_payload.zip"
}
resource "aws_lambda_layer_version" "layer_to_be_added" {
  layer_name          = ""
  compatible_runtimes = [var.python_runtime]
  s3_bucket           = aws_s3_bucket.code_bucket.bucket # CHANGE
  s3_key              = "${var.lambda_name}/layer.zip" # CHANGE
}

resource "aws_lambda_function" "extract_lambda" {
  filename = "lambda_function_payload.zip"
  function_name = "${var.lambda_name}-extract"
  role = aws_iam_role.extract_lambda_role.arn
  handler = "${var.lambda_name}-extract.lambda_handler"
  runtime       = var.python_runtime
  depends_on = [aws_sns_topic.email_notification ] # add environment below!
    }

# this bloc creates a deployment package or the layer
# data "archive_file" "extract-lambda" {
#   type             = "zip"
#   output_file_mode = "0666"
#   source_file      = "${path.module}/../src/......"
#   output_path      = "${path.module}/../function.zip"
# }



resource "aws_lambda_function" "transform_lambda" {
  function_name = "${var.lambda_name}-transform"
  role = # aws_iam_role.lambda_role.arn
  #handler = "${path.module}/../function.lambda_handler"
  # connect the layer outlined above
  runtime       = var.python_runtime
    }


resource "aws_lambda_function" "load_lambda" {
  function_name = "${var.lambda_name}-load"
  role = # aws_iam_role.lambda_role.arn
  #handler = "${path.module}/../function.lambda_handler"
  # connect the layer outlined above
  runtime       = var.python_runtime
    }




