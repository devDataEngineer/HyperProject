
resource "aws_s3_bucket" "ingestion-bucket" {
   bucket = "${var.bucket_prefix}-ingestion"

    tags = {
        Name = "totesys ingested data bucket"
    
  }
}

resource "aws_s3_bucket" "processed-bucket" {
  bucket = "${var.bucket_prefix}-processed"

    tags = {
        Name  = "processed data bucket for loading into warehouse"
    
  }
}

resource "aws_s3_bucket" "lambda-code-bucket" {
  bucket = "${var.bucket_prefix}-lambda-code"

    tags = {
        Name  = "lambda code bucket to upload python files to be used as lambda functions"
    
  }
}

resource "aws_s3_bucket_notification" "ingestion-bucket-notification" {
  bucket = aws_s3_bucket.ingestion-bucket.id
  eventbridge = true

  lambda_function {
      
    lambda_function_arn = aws_lambda_function.extract_lambda.arn
    events              = ["s3:ObjectCreated:*"]
  }

  depends_on = [aws_lambda_permission.allow_s3]
 }  

