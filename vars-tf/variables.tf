variable "container_name" {
  description = "Value of the name for the Docker container"
  # basic types include string, number and bool
  type        = string
  default     = "ExampleNginxContainer"


  validation {
     condition     = length(var.container_name) > 8 && substr(var.container_name, 0, 7) == "Example"
     error_message = "The container_name must begin with Example"
  }
}

variable "internal_port" {
  description = "Port number for the app"
  type        = number
  default     = 80
}
variable "external_port" {
  description = "Port number for the container"
  type        = number
  default     = 2224
}
