variable "location" {
  description = "Azure region"
  type        = string
}

variable "resource_group_name" {
  description = "Resource group name"
  type        = string
}

variable "admin_username" {
  description = "Admin username for the AKS Linux profile"
  type        = string
}

variable "ssh_public_key" {
  description = "SSH public key content"
  type        = string
}

variable "cluster_name" {
  description = "AKS cluster name"
  type        = string
}

variable "dns_prefix" {
  description = "DNS prefix for the AKS cluster"
  type        = string
}

variable "kubernetes_version" {
  description = "Kubernetes version to deploy"
  type        = string
}

variable "node_count" {
  description = "Number of worker nodes"
  type        = number
}

variable "node_vm_size" {
  description = "VM size for AKS node pool"
  type        = string
}

variable "public_ip_id" {
  description = "Public IP resource ID to associate"
  type        = string
}
