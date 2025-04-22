import os
import random
import string
import subprocess

def generate_suffix(length=4):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def check_existing_resource(resource_group, resource_type, name):
    try:
        result = subprocess.run(
            ["az", resource_type, "show", "--name", name, "--resource-group", resource_group],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"⚠️ Could not verify resource existence: {e}")
        return False

def validate_ssh_key(path):
    if not os.path.exists(os.path.expanduser(path)):
        raise FileNotFoundError(f"❌ SSH key not found at {path}")
    return path

def prompt_vm_inputs():
    suffix = generate_suffix()
    prefix = input("Enter VM name prefix (e.g., appvm): ")
    full_prefix = f"{prefix}-{suffix}"

    location = input("Enter Azure location (e.g., eastus): ")
    resource_group = input("Enter Resource Group name: ")

    if check_existing_resource(resource_group, "vm", full_prefix):
        raise Exception(f"❌ A VM with name {full_prefix} already exists in {resource_group}.")

    ssh_key = input("Enter path to SSH public key (e.g., ~/.ssh/id_rsa.pub): ")
    validate_ssh_key(ssh_key)

    return {
        "assign_public_ip_to": "vm",
        "public_ip_name": f"shared-ip-{suffix}",
        "vm_count": input("Enter number of VMs: "),
        "vm_size": input("Enter VM size (e.g., Standard_B2s): "),
        "vm_name_prefix": full_prefix,
        "location": location,
        "resource_group_name": resource_group,
        "admin_username": input("Enter VM admin username: "),
        "ssh_public_key": ssh_key,
    }

def prompt_k8s_inputs():
    suffix = generate_suffix()
    base_name = input("Enter base name for Kubernetes cluster (e.g., aks-cluster): ")
    full_name = f"{base_name}-{suffix}"

    location = input("Enter Azure location (e.g., eastus): ")
    resource_group = input("Enter Resource Group name: ")

    if check_existing_resource(resource_group, "aks", full_name):
        raise Exception(f"❌ AKS Cluster {full_name} already exists in {resource_group}.")

    ssh_key = input("Enter path to SSH public key (e.g., ~/.ssh/id_rsa.pub): ")
    validate_ssh_key(ssh_key)

    return {
        "assign_public_ip_to": "k8s",
        "public_ip_name": f"shared-ip-{suffix}",
        "cluster_name": full_name,
        "dns_prefix": f"{base_name}-dns",
        "kubernetes_version": input("Enter Kubernetes version (e.g., 1.29.0): "),
        "node_count": input("Enter number of worker nodes: "),
        "node_vm_size": input("Enter VM size for nodes (e.g., Standard_B2s): "),
        "location": location,
        "resource_group_name": resource_group,
        "admin_username": input("Enter admin username: "),
        "ssh_public_key": ssh_key,
    }

def prompt_sql_inputs():
    suffix = generate_suffix()
    base_name = input("Enter SQL Server base name (e.g., sqlserver): ")
    server_name = f"{base_name}-{suffix}"

    location = input("Enter Azure location (e.g., eastus): ")
    resource_group = input("Enter Resource Group name: ")

    if check_existing_resource(resource_group, "sql", server_name):
        raise Exception(f"❌ SQL Server {server_name} already exists in {resource_group}.")

    return {
        "assign_public_ip_to": "sql",
        "public_ip_name": f"shared-ip-{suffix}",
        "sql_server_name": server_name,
        "sql_admin_user": input("Enter SQL admin username: "),
        "sql_admin_password": input("Enter SQL admin password: "),
        "location": location,
        "resource_group_name": resource_group,
    }

def update_sql_version():
    server_name = input("Enter SQL Server name: ")
    resource_group = input("Enter Resource Group name: ")
    new_version = input("Enter new SQL Server version (e.g., 12.0, 14.0): ")

    if not check_existing_resource(resource_group, "sql", server_name):
        print(f"❌ SQL Server {server_name} does not exist in {resource_group}.")
        return

    try:
        subprocess.run(
            ["az", "sql", "server", "update", "--name", server_name, "--resource-group", resource_group, "--version", new_version],
            check=True
        )
        print(f"✅ SQL Server {server_name} updated to version {new_version}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Update failed: {e.stderr}")

def upgrade_kubernetes_version(tfvars_path="terraform.tfvars"):
    new_version = input("Enter new Kubernetes version (e.g., 1.29.0): ")
    update_tfvars(tfvars_path, {"kubernetes_version": new_version})
    print(f"✅ Kubernetes version updated to {new_version} in {tfvars_path}")

def update_tfvars(tfvars_path, new_vars):
    lines = []
    if os.path.exists(tfvars_path):
        with open(tfvars_path, "r") as f:
            lines = f.readlines()

    tfvars = {}
    for line in lines:
        if "=" in line:
            key, val = line.split("=", 1)
            tfvars[key.strip()] = val.strip()

    tfvars.update(new_vars)

    with open(tfvars_path, "w") as f:
        for key, val in tfvars.items():
            if isinstance(val, bool) or str(val).lower() in ["true", "false"]:
                f.write(f"{key} = {val}\n")
            elif str(val).isnumeric():
                f.write(f"{key} = {val}\n")
            elif str(val).startswith('"') and str(val).endswith('"'):
                f.write(f"{key} = {val}\n")
            else:
                f.write(f'{key} = "{val}"\n')

def main():
    print("Choose what to create or update:")
    print("1. Virtual Machine(s)")
    print("2. Kubernetes Cluster")
    print("3. SQL Server")
    print("4. Update SQL Server Version")
    print("5. Upgrade Kubernetes Version")

    choice = input("Enter your choice (1-5): ").strip()

    try:
        if choice == "1":
            vars_to_write = prompt_vm_inputs()
            update_tfvars("terraform.tfvars", vars_to_write)
        elif choice == "2":
            vars_to_write = prompt_k8s_inputs()
            update_tfvars("terraform.tfvars", vars_to_write)
        elif choice == "3":
            vars_to_write = prompt_sql_inputs()
            update_tfvars("terraform.tfvars", vars_to_write)
        elif choice == "4":
            update_sql_version()
        elif choice == "5":
            upgrade_kubernetes_version()
        else:
            print("❌ Invalid choice.")
    except Exception as e:
        print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    main()
