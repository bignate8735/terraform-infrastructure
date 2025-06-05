terraform {
  backend "s3" {
    bucket         = "my-terraform-backend-010"
    key            = "terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks-dev"
    encrypt        = true
  }
}