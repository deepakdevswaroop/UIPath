output "vm_names" {
  value = module.vm.vm_names
}

output "kube_config" {
  value     = module.k8s.kube_config
  sensitive = true
}

output "k8s_cluster_name" {
  value = module.k8s.cluster_name
}

output "assigned_resource" {
  value = var.assign_public_ip_to
}

output "public_ip_id" {
  value = module.public_ip.public_ip_id
}
