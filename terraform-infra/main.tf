module "vm" {
  source              = "./modules/vm"
  location            = var.location
  vm_count            = var.vm_count
  vm_size             = var.vm_size
  resource_group_name = var.resource_group_name
  name_prefix         = var.vm_name_prefix
  admin_username      = var.admin_username
  ssh_public_key      = var.ssh_public_key
}

module "k8s" {
  source              = "./modules/k8s"
  location            = var.location
  resource_group_name = var.resource_group_name
  cluster_name        = var.cluster_name
  dns_prefix          = var.dns_prefix
  kubernetes_version  = var.kubernetes_version
  node_count          = var.node_count
  node_vm_size        = var.node_vm_size
  admin_username      = var.admin_username
  ssh_public_key      = var.ssh_public_key
}
