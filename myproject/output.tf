output "username" {
  value     = var.username
  sensitive = false  
}

output "vm_password" {
  value     = var.password
  sensitive = false  
}
output "vm_name" {
  value = [for vm in proxmox_virtual_environment_vm.vm : vm.name]
#   value = proxmox_virtual_environment_vm.example_vm.name
}

output "vm_ids" {
  value = [for vm in proxmox_virtual_environment_vm.vm : vm.id]
#   value = proxmox_virtual_environment_vm.example_vm.id
}

output "ubuntu_vm_private_key" {
  value     = tls_private_key.ubuntu_vm_key.private_key_pem
  sensitive = true
}

output "ubuntu_vm_public_key" {
  value = tls_private_key.ubuntu_vm_key.public_key_openssh
  sensitive = true
}