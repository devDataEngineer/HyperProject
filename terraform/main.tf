
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }


    backend "s3" {
    bucket         	   = "team-hyper-accelerated-dragon-tf-state-bucket"
    key                = "state/terraform.tfstate"
    region         	   = "eu-west-2"
  }
}

 
 provider "aws" {
        region = "eu-west-2"

    default_tags  {

        tags =  {
        ProjectName = "Team Hyper Accelerated Dragon"
        Repo = "HyperProject"
        DeployedFrom = "Terraform"
        Environment  = "dev"

        }
    }
    
  } 

  data "aws_caller_identity" "current" {}

  data "aws_region" "current" {}

   





