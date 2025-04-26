# Azure Infrastructure Automation with Terraform 🚀

This Terraform project automates the deployment of Azure infrastructure, including Virtual Machines (VMs), Kubernetes clusters (AKS), SQL Servers, and a shared public IP. It is built with modularity, scalability, edge case validation, and dynamic user-driven input in mind.

---

## 📦 Overview

This repository includes reusable modules to create:

- ✅ Virtual Machines (VMs)
- ✅ Kubernetes Cluster (AKS)
- ✅ SQL Server and Database
- ✅ Shared Public IP (dynamically assigned to one module)

A Python script (`main.py`) is provided to dynamically update `terraform.tfvars` based on user input and includes structured logging, validation, and basic error handling.

---

## ✅ Features

- **Shared Public IP Logic**: A central public IP resource is provisioned and passed to the selected module (`vm`, `k8s`, or `sql`) using a single variable.
- **Dynamic Configuration**: A Python CLI and optional FastAPI interface prompts for values and updates the `terraform.tfvars` automatically.
- **Modular Design**: Easily extend or reuse infrastructure by adding more modules.
- **Randomized Resource Naming**: Prevents name collisions using `random_string` logic.
- **Selective Deployment**: Only the selected module (based on user input) is deployed with a public IP.
- **Secure & Idempotent**: Follows Terraform best practices including sensitive value handling and idempotent deployment logic.
- **Validation & Edge Case Handling**:
  - Prevents creation of resources with existing names using Azure CLI.
  - SSH public key validation before proceeding.
  - SQL Server version and Kubernetes version upgrades with dry-run simulation.
- **Logging**: Uses structured logging instead of raw `print()` statements for consistent CLI feedback.
- **Extensible API**: A FastAPI interface enables dynamic updates to infrastructure through RESTful calls.

---

## 🧪 Bonus Requirements (Optional)

| Requirement           | Status  | Suggestions                                                                 |
|-----------------------|---------|------------------------------------------------------------------------------|
| Unit testing          | ❌      | Not yet implemented. Could add unit tests for `update_tfvars` and CLI logic.|
| Integration testing   | ❌      | Could use `subprocess` to simulate a dry run with Terraform (`terraform plan`).|
| Logging & error handling | ⚠️   | Basic logging implemented. Can improve using structured logging with log levels.|

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

| Case                     | Handling                                                                 |
|--------------------------|--------------------------------------------------------------------------|
| **Duplicate Names**      | Azure CLI check for existing VM, AKS, SQL resources in the resource group|
| **Invalid SSH Key Path** | Raises error if the key path doesn't exist                              |
| **Public IP Conflicts**  | Only one resource receives the shared IP                                |
| **Invalid Updates**      | Validates SQL Server & AKS version upgrades using live checks           |
| **Sensitive Data**       | Passwords and secrets marked as `sensitive` in Terraform                |
| **Terraform Formatting** | Python script ensures `terraform.tfvars` format is respected (quoted, bool, int)|

---

## 📌 Assumptions

The following assumptions were made in designing and implementing this solution:

1. **User Access & Permissions**  
   It is assumed that the user has appropriate Azure credentials and CLI access with sufficient permissions to create and manage resources.

2. **Azure CLI Installed**  
   The system executing the script must have the Azure CLI (`az`) installed and configured.

3. **SSH Key Exists**  
   Users are expected to provide a valid path to an existing SSH public key.

4. **Terraform Installed & Configured**  
   Terraform is expected to be installed and usable via the CLI. Backend configuration is assumed to be local unless extended.

5. **Resource Naming Convention**  
   Names are suffixed randomly to avoid naming collisions.

6. **Single Public IP Use Case**  
   Only one module uses the shared public IP at a time.

7. **Modular Inputs**  
   Inputs are passed through `.tfvars` and assumed to follow Terraform conventions.

8. **No Parallel Runs**  
   The system assumes no concurrent `terraform apply` runs occur in the same working directory.

---

## ⚙️ Scalability & Reliability

- **Scale Easily**: Add new modules or scale VM/node count through variables.
- **Safe Deployments**: Modular design keeps resources isolated and predictable.
- **Idempotent Infrastructure**: Terraform ensures consistent state on repeated runs.

---

## 🔄 How to Extend

1. **New Modules**: Add new modules under `modules/` and wire into `main.tf`.
2. **Multi-Env Support**: Extend Python to manage `dev.tfvars`, `prod.tfvars`, etc.
3. **API-driven Control**: Use FastAPI endpoints to create an infrastructure management UI or integrate with CI/CD.
4. **Enhanced Validation**: Add regional validation for VM sizes or estimated pricing.

---

## 🚀 Usage

```bash
# Clone the repository
git clone https://github.com/your-org/terraform-infra.git
cd terraform-infra

# Run the Python script to configure your environment
python3 main.py

# Deploy the infrastructure
terraform init
terraform plan
terraform apply
```

---

## 🗂️ Project Structure

```bash
terraform-infra/
├── main.tf                  # Root Terraform config - includes modules
├── variables.tf             # Input variable declarations
├── terraform.tfvars         # Auto-generated from CLI/API input
├── outputs.tf               # Output definitions
├── main.py                  # CLI script with logging and validation
├── api.py                   # Optional FastAPI interface
├── modules/
│   ├── public_ip/           # Shared Public IP logic
│   ├── vm/                  # VM definition
│   ├── k8s/                 # AKS definition
│   └── sql/                 # SQL Server definition
```

---

## 🧠 Tip

Use the Python CLI for guided configuration, or call the `/update-tfvars` API to plug this into a self-service UI.

---
