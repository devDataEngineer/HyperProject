# create an email address for sending notification to
locals {
  emails = ["zabihullah4830@gmail.com"]
}

#  create aws sns topic
resource "aws_sns_topic" "email_notification" {
    name            = "email_notification"
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
resource "aws_sns_topic_subscription" "topic_email_subscription" {
  count     = length(local.emails)
  topic_arn = aws_sns_topic.email_notification.arn
  protocol  = "email"
  endpoint  = local.emails[count.index]
}


#  Attaches a policy to the SNS topic, allowing various SNS actions such as subscribing, publishing, and modifying topic attributes.
resource "aws_sns_topic_policy" "default" {
  arn = aws_sns_topic.email_notification.arn
  policy = data.aws_iam_policy_document.sns_topic_policy.json

}
# Defines the policy document that specifies the permissions for the SNS topic. It allows our lambda to perform SNS actions on the topic.
data "aws_iam_policy_document" "sns_topic_policy" {
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
        identifiers = [aws_iam_role.extract_lambda_role.arn]
        }

        resources = [
        aws_sns_topic.email_notification.arn
        ]
        sid = "__default_statement_ID"
    }
}

#  add permission to extract lambda function to call sns
resource "aws_lambda_permission" "sns_publish" {
    function_name = aws_lambda_function.extract_lambda.function_name
    statement_id  = "AllowSNSPublish"
    action        = "lambda:PublishMessage"
    principal     = "sns.amazonaws.com"
    source_arn    = aws_sns_topic.email_notification.arn
}
#  add permission to transform lambda function to call sns
resource "aws_lambda_permission" "transform_sns_publish" {
    function_name = aws_lambda_function.transform_lambda.function_name
    statement_id  = "AllowSNSPublish"
    action        = "lambda:PublishMessage"
    principal     = "sns.amazonaws.com"
    source_arn    = aws_sns_topic.email_notification_transform_lambda.arn
}

#  add permission to load lambda function to call sns
resource "aws_lambda_permission" "load_sns_publish" {
    function_name = aws_lambda_function.load_lambda.function_name
    statement_id  = "AllowSNSPublish"
    action        = "lambda:PublishMessage"
    principal     = "sns.amazonaws.com"
    source_arn    = aws_sns_topic.email_notification_load_lambda.arn
}


################################################################################
# SNS (email) configuration for the transform lambda
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

################################################################################
# SNS (email) configuration for the load lambda
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