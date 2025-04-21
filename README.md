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

## ✅ Features

- **Shared Public IP Logic**: A central public IP resource is provisioned and passed to the selected module (`vm`, `k8s`, or `sql`) using a single variable.
- **Dynamic Configuration**: A Python script prompts for values and updates the `terraform.tfvars` automatically.
- **Modular Design**: Easily extend or reuse infrastructure by adding more modules.
- **Randomized Resource Naming**: Prevents name collisions using `random_string`.
- **Selective Deployment**: Only the selected module (based on user input) is deployed with a public IP.
- **Secure & Idempotent**: Follows Terraform best practices including sensitive value handling and idempotent design.

---

## 🧾 Inputs

### General Inputs (used by all modules)
- `location`: Azure region (e.g., `eastus`)
- `resource_group_name`: Azure resource group
- `admin_username`: Admin username for VMs, AKS, SQL
- `ssh_public_key`: Path to SSH public key
- `assign_public_ip_to`: Which module gets the shared public IP (`vm`, `k8s`, or `sql`)
- `public_ip_name`: Name for the shared public IP

### VM Module Inputs
- `vm_size`: Size of the VM (e.g., `Standard_B2s`)
- `subnet_id`: Azure subnet ID

### Kubernetes Module Inputs
- `cluster_name`: AKS cluster name
- `dns_prefix`: DNS prefix for AKS
- `kubernetes_version`: Kubernetes version (e.g., `1.29.0`)
- `node_count`: Number of worker nodes
- `node_vm_size`: VM size per node

### SQL Server Module Inputs
- `sql_server_name`: SQL Server name
- `sql_server_version`: SQL version (e.g., `12.0`)
- `sql_database_name`: SQL DB name
- `sql_admin_username`: Admin username for SQL
- `sql_admin_password`: Admin password (sensitive)
- `sql_sku_name`: Performance tier (e.g., `Basic`, `S0`)
- `sql_max_size_gb`: Maximum DB size in GB

---

## 🛡️ Edge Case Handling

- **Name Collisions**: Prevented using randomized suffixes.
- **Invalid Inputs**: Python script validates inputs before writing them to `tfvars`.
- **Public IP Waste**: Only one resource receives a public IP based on logic.
- **Sensitive Data Protection**: Passwords marked as `sensitive`.

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


**## Architecture Diagram**

```bash
terraform-infra/
├── main.tf                  # Orchestration - controls modules and resources
├── variables.tf             # Input variable definitions
├── terraform.tfvars         # Populated dynamically with runtime values
├── outputs.tf               # Output values from resources
├── main.py                  # Python script to dynamically update tfvars
├── modules/
│   ├── public_ip/           # Shared Public IP module
│   ├── vm/                  # Virtual Machine module
│   ├── k8s/                 # AKS Cluster module
│   └── sql/                 # SQL Server module
