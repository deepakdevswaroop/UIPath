variable "location" {
  description = "Azure region"
  type        = string
}

variable "resource_group_name" {
  description = "Resource group name"
  type        = string
}

variable "admin_username" {
  description = "Admin username"
  type        = string
}

variable "ssh_public_key" {
  description = "SSH public key path"
  type        = string
}

variable "cluster_name" {
  description = "AKS cluster name"
  type        = string
}

variable "dns_prefix" {
  description = "DNS prefix for AKS"
  type        = string
}

variable "kubernetes_version" {
  description = "Kubernetes version"
  type        = string
}

variable "node_count" {
  description = "Number of worker nodes"
  type        = number
}

variable "node_vm_size" {
  description = "VM size for node pool"
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
