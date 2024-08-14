
resource "aws_s3_bucket" "ingestion-bucket" {
   bucket = "${var.bucket_prefix}-ingestion"

    tags = {
        Name = "totesys ingested data bucket"
    
  }
}
# not relevant for the ingestion part
resource "aws_s3_bucket" "processed-bucket" {
  bucket = "${var.bucket_prefix}-processed"

    tags = {
        Name  = "processed data bucket for loading into warehouse"
    
  }
}
# incomplete
resource "aws_s3_bucket_notification" "ingestion-bucket-notification" {
  bucket = "aws_s3_bucket.${var.bucket_prefix}-ingestion".id
  eventbridge = true

#   lambda_function {
      name =
#     lambda_function_arn = aws_lambda_function.s3_file_reader.arn (destination) STARTS TRANSFORM LAMBA
#     events              = ["s3:ObjectCreated:*"]
#   }

#   depends_on = [aws_lambda_permission.allow_s3]
 }  

