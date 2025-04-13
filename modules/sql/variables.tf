variable "sql_server_name" {
  description = "The name of the SQL Server"
  type        = string
}

variable "sql_database_name" {
  description = "The name of the SQL Database"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
}

variable "resource_group_name" {
  description = "Resource group for the SQL Server"
  type        = string
}

variable "admin_username" {
  description = "SQL Server admin username"
  type        = string
}

variable "admin_password" {
  description = "SQL Server admin password"
  type        = string
  sensitive   = true
}

variable "sku_name" {
  description = "The SKU name for the database (e.g., Basic, S0, P1)"
  type        = string
}

variable "max_size_gb" {
  description = "Max size of the SQL database in GB"
  type        = number
  default     = 2
}
