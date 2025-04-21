terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }

  required_version = ">= 1.3.0"
}

provider "azurerm" {
  features {}
}

# -----------------------------
# Shared Public IP Resource
# -----------------------------
module "public_ip" {
  source              = "./modules/public_ip"
  public_ip_name      = var.public_ip_name
  location            = var.location
  resource_group_name = var.resource_group_name
}

# -----------------------------
# VM Module (optional)
# -----------------------------
module "vm" {
  source              = "./modules/vm"
  count               = var.assign_public_ip_to == "vm" ? 1 : 0

  vm_name             = "vm-${random_string.vm_suffix.result}"
  location            = var.location
  resource_group_name = var.resource_group_name
  subnet_id           = var.subnet_id
  public_ip_id        = module.public_ip.public_ip_id
}

# -----------------------------
# Kubernetes Module (optional)
# -----------------------------
module "k8s" {
  source              = "./modules/k8s"
  count               = var.assign_public_ip_to == "k8s" ? 1 : 0

  cluster_name        = "k8s-${random_string.k8s_suffix.result}"
  location            = var.location
  resource_group_name = var.resource_group_name
  public_ip_id        = module.public_ip.public_ip_id

  kubernetes_version  = var.kubernetes_version    
  dns_prefix          = var.dns_prefix            
  node_count          = var.node_count            
  node_vm_size        = var.node_vm_size          
  admin_username      = var.admin_username       
  ssh_public_key      = var.ssh_public_key        
}

# -----------------------------
# SQL Server Module (optional)
# -----------------------------
module "sql" {
  source              = "./modules/sql"
  count               = var.assign_public_ip_to == "sql" ? 1 : 0

  sql_server_name     = "sql-${random_string.sql_suffix.result}"
  location            = var.location
  resource_group_name = var.resource_group_name
  public_ip_id        = module.public_ip.public_ip_id
  sql_server_version  = var.sql_server_version  # Adding version dynamically
}

# -----------------------------
# Random suffix generators
# -----------------------------
resource "random_string" "vm_suffix" {
  length  = 4
  upper   = false
  lower   = true
  numeric = true
}

resource "random_string" "k8s_suffix" {
  length  = 4
  upper   = false
  lower   = true
  numeric = true
}

resource "random_string" "sql_suffix" {
  length  = 4
  upper   = false
  lower   = true
  numeric = true
}
