import re

def update_variable_default(tf_content, var_name, new_value):
    # Handles both string and numeric values
    if isinstance(new_value, str):
        new_value_str = f'"{new_value}"'
    else:
        new_value_str = str(new_value)

    pattern = rf'(variable\s+"{var_name}"\s*\{{.*?default\s*=\s*)(.*?)(\s*[\r\n]+.*?)\}}'
    repl = rf'\1{new_value_str}\3}}'
    return re.sub(pattern, repl, tf_content, flags=re.DOTALL)

def main():
    tf_file_path = "variables.tf"

    # Take input from user
    location = input("Enter Azure location (e.g., eastus): ").strip()
    vm_size = input("Enter VM size (e.g., Standard_B2s): ").strip()
    vm_count = input("Enter VM count (e.g., 2): ").strip()

    try:
        vm_count = int(vm_count)
    except ValueError:
        print("❌ VM count must be a number.")
        return

    # Read the file
    with open(tf_file_path, "r") as file:
        content = file.read()

    # Update values
    content = update_variable_default(content, "location", location)
    content = update_variable_default(content, "vm_size", vm_size)
    content = update_variable_default(content, "vm_count", vm_count)

    # Write back to the file
    with open(tf_file_path, "w") as file:
        file.write(content)

    print("✅ variables.tf updated successfully.")

if __name__ == "__main__":
    main()
