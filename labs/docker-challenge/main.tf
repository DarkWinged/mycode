terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 2.22.0"
    }
  }
}

provider "docker" {}

resource "docker_image" "simplegoservice" {
  name         = "registry.gitlab.com/alta3/simplegoservice"
  keep_locally = true
}

resource "docker_container" "nginx" {
  image = docker_image.simplegoservice.image_id
  name = var.container_name
  ports {
    internal = var.internal_port
    external = var.external_port
  }
}

variable "container_name" {
  description = "Value of the name for the Docker container"
  type        = string
  default     = "AltaResearchWebService"
}

variable "internal_port" {
  description = "Port number for the app"
  type        = number
  default     = 9876
}
variable "external_port" {
  description = "Port number for the container"
  type        = number
  default     = 5432
}
