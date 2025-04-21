resource "azurerm_sql_server" "sql_server" {
  name                         = var.sql_server_name
  location                     = var.location
  resource_group_name          = var.resource_group_name
  version                      = "12.0"
  administrator_login          = var.sql_admin_username
  administrator_login_password = var.sql_admin_password

  tags = {
    Environment = "Terraform"
  }
}

resource "azurerm_sql_database" "sql_db" {
  name                = var.sql_database_name
  resource_group_name = var.resource_group_name
  location            = var.location
  server_name         = azurerm_sql_server.sql_server.name
  sku_name            = var.sql_sku_name
  max_size_gb         = var.sql_max_size_gb
}

resource "azurerm_public_ip" "sql_public_ip" {
  count               = var.assign_public_ip_to == "sql" ? 1 : 0
  name                = var.public_ip_name
  location            = var.location
  resource_group_name = var.resource_group_name
  allocation_method   = "Static"
  sku                 = "Standard"
}
