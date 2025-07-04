
output "ecr_repository_url" {
  description = "URL del repositorio ECR para la imagen de la aplicación."
  value       = aws_ecr_repository.app_repo.repository_url
}

output "load_balancer_dns_name" {
  description = "Nombre DNS del Application Load Balancer."
  value       = aws_lb.app_lb.dns_name
}