location             = "eastus"
resource_group_name  = "infra-rg"
admin_username       = "azureuser"
ssh_public_key       = "~/.ssh/id_rsa.pub"

# VM values
vm_count             = 2
vm_size              = "Standard_B2s"
vm_name_prefix       = "appvm"

# Kubernetes values
cluster_name         = "aks-cluster"
dns_prefix           = "aksinfra"
kubernetes_version   = "1.29.0"
node_count           = 3
node_vm_size         = "Standard_B2s"
