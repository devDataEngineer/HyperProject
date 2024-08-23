#  making .zip file of transform lambda python code and store in terraform file
data "archive_file" "transform_layer" {
  type             = "zip"
  source_file       = "${path.module}/../src/transform.py"
  output_path      = "${path.module}/../src/transform_lambda_func_payload.zip"
}

resource "aws_lambda_layer_version" "transform-layer" {
  filename      = "${path.module}/../src/transform-lambda-layer.zip" 
  layer_name    = "transform_lambda_layer"
  compatible_runtimes = [var.python_runtime]
}

#  making .zip file of transform lambda python code and store in terraform file
data "archive_file" "transform_layer_zip" {
  type        = "zip"
  source_dir = "${path.module}/../src/transform-lambda-layer"
  output_path = "${path.module}/../src/transform-lambda-layer.zip"
}


resource "aws_lambda_function" "transform_lambda" {
  filename          = "${path.module}/../src/transform_lambda_func_payload.zip" 
  function_name     = "${var.lambda_name}-transform"
  role              = aws_iam_role.iam_for_transform_lambda.arn
  handler           = "transform.lambda_handler"
  runtime           = var.python_runtime
  source_code_hash  = data.archive_file.transform_layer.output_base64sha256
  layers            = [aws_lambda_layer_version.transform-layer.arn]
  depends_on        = [aws_sns_topic.email_notification_transform_lambda]
  environment {
    variables   = {
      TOPIC_ARN = aws_sns_topic.email_notification_transform_lambda.arn,
       # get sns topic arn and assing to env variable TOPIC_ARN
      SSMParameterName = var.ssm_parameter_name # sets SSM parameter name 
    }
  }
  timeout = 120 
}

resource "aws_cloudwatch_log_group" "transform_lambda_cw_group"{
  name = "/aws/lambda/${var.lambda_name}-transform"
}

#  add permission to transform lambda function to call sns
resource "aws_lambda_permission" "transform_sns_publish" {
    function_name = aws_lambda_function.transform_lambda.function_name
    statement_id  = "AllowSNSPublish"
    action        = "lambda:PublishMessage"
    principal     = "sns.amazonaws.com"
    source_arn    = aws_sns_topic.email_notification_transform_lambda.arn
}



data "aws_iam_policy_document" "transform_lambda_trust_policy" {
statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
  statement {  # this statment allow lambda to access scheduler, potentailly not needed anymore
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["scheduler.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}


resource "aws_iam_role" "iam_for_transform_lambda" {
  name_prefix        = "iam_for_transform_lambda"
  assume_role_policy = data.aws_iam_policy_document.transform_lambda_trust_policy.json
}

data "aws_iam_policy_document" "s3_data_policy_transform_lambda" {
  statement {
    #this statement should give permission to put objects in the data bucket
    actions = [
        "s3:PutObject",
        "s3:GetObject",
        "s3:ListBucket"
    ]
    resources = [
      "${aws_s3_bucket.ingestion-bucket.arn}/*",
      "${aws_s3_bucket.processed-bucket.arn}/*"
       ]
  }
}

resource "aws_iam_policy" "transform_s3_policy" {
  name_prefix = "s3-policy-transform-lambda"
  policy      = data.aws_iam_policy_document.s3_data_policy_transform_lambda.json
}

resource "aws_iam_role_policy_attachment" "transform_lambda_s3_policy_attachment" {
    #TODO: attach the s3 write policy to the lambda role
    role = aws_iam_role.iam_for_transform_lambda.name
    policy_arn = aws_iam_policy.transform_s3_policy.arn
}

# transform Lambda IAM Policy for CloudWatch 
data "aws_iam_policy_document" "transform_cw_document" {
  statement {
    actions = ["logs:CreateLogGroup"]
    resources = ["arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:*"] 
  }
  statement {
    actions = ["logs:CreateLogStream",
               "logs:PutLogEvents"]
    resources =  ["arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/${var.lambda_name}-transform:*"] 
  }
}
resource "aws_iam_policy" "transform_cw_policy" {
  name_prefix = "cw-policy-transform-lambda"
  policy      = data.aws_iam_policy_document.transform_cw_document.json
}
resource "aws_iam_role_policy_attachment" "transform_lambda_cw_policy_attachment" {
  role       = aws_iam_role.iam_for_transform_lambda.name
  policy_arn = aws_iam_policy.transform_cw_policy.arn

}



# resource "aws_s3_bucket" "processed-bucket" {
#   bucket = "${var.bucket_prefix}-processed"

#     tags = {
#         Name  = "processed data bucket for loading into warehouse"
    
#   }
# }

# resource "aws_s3_bucket_notification" "processed-bucket-notification" {
#   bucket = aws_s3_bucket.processed-bucket.id
#   eventbridge = true

#   lambda_function {
      
#     lambda_function_arn = aws_lambda_function.transform_lambda.arn # change to transform
#     events              = ["s3:ObjectCreated:*"]
#   }

#   depends_on = [aws_lambda_permission.allow_bucket]
#  }  #are we still using this?

 # Transform Lambda IAM Policy for S3 Write - I am assuming this
 # will at some point be needed to add to the processed bucket?



################################################################################
# SNS (email) configuration for the second lambda
################################################################################

# Change this to parameter store
locals {
  transform_emails = ["oleh.fylypiv1@gmail.com"] 
}

#  create aws sns topic
resource "aws_sns_topic" "email_notification_transform_lambda" {
    name            = "transform_lambda_notification"
    delivery_policy = jsonencode({
        "http" : {
        "defaultHealthyRetryPolicy" : {
            "minDelayTarget" : 20,
            "maxDelayTarget" : 20,
            "numRetries" : 3,
            "numMaxDelayRetries" : 0,
            "numNoDelayRetries" : 0,
            "numMinDelayRetries" : 0,
            "backoffFunction" : "linear"
        },
        "disableSubscriptionOverrides" : false,
        "defaultThrottlePolicy" : {
            "maxReceivesPerSecond" : 1
        }
        }
    })
}

#  create sns topic subscription of an email to send notification to 
resource "aws_sns_topic_subscription" "topic_email_subscr_transform_lambda" {
  count     = length(local.transform_emails)
  topic_arn = aws_sns_topic.email_notification_transform_lambda.arn
  protocol  = "email"
  endpoint  = local.transform_emails[count.index]
}


#  Attaches a policy to the SNS topic, allowing various SNS actions such as subscribing, publishing, and modifying topic attributes.
resource "aws_sns_topic_policy" "transform_lambda_policy_attachment" {
  arn = aws_sns_topic.email_notification_transform_lambda.arn
  policy = data.aws_iam_policy_document.sns_topic_policy_transform_lambda.json

}
# Defines the policy document that specifies the permissions for the SNS topic. It allows our lambda to perform SNS actions on the topic.
data "aws_iam_policy_document" "sns_topic_policy_transform_lambda" {
    policy_id = "__default_policy_ID"

    statement {
        actions = [
      "SNS:Subscribe",
      "SNS:SetTopicAttributes",
      "SNS:RemovePermission",
      "SNS:Receive",
      "SNS:Publish",
      "SNS:ListSubscriptionsByTopic",
      "SNS:GetTopicAttributes",
      "SNS:DeleteTopic",
      "SNS:AddPermission",
    ]

        effect = "Allow"

        principals {
        type        = "AWS"
        identifiers = [aws_iam_role.iam_for_transform_lambda.arn]
        }

        resources = [
        aws_sns_topic.email_notification_transform_lambda.arn
        ]
        sid = "__default_statement_ID"
    }
}