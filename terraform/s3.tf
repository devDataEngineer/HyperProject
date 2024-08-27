
resource "aws_s3_bucket" "ingestion-bucket" {
   bucket = "${var.bucket_prefix}-ingestion"
   force_destroy = true
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

# Commented out after confirming with Cris, because this was another trigger 
# for the Extract Lambda

# resource "aws_s3_bucket_notification" "ingestion-bucket-notification" {
#   bucket = aws_s3_bucket.ingestion-bucket.id
#   eventbridge = true

#   lambda_function {
      
#     lambda_function_arn = aws_lambda_function.extract_lambda.arn # change to transform
#     events              = ["s3:ObjectCreated:*"]
#   }

#   depends_on = [aws_lambda_permission.allow_bucket]
#  }  

