# Fetch Ubuntu AMI
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# MASTER EC2
resource "aws_instance" "master" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = "t2.micro"
  subnet_id              = var.public_subnet_1_id
  vpc_security_group_ids = [var.master_sg_id]
  key_name               = var.key_name

  tags = {
    Name = "master-node"
  }
}

# SLAVE 1 EC2
resource "aws_instance" "slave1" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = "t2.micro"
  subnet_id              = var.private_subnet_1_id
  vpc_security_group_ids = [var.slave1_sg_id]
  key_name               = var.key_name

  tags = {
    Name = "slave1-node"
  }
}

# SLAVE 2 EC2
resource "aws_instance" "slave2" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = "t2.micro"
  subnet_id              = var.private_subnet_2_id
  vpc_security_group_ids = [var.slave2_sg_id]
  key_name               = var.key_name

  tags = {
    Name = "slave2-node"
  }
}