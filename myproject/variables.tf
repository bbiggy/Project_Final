variable "pve_api_url" {
  description = "The URL for the Proxmox API endpoint"
  type        = string
}

variable "pve_username" {
  description = "Username for Proxmox authentication"
  type        = string
}

variable "pve_password" {
  description = "Password for Proxmox authentication"
  type        = string
  sensitive   = true
}

variable "username" {
  description = "Username for VM account"
  type        = string
}

variable "password" {
  description = "Password for VM account"
  type        = string
}

variable "hashed_password" {
  type = string
  description = "Pre-hashed password for user creation"
  sensitive   = true
}

variable "vm_configs" {
  description = "List of VM configurations"
  type = list(object({
    name        = string
    node        = string
    memory      = number
    cpu         = number
    template_id = number
    ip_address  = string
    gateway     = string
    disks = list(object({
      size         = number
      datastore = string
    }))
  }))
}
