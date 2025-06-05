# Output for the app security group ID
output "app_sg_id" {
  value = aws_security_group.app_sg.id
}

