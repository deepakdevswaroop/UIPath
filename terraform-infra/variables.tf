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
