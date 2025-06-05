variable "public_subnet_1_id" {
  description = "Subnet ID for the master node"
  type        = string
}

variable "private_subnet_1_id" {
  description = "Subnet ID for slave1"
  type        = string
}

variable "private_subnet_2_id" {
  description = "Subnet ID for slave2"
  type        = string
}

variable "master_sg_id" {
  type = string
}

variable "slave1_sg_id" {
  type = string
}

variable "slave2_sg_id" {
  type = string
}

variable "key_name" {
  description = "The name of the SSH key pair to use for the instances"
  type        = string
}