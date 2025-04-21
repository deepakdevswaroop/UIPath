output "aks_cluster_name" {
  value = azurerm_kubernetes_cluster.aks.name
}

output "kube_config" {
  value = azurerm_kubernetes_cluster.aks.kube_config_raw
  sensitive = true
}

output "k8s_public_ip" {
  value = var.assign_public_ip_to == "k8s" ? azurerm_public_ip.k8s_public_ip[0].ip_address : null
}
