output "vm_names" {
  value = [for i in azurerm_linux_virtual_machine.vm : i.name]
}
