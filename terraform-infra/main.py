import os

def prompt_vm_inputs():
    return {
        "vm_count": input("Enter number of VMs: "),
        "vm_size": input("Enter VM size (e.g., Standard_B2s): "),
        "vm_name_prefix": input("Enter VM name prefix: "),
        "location": input("Enter Azure location (e.g., eastus): "),
        "resource_group_name": input("Enter Resource Group name: "),
        "admin_username": input("Enter VM admin username: "),
        "ssh_public_key": input("Enter path to SSH public key (e.g., ~/.ssh/id_rsa.pub): "),
    }

def prompt_k8s_inputs():
    return {
        "cluster_name": input("Enter Kubernetes cluster name: "),
        "dns_prefix": input("Enter DNS prefix: "),
        "kubernetes_version": input("Enter Kubernetes version (e.g., 1.29.0): "),
        "node_count": input("Enter number of worker nodes: "),
        "node_vm_size": input("Enter VM size for nodes (e.g., Standard_B2s): "),
        "location": input("Enter Azure location (e.g., eastus): "),
        "resource_group_name": input("Enter Resource Group name: "),
        "admin_username": input("Enter admin username: "),
        "ssh_public_key": input("Enter path to SSH public key (e.g., ~/.ssh/id_rsa.pub): "),
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

    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        vars_to_write = prompt_vm_inputs()
    elif choice == "2":
        vars_to_write = prompt_k8s_inputs()
    else:
        print("❌ Invalid choice.")
        return

    update_tfvars("terraform.tfvars", vars_to_write)

if __name__ == "__main__":
    main()
