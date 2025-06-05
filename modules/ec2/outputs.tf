output "master_instance_id" {
  value = aws_instance.master.id
}

output "slave1_instance_id" {
  value = aws_instance.slave1.id
}

output "slave2_instance_id" {
  value = aws_instance.slave2.id
}