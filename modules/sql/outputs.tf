output "sql_server_name" {
  value = azurerm_sql_server.sql_server.name
}

output "sql_database_name" {
  value = azurerm_sql_database.sql_db.name
}

output "sql_public_ip" {
  value = var.assign_public_ip_to == "sql" ? azurerm_public_ip.sql_public_ip[0].ip_address : null
}
