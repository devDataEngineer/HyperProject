
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
  statement {  # this statment allow lambad to access scheduler 
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
  policy      = data.aws_iam_policy_document.json
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
    resources =  ["arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/${var.lambda_name}:*"] 
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




