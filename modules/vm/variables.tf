variable "location" {
  description = "Azure region"
  type        = string
}

variable "resource_group_name" {
  description = "Resource group name"
  type        = string
}

variable "admin_username" {
  description = "Admin username for VMs"
  type        = string
}

variable "ssh_public_key" {
  description = "SSH public key for authentication"
  type        = string
}

variable "vm_count" {
  description = "Number of VMs to create"
  type        = number
}

variable "vm_size" {
  description = "VM size (SKU)"
  type        = string
}

variable "vm_name_prefix" {
  description = "Prefix for VM names"
  type        = string
}

variable "assign_public_ip_to" {
  description = "Which resource to assign public IP"
  type        = string
}

variable "public_ip_name" {
  description = "Name of the shared public IP"
  type        = string
}
