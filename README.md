# UIPath

# Azure Infrastructure Automation with Terraform

This Terraform project automates the deployment of Azure infrastructure, including Virtual Machines (VMs), Kubernetes clusters (AKS), and SQL Servers. The project is designed for flexibility and modularity, making it easier to manage cloud resources in a structured, automated manner.

## Overview

This repository provides a set of reusable Terraform modules to create the following Azure resources:

- **Virtual Machines (VMs)**
- **Kubernetes Cluster (AKS)**
- **SQL Server and Database**

Each module is flexible, allowing dynamic input parameters to customize the resources based on your requirements. The Python script (`main.py`) interacts with these modules by dynamically updating `terraform.tfvars` with runtime values entered by the user.

## Advantages

1. **Modularity**: The infrastructure components (VMs, Kubernetes, SQL Server) are separated into distinct modules. This allows for easy management, reusability, and scalability of individual components.
2. **Dynamic Inputs**: The Python script prompts the user for input values (e.g., VM size, Kubernetes version, SQL Server name) and updates the `terraform.tfvars` file accordingly, making it easy to modify and manage configurations.
3. **Randomized and Unique Naming**: For resources like VMs and Kubernetes clusters, a unique suffix is generated, ensuring no name collisions, which is critical for avoiding conflicts in large deployments.
4. **Public IP Assignment**: The modules support the optional assignment of public IPs to VMs, Kubernetes clusters, and SQL Servers, providing flexibility in how you manage external access to your resources.
5. **Error Handling**: The Python script ensures that the user’s input is valid and updates the `tfvars` file correctly, preventing issues in Terraform deployments.

## Inputs

Each module accepts specific inputs through the `terraform.tfvars` file. These variables are categorized based on the resource type.

### General Inputs

- `location`: Azure region (e.g., `eastus`, `westeurope`).
- `resource_group_name`: Name of the resource group.
- `admin_username`: The admin username for VMs, Kubernetes, and SQL.
- `ssh_public_key`: Path to the SSH public key (required for VMs and Kubernetes).
- `assign_public_ip_to`: Specifies which resource (VM, Kubernetes, or SQL) should be assigned a public IP.
- `public_ip_name`: Name of the public IP to be assigned.

### VM Module Inputs

- `vm_count`: Number of VMs to deploy.
- `vm_size`: Size of the VMs (e.g., `Standard_B2s`).
- `vm_name_prefix`: Prefix for the VM names (random suffix is added to ensure uniqueness).

### Kubernetes Module Inputs

- `cluster_name`: Name of the Kubernetes cluster.
- `dns_prefix`: DNS prefix for the Kubernetes cluster.
- `kubernetes_version`: Version of Kubernetes to deploy (e.g., `1.29.0`).
- `node_count`: Number of worker nodes.
- `node_vm_size`: Size of the VMs for the worker nodes.

### SQL Server Module Inputs

- `sql_server_name`: Name of the SQL Server instance.
- `sql_server_version`: Version of SQL Server to deploy (e.g., `12.0`, `14.0`). *(NEW)*
- `sql_database_name`: Name of the SQL Database.
- `sql_admin_username`: Admin username for SQL Server.
- `sql_admin_password`: Admin password for SQL Server (sensitive).
- `sql_sku_name`: SKU for the SQL Server (e.g., `Basic`, `S0`).
- `sql_max_size_gb`: Maximum size of the database in GB.

## Edge Cases Covered

- **Duplicate Names**: The code generates a unique suffix for each resource, preventing name collisions in a large deployment.
- **Resource Availability**: If a resource cannot be created due to region constraints (e.g., insufficient resources in the selected Azure region), Terraform will handle this with appropriate error messages.
- **Sensitive Information**: SQL admin passwords are marked as sensitive to avoid exposing them in the Terraform output.
- **Public IP Assignment**: Public IPs are only created if the user selects the option to assign them to a specific resource (VM, Kubernetes, or SQL), ensuring resources are only provisioned as needed.

## Scalability and Reliability

- **Scalability**: The Terraform modules are scalable by allowing for the dynamic addition of resources. You can adjust the number of VMs, worker nodes in the Kubernetes cluster, and the size of databases at runtime. You can also easily extend the infrastructure by adding new modules or resources.
- **Reliability**: By using modular design and separating concerns (e.g., VM creation, Kubernetes cluster, SQL Server), the infrastructure is less prone to errors during deployment. Each module is independent and reusable, reducing the chances of failure during updates.
- **Idempotency**: Terraform ensures that running the same configuration multiple times will not result in duplicated resources or unintended changes. This makes your infrastructure management reliable and predictable.
- **Error Handling**: The Python script and Terraform configuration ensure that any errors (like invalid input or missing variables) are handled gracefully and are communicated to the user.

## Novelty

This solution is novel because it combines multiple Terraform modules with a Python script that dynamically updates configuration files (`terraform.tfvars`). It allows for:

- **Automated Deployment**: Instead of manually editing Terraform files, users can input values at runtime, making the process more streamlined.
- **Randomized Resource Naming**: The automatic generation of unique resource names ensures that resources can be safely created in any environment without the risk of naming collisions.

## How to Extend

1. **Add New Modules**: You can extend this infrastructure by adding more modules to provision other Azure resources, such as storage accounts, virtual networks, or load balancers. New modules can be added in the `modules/` directory, and the main Terraform files can be updated to include them.
2. **Multiple Environments**: You can extend the `main.py` script to handle multiple environments (e.g., `dev`, `staging`, `prod`) by prompting the user for environment-specific values or reading from different `.tfvars` files.
3. **Advanced Networking**: Integrating virtual networks, subnets, and network security groups into the modules would provide more control over the networking configuration for VMs, Kubernetes, and SQL Server.
4. **Terraform Cloud Integration**: For better collaboration and automation, you can integrate the setup with Terraform Cloud or another CI/CD tool to automate the deployment process.

## Usage

1. Clone this repository to your local machine.
2. Ensure that you have Terraform and Python installed.
3. Run `main.py` to prompt for inputs and automatically update `terraform.tfvars` based on your selections.
4. Run Terraform commands to apply the infrastructure:

```bash
terraform init
terraform plan
terraform apply
