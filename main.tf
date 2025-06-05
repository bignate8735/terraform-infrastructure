terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}


# VPC Module
module "vpc" {
  source = "./modules/vpc"
}

# Security Groups Module
module "security_groups" {
  source = "./modules/security_groups"
  vpc_id = module.vpc.vpc_id
  #vpc_id  = aws_vpc.main.id  # Pass the VPC ID from the VPC module
}

module "ec2" {
  source = "./modules/ec2"

  public_subnet_1_id  = module.vpc.public_subnet_1_id
  private_subnet_1_id = module.vpc.private_subnet_1_id
  private_subnet_2_id = module.vpc.private_subnet_2_id

  master_sg_id = module.security_groups.app_sg_id
  slave1_sg_id = module.security_groups.app_sg_id
  slave2_sg_id = module.security_groups.app_sg_id

  key_name = "nateEC2key"
}
