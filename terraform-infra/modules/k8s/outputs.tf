output "aks_cluster_name" {
  value = azurerm_kubernetes_cluster.aks.name
}

output "kube_config" {
  value     = azurerm_kubernetes_cluster.aks.kube_config_raw
  sensitive = true
}

output "kubernetes_version" {
  description = "The Kubernetes version of the AKS cluster"
  value       = azurerm_kubernetes_cluster.aks.kubernetes_version
}
