output "vm_names" {
  value = [for vm in azurerm_linux_virtual_machine.vm : vm.name]
}

output "vm_public_ip" {
  value = var.assign_public_ip_to == "vm" ? azurerm_public_ip.vm_public_ip[0].ip_address : null
}
