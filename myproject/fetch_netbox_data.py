# # import requests
# # import json

# # NETBOX_URL = "http://172.16.46.100/api"
# # NETBOX_TOKEN = "493e5a2da21cb07c8dfd7eecd63865aeefe62d08"

# # HEADERS = {
# #     "Authorization": f"Token {NETBOX_TOKEN}",
# #     "Content-Type": "application/json"
# # }

# # def get_vms():
# #     url = f"{NETBOX_URL}/virtualization/virtual-machines/?status=staged"
# #     response = requests.get(url, headers=HEADERS)
# #     response.raise_for_status()
# #     data = response.json()
# #     print(f"DEBUG: Total VMs fetched: {data.get('count')}")
# #     for vm in data.get('results', []):
# #         print(f"DEBUG: VM name: {vm.get('name')}, vcpus: {vm.get('vcpus')}, memory: {vm.get('memory')}, device: {vm.get('device')}")
# #     return data["results"]

# # def get_disks():
# #     url = f"{NETBOX_URL}/virtualization/virtual-disks/"
# #     response = requests.get(url, headers=HEADERS)
# #     response.raise_for_status()
# #     data = response.json()
# #     print(f"DEBUG: Total Disks fetched: {data.get('count')}")
# #     for disk in data.get('results', []):
# #         vm = disk.get("virtual_machine")
# #         vm_name = vm.get("name") if vm else "No VM"
# #         print(f"DEBUG: Disk name: {disk.get('name')}, VM: {vm_name}")
# #     return data["results"]

# # def build_tfvars(vms, disks):
# #     # สร้าง map vm_id → list of disk names
# #     vm_disk_map = {}
# #     for disk in disks:
# #         vm = disk.get("virtual_machine")
# #         if vm:
# #             vm_id = vm["id"]
# #             vm_disk_map.setdefault(vm_id, []).append(disk["name"])

# #     tfvars = {
# #         "pve_api_url": "https://172.16.46.101:8006/api2/json",
# #         "pve_username": "root@pam",
# #         "pve_password": "P@ssw0rd",
# #         "vm_configs": []
# #     }

# #     for vm in vms:
# #         node = vm.get("device", {}).get("name", "pve1")
# #         cpu = int(vm.get("vcpus", 2))
# #         raw_memory = vm.get("memory", 1024)  # MB
# #         raw_disk = vm.get("disk", 8192)      # MB

# #         # แปลงหน่วย
# #         memory = int(round(raw_memory * 1.024))  # MB → MiB
# #         disk = int(round(raw_disk / 1000))       # MB → GB (SI)
# #         template_id = 9000  # กำหนด default

# #         disks_for_vm = vm_disk_map.get(vm["id"], [])

# #         print(f"DEBUG: Adding VM config: name={vm.get('name')}, node={node}, cpu={cpu}, memory={memory}, disk={disk}, template_id={template_id}, disks={disks_for_vm}")

# #         tfvars["vm_configs"].append({
# #             "name": vm.get("name"),
# #             "node": node,
# #             "cpu": cpu,
# #             "memory": memory,
# #             "disk": disk,
# #             "template_id": template_id,
# #             "disks": disks_for_vm
# #         })

# #     with open("terraform.tfvars.json", "w") as f:
# #         json.dump(tfvars, f, indent=2)

# # if __name__ == "__main__":
# #     vms = get_vms()
# #     disks = get_disks()
# #     build_tfvars(vms, disks)


# # import requests
# # import json

# # NETBOX_URL = "http://172.16.46.100/api"
# # NETBOX_TOKEN = "493e5a2da21cb07c8dfd7eecd63865aeefe62d08"

# # HEADERS = {
# #     "Authorization": f"Token {NETBOX_TOKEN}",
# #     "Content-Type": "application/json"
# # }

# # def get_vms():
# #     url = f"{NETBOX_URL}/virtualization/virtual-machines/?status=staged"
# #     response = requests.get(url, headers=HEADERS)
# #     response.raise_for_status()
# #     data = response.json()
# #     print(f"DEBUG: Total VMs fetched: {data.get('count')}")
# #     for vm in data.get('results', []):
# #         print(f"DEBUG: VM name: {vm.get('name')}, vcpus: {vm.get('vcpus')}, memory: {vm.get('memory')}, device: {vm.get('device')}")
# #     return data["results"]

# # def get_disks():
# #     url = f"{NETBOX_URL}/virtualization/virtual-disks/"
# #     response = requests.get(url, headers=HEADERS)
# #     response.raise_for_status()
# #     data = response.json()
# #     print(f"DEBUG: Total Disks fetched: {data.get('count')}")
# #     for disk in data.get('results', []):
# #         vm = disk.get("virtual_machine")
# #         vm_name = vm.get("name") if vm else "No VM"
# #         print(f"DEBUG: Disk name: {disk.get('name')}, VM: {vm_name}")
# #     return data["results"]

# # def build_tfvars(vms, disks):
# #     # สร้าง map vm_id → list ของ disk dict { datastore, size }
# #     vm_disk_map = {}
# #     for disk in disks:
# #         vm = disk.get("virtual_machine")
# #         if vm:
# #             vm_id = vm["id"]
# #             datastore = disk["name"]
# #             size_mb = disk.get("size", 0)
# #             size_gb = int(round(size_mb / 1000)) if size_mb else 10  # default 10 GB

# #             disk_obj = {
# #                 "datastore": datastore,
# #                 "size": size_gb
# #             }
# #             vm_disk_map.setdefault(vm_id, []).append(disk_obj)

# #     tfvars = {
# #         "pve_api_url": "https://172.16.46.101:8006/api2/json",
# #         "pve_username": "root@pam",
# #         "pve_password": "P@ssw0rd",
# #         "vm_configs": []
# #     }

# #     for vm in vms:
# #         node = vm.get("device", {}).get("name", "pve1")
# #         cpu = int(vm.get("vcpus", 2))
# #         raw_memory = vm.get("memory", 1024)  # MB
# #         memory = int(round(raw_memory * 1.024))  # แปลงเป็น MiB
# #         template_id = 9000  # กำหนด default

# #         disks_for_vm = vm_disk_map.get(vm["id"], [])

# #         print(f"DEBUG: Adding VM config: name={vm.get('name')}, node={node}, cpu={cpu}, memory={memory}, disks={disks_for_vm}")

# #         tfvars["vm_configs"].append({
# #             "name": vm.get("name"),
# #             "node": node,
# #             "cpu": cpu,
# #             "memory": memory,
# #             "template_id": template_id,
# #             "disks": disks_for_vm
# #         })

# #     with open("terraform.tfvars.json", "w") as f:
# #         json.dump(tfvars, f, indent=2)

# # if __name__ == "__main__":
# #     vms = get_vms()
# #     disks = get_disks()
# #     build_tfvars(vms, disks)
# #     print("terraform.tfvars.json created successfully.")


# # import requests
# # import json

# # NETBOX_URL = "http://172.16.46.100/api"
# # NETBOX_TOKEN = "493e5a2da21cb07c8dfd7eecd63865aeefe62d08"

# # HEADERS = {
# #     "Authorization": f"Token {NETBOX_TOKEN}",
# #     "Content-Type": "application/json"
# # }

# # def get_vms():
# #     url = f"{NETBOX_URL}/virtualization/virtual-machines/?status=staged"
# #     response = requests.get(url, headers=HEADERS)
# #     response.raise_for_status()
# #     data = response.json()
# #     print(f"DEBUG: Total VMs fetched: {data.get('count')}")
# #     return data["results"]

# # def get_disks():
# #     url = f"{NETBOX_URL}/virtualization/virtual-disks/"
# #     response = requests.get(url, headers=HEADERS)
# #     response.raise_for_status()
# #     data = response.json()
# #     print(f"DEBUG: Total Disks fetched: {data.get('count')}")
# #     return data["results"]

# # def get_interfaces():
# #     url = f"{NETBOX_URL}/virtualization/interfaces/"
# #     response = requests.get(url, headers=HEADERS)
# #     response.raise_for_status()
# #     data = response.json()
# #     print(f"DEBUG: Total Interfaces fetched: {data.get('count')}")

# #     # สร้าง map vm_id → { ip: ..., gateway: ... }
# #     vm_network_map = {}
# #     for iface in data["results"]:
# #         vm = iface.get("virtual_machine")
# #         if not vm:
# #             continue

# #         vm_id = vm["id"]
# #         gateway_ip = iface.get("custom_fields", {}).get("gateway_ip", "")

# #         # ดึง IP จาก count_ipaddresses ถ้ามี
# #         ip_url = iface.get("url") + "ip-addresses/"
# #         ip_response = requests.get(ip_url, headers=HEADERS)
# #         if ip_response.status_code == 200:
# #             ip_data = ip_response.json()
# #             ip_address = ip_data["results"][0]["address"] if ip_data["results"] else ""
# #         else:
# #             ip_address = ""

# #         vm_network_map[vm_id] = {
# #             "ip_address": ip_address,
# #             "gateway": gateway_ip
# #         }

# #     return vm_network_map

# # def build_tfvars(vms, disks, network_info):
# #     # สร้าง map vm_id → list ของ disk dict { datastore, size }
# #     vm_disk_map = {}
# #     for disk in disks:
# #         vm = disk.get("virtual_machine")
# #         if vm:
# #             vm_id = vm["id"]
# #             datastore = disk["name"]
# #             size_mb = disk.get("size", 0)
# #             size_gb = int(round(size_mb / 1000)) if size_mb else 10  # default 10 GB

# #             disk_obj = {
# #                 "datastore": datastore,
# #                 "size": size_gb
# #             }
# #             vm_disk_map.setdefault(vm_id, []).append(disk_obj)

# #     tfvars = {
# #         "pve_api_url": "https://172.16.46.101:8006/api2/json",
# #         "pve_username": "root@pam",
# #         "pve_password": "P@ssw0rd",
# #         "vm_configs": []
# #     }

# #     for vm in vms:
# #         vm_id = vm["id"]
# #         node = vm.get("device", {}).get("name", "pve1")
# #         cpu = int(vm.get("vcpus", 2))
# #         raw_memory = vm.get("memory", 1024)
# #         memory = int(round(raw_memory * 1.024))
# #         template_id = 9000
# #         disks_for_vm = vm_disk_map.get(vm_id, [])

# #         network = network_info.get(vm_id, {})
# #         ip_obj = vm.get("primary_ip4")
# #         ip_address = ip_obj.get("address") if ip_obj else ""
# #         gateway = network.get("gateway", "")

# #         print(f"DEBUG: Adding VM config: name={vm.get('name')}, ip={ip_address}, gw={gateway}")

# #         tfvars["vm_configs"].append({
# #             "name": vm.get("name"),
# #             "node": node,
# #             "cpu": cpu,
# #             "memory": memory,
# #             "template_id": template_id,
# #             "ip_address": ip_address,
# #             "gateway": gateway,
# #             "disks": disks_for_vm
# #         })

# #     with open("terraform.tfvars.json", "w") as f:
# #         json.dump(tfvars, f, indent=2)

# # if __name__ == "__main__":
# #     vms = get_vms()
# #     disks = get_disks()
# #     network_info = get_interfaces()
# #     build_tfvars(vms, disks, network_info)
# #     print("terraform.tfvars.json created successfully.")


# import requests
# import json
# from dotenv import load_dotenv
# import os
# import urllib3
# # Disable SSL warnings for self-signed certificates
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# load_dotenv()

# NETBOX_URL = os.getenv("NETBOX_URL")
# NETBOX_TOKEN = os.getenv("NETBOX_TOKEN")

# PVE_API_URL = os.getenv("PVE_API_URL")
# PVE_USERNAME = os.getenv("PVE_USERNAME")
# PVE_PASSWORD = os.getenv("PVE_PASSWORD")

# USERNAME = os.getenv("USERNAME")
# PASSWORD = os.getenv("PASSWORD")   



# HEADERS = {
#     "Authorization": f"Token {NETBOX_TOKEN}",
#     "Content-Type": "application/json"
# }

# def get_vms():
#     url = f"{NETBOX_URL}/virtualization/virtual-machines/?status=staged"
#     response = requests.get(url, headers=HEADERS, verify=False)
#     response.raise_for_status()
#     data = response.json()
#     print(f"DEBUG: Total VMs fetched: {data.get('count')}")
#     return data["results"]

# def get_disks():
#     url = f"{NETBOX_URL}/virtualization/virtual-disks/"
#     response = requests.get(url, headers=HEADERS, verify=False)
#     response.raise_for_status()
#     data = response.json()
#     print(f"DEBUG: Total Disks fetched: {data.get('count')}")
#     return data["results"]

# def get_interfaces():
#     url = f"{NETBOX_URL}/virtualization/interfaces/"
#     response = requests.get(url, headers=HEADERS, verify=False)
#     response.raise_for_status()
#     data = response.json()
#     print(f"DEBUG: Total Interfaces fetched: {data.get('count')}")

#     # สร้าง map vm_id → { ip: ..., gateway: ... }
#     vm_network_map = {}
#     for iface in data["results"]:
#         vm = iface.get("virtual_machine")
#         if not vm:
#             continue

#         vm_id = vm["id"]
#         gateway_ip = iface.get("custom_fields", {}).get("gateway_ip", "")

#         # ดึง IP จาก count_ipaddresses ถ้ามี
#         ip_url = iface.get("url") + "ip-addresses/"
#         ip_response = requests.get(ip_url, headers=HEADERS, verify=False)
#         if ip_response.status_code == 200:
#             ip_data = ip_response.json()
#             ip_address = ip_data["results"][0]["address"] if ip_data["results"] else ""
#         else:
#             ip_address = ""

#         vm_network_map[vm_id] = {
#             "ip_address": ip_address,
#             "gateway": gateway_ip
#         }

#     return vm_network_map

# def build_tfvars(vms, disks, network_info):
#     # สร้าง map vm_id → list ของ disk dict { datastore, size }
#     vm_disk_map = {}
#     for disk in disks:
#         vm = disk.get("virtual_machine")
#         if vm:
#             vm_id = vm["id"]
#             datastore = disk["name"]
#             size_mb = disk.get("size", 0)
#             size_gb = int(round(size_mb / 1000)) if size_mb else 10  # default 10 GB

#             disk_obj = {
#                 "datastore": datastore,
#                 "size": size_gb
#             }
#             vm_disk_map.setdefault(vm_id, []).append(disk_obj)

#     tfvars = {
#         "pve_api_url": PVE_API_URL,
#         "pve_username": PVE_USERNAME,
#         "pve_password": PVE_PASSWORD,
#         'username': USERNAME,
#         'password': PASSWORD,
#         "vm_configs": []
#     }

#     for vm in vms:
#         vm_id = vm["id"]
#         node = vm.get("device", {}).get("name", "pve1")
#         cpu = int(vm.get("vcpus", 2))
#         raw_memory = vm.get("memory", 1024)
#         memory = int(round(raw_memory * 1.024))
#         template_id = 9000
#         disks_for_vm = vm_disk_map.get(vm_id, [])

#         network = network_info.get(vm_id, {})
#         ip_obj = vm.get("primary_ip4")
#         ip_address = ip_obj.get("address") if ip_obj else ""
#         gateway = network.get("gateway", "")

#         print(f"DEBUG: Adding VM config: name={vm.get('name')}, ip={ip_address}, gw={gateway}")

#         tfvars["vm_configs"].append({
#             "name": vm.get("name"),
#             "node": node,
#             "cpu": cpu,
#             "memory": memory,
#             "template_id": template_id,
#             "ip_address": ip_address,
#             "gateway": gateway,
#             "disks": disks_for_vm
#         })

#     with open("terraform.tfvars.json", "w") as f:
#         json.dump(tfvars, f, indent=2)

# if __name__ == "__main__":
#     vms = get_vms()
#     disks = get_disks()
#     network_info = get_interfaces()
#     build_tfvars(vms, disks, network_info)
#     print("terraform.tfvars.json created successfully.")


import requests
import json
import os
from passlib.hash import sha512_crypt
import urllib3
from dotenv import load_dotenv

# ปิด warning SSL self-signed cert
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

NETBOX_URL = os.getenv("NETBOX_URL")
NETBOX_TOKEN = os.getenv("NETBOX_TOKEN")

PVE_API_URL = os.getenv("PVE_API_URL")
PVE_USERNAME = os.getenv("PVE_USERNAME")
PVE_PASSWORD = os.getenv("PVE_PASSWORD")

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

HEADERS = {
    "Authorization": f"Token {NETBOX_TOKEN}",
    "Content-Type": "application/json"
}

def hash_password(password):
    if not password:
        return ""
    return sha512_crypt.hash(password)

def get_vms():
    url = f"{NETBOX_URL}/virtualization/virtual-machines/?status=staged"
    response = requests.get(url, headers=HEADERS, verify=False)
    response.raise_for_status()
    data = response.json()
    print(f"DEBUG: Total VMs fetched: {data.get('count')}")
    return data["results"]

def get_disks():
    url = f"{NETBOX_URL}/virtualization/virtual-disks/"
    response = requests.get(url, headers=HEADERS, verify=False)
    response.raise_for_status()
    data = response.json()
    print(f"DEBUG: Total Disks fetched: {data.get('count')}")
    return data["results"]

def get_interfaces():
    url = f"{NETBOX_URL}/virtualization/interfaces/"
    response = requests.get(url, headers=HEADERS, verify=False)
    response.raise_for_status()
    data = response.json()
    print(f"DEBUG: Total Interfaces fetched: {data.get('count')}")

    vm_network_map = {}
    for iface in data["results"]:
        vm = iface.get("virtual_machine")
        if not vm:
            continue

        vm_id = vm["id"]
        gateway_ip = iface.get("custom_fields", {}).get("gateway_ip", "")

        ip_url = iface.get("url") + "ip-addresses/"
        ip_response = requests.get(ip_url, headers=HEADERS, verify=False)
        if ip_response.status_code == 200:
            ip_data = ip_response.json()
            ip_address = ip_data["results"][0]["address"] if ip_data["results"] else ""
        else:
            ip_address = ""

        vm_network_map[vm_id] = {
            "ip_address": ip_address,
            "gateway": gateway_ip
        }

    return vm_network_map

def build_tfvars(vms, disks, network_info):
    vm_disk_map = {}
    for disk in disks:
        vm = disk.get("virtual_machine")
        if vm:
            vm_id = vm["id"]
            datastore = disk["name"]
            size_mb = disk.get("size", 0)
            size_gb = int(round(size_mb / 1000)) if size_mb else 10

            disk_obj = {
                "datastore": datastore,
                "size": size_gb
            }
            vm_disk_map.setdefault(vm_id, []).append(disk_obj)

    hashed_pw = hash_password(PASSWORD)

    tfvars = {
        "pve_api_url": PVE_API_URL,
        "pve_username": PVE_USERNAME,
        "pve_password": PVE_PASSWORD,
        "username": USERNAME,
        "password": PASSWORD,
        "hashed_password": hashed_pw,
        "vm_configs": []
    }

    for vm in vms:
        vm_id = vm["id"]
        node = vm.get("device", {}).get("name", "pve1")
        cpu = int(vm.get("vcpus", 2))
        raw_memory = vm.get("memory", 1024)
        memory = int(round(raw_memory * 1.024))
        template_id = 9000
        disks_for_vm = vm_disk_map.get(vm_id, [])

        network = network_info.get(vm_id, {})
        ip_obj = vm.get("primary_ip4")
        ip_address = ip_obj.get("address") if ip_obj else ""
        gateway = network.get("gateway", "")

        print(f"DEBUG: Adding VM config: name={vm.get('name')}, ip={ip_address}, gw={gateway}")

        tfvars["vm_configs"].append({
            "name": vm.get("name"),
            "node": node,
            "cpu": cpu,
            "memory": memory,
            "template_id": template_id,
            "ip_address": ip_address,
            "gateway": gateway,
            "disks": disks_for_vm
        })

    with open("terraform.tfvars.json", "w") as f:
        json.dump(tfvars, f, indent=2)

if __name__ == "__main__":
    vms = get_vms()
    disks = get_disks()
    network_info = get_interfaces()
    build_tfvars(vms, disks, network_info)
    print("terraform.tfvars.json created successfully.")
