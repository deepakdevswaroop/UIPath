# Global settings
variable "location" {
  description = "Azure location"
  type        = string
}

variable "resource_group_name" {
  description = "Resource Group name"
  type        = string
}

variable "admin_username" {
  description = "SSH admin username"
  type        = string
}

variable "ssh_public_key" {
  description = "Path to your SSH public key"
  type        = string
}

# VM module inputs
variable "vm_count" {
  description = "Number of VMs to create"
  type        = number
}

variable "vm_size" {
  description = "Size of VM instances"
  type        = string
}

variable "vm_name_prefix" {
  description = "Prefix for VM names"
  type        = string
}

# Kubernetes module inputs
variable "cluster_name" {
  description = "Kubernetes cluster name"
  type        = string
}

variable "dns_prefix" {
  description = "DNS prefix for the cluster"
  type        = string
}

variable "kubernetes_version" {
  description = "Kubernetes version to deploy"
  type        = string
}

variable "node_count" {
  description = "Number of nodes in Kubernetes cluster"
  type        = number
}

variable "node_vm_size" {
  description = "VM size for Kubernetes worker nodes"
  type        = string
}

# SQL Server module inputs
variable "sql_server_name" {
  description = "Name of the SQL Server instance"
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

# Public IP assignment
variable "assign_public_ip_to" {
  description = "Target resource to assign public IP: vm, sql, or k8s"
  type        = string
}

variable "public_ip_name" {
  description = "Shared public IP name"
  type        = string
}

# Network reference
variable "subnet_id" {
  description = "Azure subnet ID where resources are deployed"
  type        = string
}
