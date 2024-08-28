# Lambda IAM Role
data "aws_iam_policy_document" "extract_lambda_trust_policy" {
statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
  statement {  # this statment allow lambda to access scheduler 
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["scheduler.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}


resource "aws_iam_role" "extract_lambda_role" {
  name_prefix        = "role-${var.lambda_name}"
  assume_role_policy = data.aws_iam_policy_document.extract_lambda_trust_policy.json
}

# extract Lambda IAM Policy for S3 Write

data "aws_iam_policy_document" "s3_data_policy_doc" {
  statement {
    #this statement should give permission to put objects in the data bucket
    actions = ["s3:PutObject"]

    resources = [
      "${aws_s3_bucket.ingestion-bucket.arn}/*"
       ]
  }
}

resource "aws_iam_policy" "s3_write_policy" {
  name_prefix = "s3-policy-extract-lambda-write"
  policy      = data.aws_iam_policy_document.s3_data_policy_doc.json
}


resource "aws_iam_role_policy_attachment" "lambda_s3_write_policy_attachment" {
    #TODO: attach the s3 write policy to the lambda role
    role = aws_iam_role.extract_lambda_role.name
    policy_arn = aws_iam_policy.s3_write_policy.arn
}

# extract Lambda IAM Policy for CloudWatch incomplete
data "aws_iam_policy_document" "cw_document" {
  statement {
    actions = ["logs:CreateLogGroup"]
    resources = ["arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:*"] 
  }
  statement {
    actions = ["logs:CreateLogStream",
               "logs:PutLogEvents"]
    resources =  ["arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/${var.lambda_name}-extract:*"] 
  }
}
resource "aws_iam_policy" "cw_policy" {
  name_prefix = "cw-policy-extract-lambda-write"
  policy      = data.aws_iam_policy_document.cw_document.json
}
resource "aws_iam_role_policy_attachment" "lambda_cw_policy_attachment" {
  role       = aws_iam_role.extract_lambda_role.name
  policy_arn = aws_iam_policy.cw_policy.arn

}

data "aws_iam_policy_document" "ssm_document" {
  statement {
    actions = [
      "ssm:GetParameter",
      "ssm:PutParameter"
    ]
    resources = [aws_ssm_parameter.ssm_parameter.arn]
  }
}
resource "aws_iam_policy" "ssm_policy" {
  name_prefix = "sm-policy-extract-lambda"
  policy      = data.aws_iam_policy_document.ssm_document.json
}
resource "aws_iam_role_policy_attachment" "lambda_ssm_policy_attachment" {
  role       = aws_iam_role.extract_lambda_role.name
  policy_arn = aws_iam_policy.ssm_policy.arn

}

data "aws_iam_policy_document" "secret_manager_document" {
	statement {
		actions = ["secretsmanager:GetSecretValue"]
    resources = ["arn:aws:secretsmanager:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:secret:*"]	
		}
}
resource "aws_iam_policy" "secret_manager_policy" {
  name_prefix = "secret-manager-policy-extract-lambda"
  policy      = data.aws_iam_policy_document.secret_manager_document.json
}
resource "aws_iam_role_policy_attachment" "secret_manager_policy_attachment" {
  role       = aws_iam_role.extract_lambda_role.name
  policy_arn = aws_iam_policy.secret_manager_policy.arn

}

# Create new IAM Policy and Role for EventBridge Scheduler
resource "aws_iam_policy" "eventbridge_stepfunctions_policy" {
  name        = "eventbridge_stepfunctions_policy"
  description = "Policy for EventBridge Scheduler to trigger Step Functions"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "states:StartExecution"
        ],
        Effect   = "Allow"
        Resource = "${aws_sfn_state_machine.step_function_state_machine.arn}"
      }
    ]
  })
}

resource "aws_iam_role" "eventbridge_scheduler_iam_role" {
  name_prefix         = "eb-scheduler-role-"
  managed_policy_arns = [aws_iam_policy.eventbridge_stepfunctions_policy.arn]
  path = "/"
  assume_role_policy  = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "scheduler.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
EOF
}

# Create new IAM Policy and Role for Step Function 

resource "aws_iam_role" "sfn_iam_role" {
  name = "sfn-iam-role"
  managed_policy_arns = ["arn:aws:iam::aws:policy/AWSStepFunctionsFullAccess"]
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "states.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}



