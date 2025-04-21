# Global settings
location             = "eastus"
resource_group_name  = "infra-rg"
admin_username       = "azureuser"
ssh_public_key       = "~/.ssh/id_rsa.pub"

# VM settings
vm_count             = 2
vm_size              = "Standard_B2s"
vm_name_prefix       = "appvm"

# Kubernetes settings
cluster_name         = "aks-cluster"
dns_prefix           = "aksinfra"
kubernetes_version   = "1.29.0"
node_count           = 3
node_vm_size         = "Standard_B2s"

# SQL Server settings (optional)
sql_server_name      = "sql-infra"
sql_admin_user       = "sqladmin"
sql_admin_password   = "YourSecurePassword123!"
sql_server_version   = "12.0"  # Adding SQL server version setting

# Public IP assignment
assign_public_ip_to  = "vm"  # Options: vm, sql, k8s
public_ip_name       = "shared-public-ip"

# Networking
subnet_id            = "/subscriptions/xxx/resourceGroups/infra-rg/providers/Microsoft.Network/virtualNetworks/infra-vnet/subnets/default"
