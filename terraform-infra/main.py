import os
import random
import string

def generate_suffix(length=4):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def prompt_vm_inputs():
    suffix = generate_suffix()
    prefix = input("Enter VM name prefix (e.g., appvm): ")
    full_prefix = f"{prefix}-{suffix}"

    return {
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
    base_name = input("Enter base name for Kubernetes cluster (e.g., akscluster): ")
    full_name = f"{base_name}-{suffix}"

    return {
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
    server_base = input("Enter SQL Server name base (e.g., sqlserver): ")
    db_base = input("Enter SQL Database name (e.g., appdb): ")

    return {
        "sql_server_name": f"{server_base}-{suffix}",
        "sql_database_name": db_base,
        "sql_admin_username": input("Enter SQL admin username: "),
        "sql_admin_password": input("Enter SQL admin password: "),
        "sql_sku_name": input("Enter SKU name (e.g., Basic, S0): "),
        "sql_max_size_gb": input("Enter max size in GB (e.g., 2): "),
        "location": input("Enter Azure location (e.g., eastus): "),
        "resource_group_name": input("Enter Resource Group name: "),
    }

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
            if val.lower() in ["true", "false"] or val.isnumeric() or val.startswith("["):
                file.write(f'{key} = {val}\n')
            elif val.startswith('"') and val.endswith('"'):
                file.write(f'{key} = {val}\n')
            else:
                file.write(f'{key} = "{val}"\n')

    print(f"\n✅ Updated {tfvars_path} with new values.")

def main():
    print("Choose what to create:")
    print("1. Virtual Machine(s)")
    print("2. Kubernetes Cluster")
    print("3. SQL Server + Database")

    choice = input("Enter 1, 2, or 3: ").strip()

    if choice == "1":
        vars_to_write = prompt_vm_inputs()
    elif choice == "2":
        vars_to_write = prompt_k8s_inputs()
    elif choice == "3":
        vars_to_write = prompt_sql_inputs()
    else:
        print("❌ Invalid choice.")
        return

    update_tfvars("terraform.tfvars", vars_to_write)

if __name__ == "__main__":
    main()
