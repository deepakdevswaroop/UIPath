from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
import subprocess
import os
import logging
from typing import Optional

app = FastAPI()
logging.basicConfig(level=logging.INFO)

# === CONFIG ===
API_TOKEN = os.getenv("API_AUTH_TOKEN", "supersecrettoken")
TFVARS_PATH = "terraform.tfvars"

# === AUTH ===
def authenticate(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Invalid auth format")
    token = authorization.split(" ")[1]
    if token != API_TOKEN:
        raise HTTPException(status_code=403, detail="Unauthorized")

# === UTILS ===
def check_existing_resource(resource_group, resource_type, name):
    try:
        result = subprocess.run(
            ["az", resource_type, "show", "--name", name, "--resource-group", resource_group],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        logging.warning(f"Could not verify resource existence: {e}")
        return False

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

def run_terraform_command(command):
    subprocess.run(["terraform", "init"], check=True)
    subprocess.run(["terraform", command], check=True)

# === SCHEMAS ===
class VMRequest(BaseModel):
    vm_count: int
    vm_size: str
    vm_name_prefix: str
    location: str
    resource_group_name: str
    admin_username: str
    ssh_public_key: str
    assign_public_ip_to: Optional[str] = "vm"
    public_ip_name: Optional[str]

class K8sRequest(BaseModel):
    cluster_name: str
    dns_prefix: str
    kubernetes_version: str
    node_count: int
    node_vm_size: str
    location: str
    resource_group_name: str
    admin_username: str
    ssh_public_key: str
    assign_public_ip_to: Optional[str] = "k8s"
    public_ip_name: Optional[str]

class SQLRequest(BaseModel):
    sql_server_name: str
    sql_admin_user: str
    sql_admin_password: str
    location: str
    resource_group_name: str
    assign_public_ip_to: Optional[str] = "sql"
    public_ip_name: Optional[str]

class SQLUpdateRequest(BaseModel):
    sql_server_name: str
    resource_group_name: str
    new_version: str

class K8sUpgradeRequest(BaseModel):
    new_version: str

# === ROUTES ===
@app.post("/create/vm", dependencies=[Depends(authenticate)])
def create_vm(payload: VMRequest):
    if check_existing_resource(payload.resource_group_name, "vm", payload.vm_name_prefix):
        raise HTTPException(status_code=400, detail="VM already exists.")
    update_tfvars(TFVARS_PATH, payload.dict())
    return {"message": "✅ VM tfvars updated."}

@app.post("/create/k8s", dependencies=[Depends(authenticate)])
def create_k8s(payload: K8sRequest):
    if check_existing_resource(payload.resource_group_name, "aks", payload.cluster_name):
        raise HTTPException(status_code=400, detail="AKS Cluster already exists.")
    update_tfvars(TFVARS_PATH, payload.dict())
    return {"message": "✅ AKS tfvars updated."}

@app.post("/create/sql", dependencies=[Depends(authenticate)])
def create_sql(payload: SQLRequest):
    if check_existing_resource(payload.resource_group_name, "sql", payload.sql_server_name):
        raise HTTPException(status_code=400, detail="SQL Server already exists.")
    update_tfvars(TFVARS_PATH, payload.dict())
    return {"message": "✅ SQL tfvars updated."}

@app.post("/update/sql-version", dependencies=[Depends(authenticate)])
def update_sql_version(payload: SQLUpdateRequest):
    if not check_existing_resource(payload.resource_group_name, "sql", payload.sql_server_name):
        raise HTTPException(status_code=404, detail="SQL Server not found.")
    try:
        subprocess.run(
            ["az", "sql", "server", "update",
             "--name", payload.sql_server_name,
             "--resource-group", payload.resource_group_name,
             "--version", payload.new_version],
            check=True
        )
        return {"message": f"✅ SQL Server updated to version {payload.new_version}"}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Update failed: {e.stderr}")

@app.post("/upgrade/k8s-version", dependencies=[Depends(authenticate)])
def upgrade_k8s_version(payload: K8sUpgradeRequest):
    update_tfvars(TFVARS_PATH, {"kubernetes_version": payload.new_version})
    return {"message": f"✅ Kubernetes version updated in tfvars."}

@app.post("/terraform/plan", dependencies=[Depends(authenticate)])
def terraform_plan():
    try:
        run_terraform_command("plan")
        return {"message": "✅ Terraform plan executed."}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Terraform plan failed: {e}")

@app.post("/terraform/apply", dependencies=[Depends(authenticate)])
def terraform_apply():
    try:
        run_terraform_command("apply")
        return {"message": "✅ Terraform apply executed."}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Terraform apply failed: {e}")


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API is running"}
