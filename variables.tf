variable "resource_group_name" {
  type        = string
  description = "Name of the resource group"
}

variable "location" {
  type        = string
  description = "Azure region"
}

variable "vm_count" {
  type        = number
  description = "Number of virtual machines to create"
  default     = 1
}

variable "name_prefix" {
  type        = string
  description = "Prefix for resource naming"
}

variable "vm_size" {
  type        = string
  description = "Size of the virtual machine"
  default     = "Standard_B2s"
}

variable "admin_username" {
  type        = string
  description = "Admin username for the VMs"
}

variable "ssh_public_key" {
  type        = string
  description = "Path to SSH public key file"
}
