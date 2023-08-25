terraform {
  cloud {
    organization = "JLR"

    workspaces {
      name = "tfcloud-lab"
    }
  }
}
