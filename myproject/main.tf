provider "proxmox" {
  endpoint = var.pve_api_url
  username = var.pve_username
  password = var.pve_password
  insecure = true
}


resource "proxmox_virtual_environment_vm" "vm" {
  count      = length(var.vm_configs)
  name       = var.vm_configs[count.index].name
  node_name  = var.vm_configs[count.index].node

  agent {
    enabled = true
  }

  cpu {
    cores = var.vm_configs[count.index].cpu
  }

  memory {
    dedicated = var.vm_configs[count.index].memory
  }

  initialization {
    ip_config {
      ipv4 {
        address = var.vm_configs[count.index].ip_address
        gateway = var.vm_configs[count.index].gateway
      }
    }

    dns {
      servers = ["8.8.8.8", var.vm_configs[count.index].gateway]
    }

    # user_account {
    #   keys     = [trimspace(tls_private_key.ubuntu_vm_key.public_key_openssh)]
    #   username = var.username
    #   password = var.password
    # }
    user_data_file_id = proxmox_virtual_environment_file.cloud_config[count.index].id
  }

  dynamic "disk" {
    for_each = var.vm_configs[count.index].disks
    content {
      datastore_id = disk.value.datastore
      file_id      = "local:import/ubuntu-22.04-cloudimg.qcow2"
      interface    = "scsi0"
      discard      = "on"
      size         = disk.value.size
    }
  }

  network_device {
    model  = "virtio"
    bridge = "vmbr0"
  }
}

# resource "random_password" "ubuntu_vm_password" {
#   length           = 8
#   override_special = "_%@"
#   special          = true
# }

resource "tls_private_key" "ubuntu_vm_key" {
  algorithm = "RSA"
  rsa_bits  = 2048
}

# resource "proxmox_virtual_environment_file" "cloud_config" {
#   content_type = "snippets"
#   datastore_id = "local"
#   node_name    = "pve1"

#   source_file {
#     path = "cloud-init.yaml"  # แก้เป็น path ไฟล์ cloud-init.yaml จริงบนเครื่องคุณ
#   }
# }

data "template_file" "cloud_init" {
  count    = length(var.vm_configs)
  template = file("${path.module}/cloud-init.yaml")

  vars = {
    hostname       = var.vm_configs[count.index].name
    ip_address     = "${var.vm_configs[count.index].ip_address}"  # ใส่ netmask ด้วย เช่น 192.168.1.10/24
    gateway        = var.vm_configs[count.index].gateway
    username       = var.username
    ssh_public_key = trimspace(tls_private_key.ubuntu_vm_key.public_key_openssh)
    hashed_password= var.hashed_password
  }
}

resource "proxmox_virtual_environment_file" "cloud_config" {
  count        = length(var.vm_configs)
  content_type = "snippets"
  datastore_id = "local"
  node_name    = var.vm_configs[count.index].node

  source_raw {
    data      = data.template_file.cloud_init[count.index].rendered
    file_name = "cloud-init-${var.vm_configs[count.index].name}.yaml"
  }
}