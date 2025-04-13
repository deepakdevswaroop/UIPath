variable "location" {}
variable "resource_group_name" {}
variable "admin_username" {}
variable "ssh_public_key" {}

# VM-specific
variable "vm_count" {}
variable "vm_size" {}
variable "vm_name_prefix" {}

# K8s-specific
variable "cluster_name" {}
variable "dns_prefix" {}
variable "kubernetes_version" {}
variable "node_count" {}
variable "node_vm_size" {}
