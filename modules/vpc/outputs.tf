output "public_subnet_1_id" {
  value = aws_subnet.public_1.id
}

output "public_subnet_2_id" {
  value = aws_subnet.public_2.id
}

output "private_subnet_1_id" {
  value = aws_subnet.private_1.id
}

output "private_subnet_2_id" {
  value = aws_subnet.private_2.id
}

output "private_subnet_3_id" {
  value = aws_subnet.private_3.id
}

output "private_subnet_4_id" {
  value = aws_subnet.private_4.id
}

output "vpc_id" {
  value = aws_vpc.main.id
}