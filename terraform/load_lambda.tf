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
  timeout = 120 
}

resource "aws_cloudwatch_log_group" "load_lambda_cw_group"{
  name = "/aws/lambda/${var.lambda_name}-load"
}

#  add permission to load lambda function to call sns
resource "aws_lambda_permission" "load_sns_publish" {
    function_name = aws_lambda_function.load_lambda.function_name
    statement_id  = "AllowSNSPublish"
    action        = "lambda:PublishMessage"
    principal     = "sns.amazonaws.com"
    source_arn    = aws_sns_topic.email_notification_load_lambda.arn
}

data "aws_iam_policy_document" "load_lambda_trust_policy" {
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


resource "aws_iam_role" "iam_for_load_lambda" {
  name_prefix        = "iam_for_load_lambda"
  assume_role_policy = data.aws_iam_policy_document.load_lambda_trust_policy.json
}

data "aws_iam_policy_document" "s3_data_policy_load_lambda" {
  statement {
    #this statement should give permission to put objects in the data bucket
    actions = [
        "s3:GetObject",
        "s3:ListBucket"
    ]
    resources = ["${aws_s3_bucket.processed-bucket.arn}/*"]
  }
}

resource "aws_iam_policy" "load_s3_policy" {
  name_prefix = "s3-policy-load-lambda"
  policy      = data.aws_iam_policy_document.s3_data_policy_load_lambda.json
}

resource "aws_iam_role_policy_attachment" "load_lambda_s3_policy_attachment" {
    role = aws_iam_role.iam_for_load_lambda.name
    policy_arn = aws_iam_policy.load_s3_policy.arn
}

# Load Lambda IAM Policy for CloudWatch 
data "aws_iam_policy_document" "load_cw_document" {
  statement {
    actions = ["logs:CreateLogGroup"]
    resources = ["arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:*"] 
  }
  statement {
    actions = ["logs:CreateLogStream",
               "logs:PutLogEvents"]
    resources =  ["arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/${var.lambda_name}-load:*"] 
  }
}
resource "aws_iam_policy" "load_cw_policy" {
  name_prefix = "cw-policy-load-lambda"
  policy      = data.aws_iam_policy_document.load_cw_document.json
}
resource "aws_iam_role_policy_attachment" "load_lambda_cw_policy_attachment" {
  role       = aws_iam_role.iam_for_load_lambda.name
  policy_arn = aws_iam_policy.load_cw_policy.arn

}

################################################################################
# SNS (email) configuration for the third lambda
################################################################################

# Change this to parameter store
locals {
  load_emails = ["oleh.fylypiv1@gmail.com"] 
}

#  create aws sns topic
resource "aws_sns_topic" "email_notification_load_lambda" {
    name            = "load_lambda_notification"
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
resource "aws_sns_topic_subscription" "topic_email_subscr_load_lambda" {
  count     = length(local.load_emails)
  topic_arn = aws_sns_topic.email_notification_load_lambda.arn
  protocol  = "email"
  endpoint  = local.load_emails[count.index]
}


#  Attaches a policy to the SNS topic, allowing various SNS actions such as subscribing, publishing, and modifying topic attributes.
resource "aws_sns_topic_policy" "load_lambda_policy_attachment" {
  arn = aws_sns_topic.email_notification_load_lambda.arn
  policy = data.aws_iam_policy_document.sns_topic_policy_load_lambda.json

}
# Defines the policy document that specifies the permissions for the SNS topic. It allows our lambda to perform SNS actions on the topic.
data "aws_iam_policy_document" "sns_topic_policy_load_lambda" {
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
        identifiers = [aws_iam_role.iam_for_load_lambda.arn]
        }

        resources = [
        aws_sns_topic.email_notification_load_lambda.arn
        ]
        sid = "__default_statement_ID"
    }
}

data "aws_iam_policy_document" "load_lambda_secret_manager_document" {
	statement {
		actions = ["secretsmanager:GetSecretValue"]
    resources = ["arn:aws:secretsmanager:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:secret:Data_Warehouse_Creds*"]	
		}
}
resource "aws_iam_policy" "load_lambda_secret_manager_policy" {
  name_prefix = "secret-manager-policy-load-lambda"
  policy      = data.aws_iam_policy_document.load_lambda_secret_manager_document.json
}
resource "aws_iam_role_policy_attachment" "load_lambda_sm_policy_attachment" {
  role       = aws_iam_role.iam_for_load_lambda.name
  policy_arn = aws_iam_policy.load_lambda_secret_manager_policy.arn

}

resource "aws_iam_role_policy_attachment" "load_lambda_ssm_policy_attachment" {
  role       = aws_iam_role.iam_for_load_lambda.name
  policy_arn = aws_iam_policy.ssm_policy.arn

}


# Possibly not needed anymore because we are going to be using PG8000
# data "aws_iam_policy_document" "rds_policy_load_lambda" {
#   statement {
#     #this statement should give permission to Warehouse RDS
#     actions = [
#         "rds:ModifyDBInstance",
#         "rds:DeleteDBInstance",
#         "rds-data:ExecuteSql",
#         "rds-data:ExecuteStatement",
#         "rds-data:BatchExecuteStatement",
#         "rds:Describe*"
#     ]
#     resources = [
#     #   "${aws_RDS_.warehouse.arn}/*"
#        ]
#   }
# }


# resource "aws_iam_policy" "rds_policy_load_lambda" {
#   name_prefix = "cw-policy-load-lambda"
#   policy      = data.aws_iam_policy_document.rds_policy_load_lambda.json
# }
# resource "aws_iam_role_policy_attachment" "load_lambda_rds_policy_attachment" {
#   role       = aws_iam_role.iam_for_load_lambda.name
#   policy_arn = aws_iam_policy.rds_policy_load_lambda.arn

# }

# # RDS policy document
# # RDS policy attachment
# # RDS policy role
# # 
# # Action for ModifyDBInstance:

# # "Action":[
# #             "rds:ModifyDBInstance"
# #          ],

# # Action for DenyDelete:
# # "Action": "rds:DeleteDBInstance",

# "rds-data:ExecuteSql",
# "rds-data:ExecuteStatement",
#  "rds-data:BatchExecuteStatement",
# "rds-data:BeginTransaction",
# "rds-data:CommitTransaction",
#  "rds-data:RollbackTransaction"