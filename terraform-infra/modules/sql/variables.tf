variable "location" {
  description = "Azure region"
  type        = string
}

variable "resource_group_name" {
  description = "Resource group name"
  type        = string
}

variable "sql_server_name" {
  description = "SQL Server name"
  type        = string
}

variable "sql_database_name" {
  description = "SQL Database name"
  type        = string
}

variable "sql_admin_user" {
  description = "SQL Server admin username"
  type        = string
}

variable "sql_admin_password" {
  description = "SQL Server admin password"
  type        = string
  sensitive   = true
}

variable "sql_server_version" {
  description = "SQL Server version (e.g., 12.0, 14.0)"
  type        = string
  default     = "12.0"
}

variable "sql_sku_name" {
  description = "SQL SKU (e.g., Basic, S0)"
  type        = string
}

variable "sql_max_size_gb" {
  description = "Maximum size of the database in GB"
  type        = number
}

variable "assign_public_ip_to" {
  description = "Which resource to assign public IP"
  type        = string
}

variable "public_ip_name" {
  description = "Name of the shared public IP"
  type        = string
}
