
# UIPath

# Azure Infrastructure Automation with Terraform

This Terraform project automates the deployment of Azure infrastructure, including Virtual Machines (VMs), Kubernetes clusters (AKS), SQL Servers, and a shared public IP. It is built with modularity, scalability, and dynamic input control in mind.

---

## 📦 Overview

This repository includes reusable modules to create:

- ✅ Virtual Machines (VMs)
- ✅ Kubernetes Cluster (AKS)
- ✅ SQL Server and Database
- ✅ Shared Public IP (dynamically assigned to one module)

A Python script (`main.py`) is provided to dynamically update `terraform.tfvars` based on user input.

---

## ✅ Features

- **Shared Public IP Logic**: A central public IP resource is provisioned and passed to the selected module (`vm`, `k8s`, or `sql`) using a single variable.
- **Dynamic Configuration**: A Python script prompts for values and updates the `terraform.tfvars` automatically.
- **Modular Design**: Easily extend or reuse infrastructure by adding more modules.
- **Randomized Resource Naming**: Prevents name collisions using `random_string`.
- **Selective Deployment**: Only the selected module (based on user input) is deployed with a public IP.
- **Secure & Idempotent**: Follows Terraform best practices including sensitive value handling and idempotent design.
- **Edge Case Handling & Validation**:
  - Prevents creation of resources with existing names using Azure CLI.
  - SSH public key validation before proceeding.
  - SQL Server version upgrade validation.
  - Kubernetes version upgrade directly modifies `.tfvars`.

---

## 🧾 Inputs

### General Inputs (used by all modules)

- `location`: Azure region (e.g., `eastus`)
- `resource_group_name`: Azure resource group
- `admin_username`: Admin username for VMs, AKS, SQL
- `ssh_public_key`: Path to SSH public key (validated for existence)
- `assign_public_ip_to`: Which module gets the shared public IP (`vm`, `k8s`, or `sql`)
- `public_ip_name`: Name for the shared public IP

### VM Module Inputs

- `vm_name_prefix`: Auto-generated with random suffix (validated to avoid name collisions)
- `vm_size`: Size of the VM (e.g., `Standard_B2s`)
- `vm_count`: Number of VMs to deploy
- `subnet_id`: Azure subnet ID

### Kubernetes Module Inputs

- `cluster_name`: AKS cluster name (validated for uniqueness)
- `dns_prefix`: DNS prefix for AKS
- `kubernetes_version`: Kubernetes version (e.g., `1.29.0`)
- `node_count`: Number of worker nodes
- `node_vm_size`: VM size per node

### SQL Server Module Inputs

- `sql_server_name`: SQL Server name (randomized + checked for duplication)
- `sql_admin_user`: Admin username for SQL
- `sql_admin_password`: Admin password (sensitive)
- `sql_server_version`: SQL version (e.g., `12.0`)
- `sql_database_name`: SQL DB name
- `sql_sku_name`: Performance tier (e.g., `Basic`, `S0`)
- `sql_max_size_gb`: Maximum DB size in GB

---

## 🛡️ Edge Case Handling

| Case | Handling |
|------|----------|
| **Duplicate Names** | Azure CLI check for existing VM, AKS, SQL resources in the specified resource group |
| **Invalid SSH Key Path** | Raises error if the key path doesn't exist |
| **Public IP Conflicts** | Only one resource receives the shared IP |
| **Invalid Updates** | Validates SQL Server & AKS upgrades |
| **Sensitive Data** | Passwords and secrets marked as `sensitive` in Terraform |
| **Terraform Variable Format** | Python script ensures values are written with correct format (`quotes`, `bool`, `numeric`) |

---

## ⚙️ Scalability & Reliability

- **Scale Easily**: Add new modules or scale VM/node count.
- **Safe Deployments**: Modular design keeps resources isolated.
- **Idempotent Infrastructure**: Terraform ensures repeat runs are consistent and don’t duplicate resources.

---

## 🔄 How to Extend

1. **New Modules**: Add new modules (e.g., Storage, Load Balancer) under `modules/` and wire into `main.tf`.
2. **Multi-Env**: Add support in `main.py` to manage different `.tfvars` for environments like `dev`, `staging`, `prod`.
3. **CI/CD Integration**: Integrate with Terraform Cloud, GitHub Actions, or Azure DevOps pipelines.
4. **Validation Rules**: Enhance Python logic for regional VM size validation or cost estimation APIs.

---

## 🚀 Usage

```bash
# Clone the repository
git clone https://github.com/your-org/terraform-infra.git
cd terraform-infra

# Run the script to configure your environment
python3 main.py

# Deploy the infrastructure
terraform init
terraform plan
terraform apply
```

---

## Architecture Diagram

```bash
terraform-infra/
├── main.tf                  # Orchestration - controls modules and resources
├── variables.tf             # Input variable definitions
├── terraform.tfvars         # Populated dynamically with runtime values
├── outputs.tf               # Output values from resources
├── main.py                  # Python script with validations and input handling
├── modules/
│   ├── public_ip/           # Shared Public IP module
│   ├── vm/                  # Virtual Machine module
│   ├── k8s/                 # AKS Cluster module
│   └── sql/                 # SQL Server module
```

---
