import os
import random
import string
import subprocess  # To run az CLI commands

def generate_suffix(length=4):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def prompt_vm_inputs():
    suffix = generate_suffix()
    prefix = input("Enter VM name prefix (e.g., appvm): ")
    full_prefix = f"{prefix}-{suffix}"

    return {
        "assign_public_ip_to": "vm",
        "public_ip_name": f"shared-ip-{suffix}",
        "vm_count": input("Enter number of VMs: "),
        "vm_size": input("Enter VM size (e.g., Standard_B2s): "),
        "vm_name_prefix": full_prefix,
        "location": input("Enter Azure location (e.g., eastus): "),
        "resource_group_name": input("Enter Resource Group name: "),
        "admin_username": input("Enter VM admin username: "),
        "ssh_public_key": input("Enter path to SSH public key (e.g., ~/.ssh/id_rsa.pub): "),
    }

def prompt_k8s_inputs():
    suffix = generate_suffix()
    base_name = input("Enter base name for Kubernetes cluster (e.g., aks-cluster): ")
    full_name = f"{base_name}-{suffix}"

    return {
        "assign_public_ip_to": "k8s",
        "public_ip_name": f"shared-ip-{suffix}",
        "cluster_name": full_name,
        "dns_prefix": f"{base_name}-dns",
        "kubernetes_version": input("Enter Kubernetes version (e.g., 1.29.0): "),
        "node_count": input("Enter number of worker nodes: "),
        "node_vm_size": input("Enter VM size for nodes (e.g., Standard_B2s): "),
        "location": input("Enter Azure location (e.g., eastus): "),
        "resource_group_name": input("Enter Resource Group name: "),
        "admin_username": input("Enter admin username: "),
        "ssh_public_key": input("Enter path to SSH public key (e.g., ~/.ssh/id_rsa.pub): "),
    }

def prompt_sql_inputs():
    suffix = generate_suffix()
    server_base = input("Enter SQL Server base name (e.g., sqlserver): ")

    return {
        "assign_public_ip_to": "sql",
        "public_ip_name": f"shared-ip-{suffix}",
        "sql_server_name": f"{server_base}-{suffix}",
        "sql_admin_user": input("Enter SQL admin username: "),
        "sql_admin_password": input("Enter SQL admin password: "),
        "location": input("Enter Azure location (e.g., eastus): "),
        "resource_group_name": input("Enter Resource Group name: "),
    }

def update_sql_version():
    # Prompt for the current and new version
    server_name = input("Enter the SQL Server name to update: ")
    resource_group = input("Enter the Resource Group name: ")
    new_version = input("Enter the new SQL Server version (e.g., 12.0, 14.0): ")

    # Run the az CLI command to update the SQL Server version
    print(f"Updating SQL Server {server_name} to version {new_version}...")
    try:
        result = subprocess.run(
            [
                "az", "sql", "server", "update",
                "--name", server_name,
                "--resource-group", resource_group,
                "--version", new_version
            ],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✅ Successfully updated SQL Server to version {new_version}.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to update SQL Server: {e.stderr}")
        print(e.output)

def update_tfvars(tfvars_path, new_vars):
    lines = []
    if os.path.exists(tfvars_path):
        with open(tfvars_path, "r") as file:
            lines = file.readlines()

    tfvars = {}
    for line in lines:
        if "=" in line:
            key, val = line.split("=", 1)
            tfvars[key.strip()] = val.strip()

    tfvars.update(new_vars)

    with open(tfvars_path, "w") as file:
        for key, val in tfvars.items():
            if isinstance(val, bool) or val.lower() in ["true", "false"]:
                file.write(f'{key} = {val}\n')
            elif val.isnumeric():
                file.write(f'{key} = {val}\n')
            elif val.startswith('"') and val.endswith('"'):
                file.write(f'{key} = {val}\n')
            else:
                file.write(f'{key} = "{val}"\n')

    print(f"\n✅ Updated {tfvars_path} with new values.")

def main():
    print("Choose what to create or update:")
    print("1. Virtual Machine(s)")
    print("2. Kubernetes Cluster")
    print("3. SQL Server")
    print("4. Update SQL Server Version")

    choice = input("Enter 1, 2, 3, or 4: ").strip()

    if choice == "1":
        vars_to_write = prompt_vm_inputs()
    elif choice == "2":
        vars_to_write = prompt_k8s_inputs()
    elif choice == "3":
        vars_to_write = prompt_sql_inputs()
    elif choice == "4":
        update_sql_version()
        return
    else:
        print("❌ Invalid choice.")
        return

    update_tfvars("terraform.tfvars", vars_to_write)

if __name__ == "__main__":
    main()
