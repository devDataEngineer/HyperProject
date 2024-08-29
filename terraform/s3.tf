
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

