variable "public_ip_name" {}
variable "location" {}
variable "resource_group_name" {}

resource "azurerm_public_ip" "this" {
  name                = var.public_ip_name
  location            = var.location
  resource_group_name = var.resource_group_name
  allocation_method   = "Static"
  sku                 = "Standard"
}

output "public_ip_id" {
  value = azurerm_public_ip.this.id
}
