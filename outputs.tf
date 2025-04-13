output "vm_names" {
  value = [for vm in azurerm_linux_virtual_machine.this : vm.name]
}

output "vm_private_ips" {
  value = [for nic in azurerm_network_interface.this : nic.ip_configuration[0].private_ip_address]
}
