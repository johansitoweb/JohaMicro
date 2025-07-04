
variable "aws_region" {
  description = "La región de AWS donde se desplegará la infraestructura."
  type        = string
  default     = "us-east-1" # Puedes cambiar esto a tu región preferida
}

variable "project_name" {
  description = "Nombre del proyecto, usado para nombrar recursos."
  type        = string
  default     = "JohaMicro"
}

variable "app_port" {
  description = "Puerto en el que escucha la aplicación dentro del contenedor."
  type        = number
  default     = 8000
}

variable "desired_count" {
  description = "Número deseado de tareas de la aplicación."
  type        = number
  default     = 1
}

variable "cpu_units" {
  description = "Número de unidades de CPU para la tarea de Fargate (256, 512, 1024, 2048, etc.)."
  type        = number
  default     = 256 
}

variable "memory_mib" {
  description = "Cantidad de memoria en MiB para la tarea de Fargate (512, 1024, 2048, etc.)."
  type        = number
  default     = 512 
}