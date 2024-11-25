import subprocess
from dotenv import dotenv_values

# Secret name in Modal
SECRET_NAME = "custom_secret"
ENV_FILE_PATH = ".env"

def load_env_file(file_path=ENV_FILE_PATH):
    """
    Load environment variables from a .env file.

    Args:
        file_path (str): Path to the .env file.

    Returns:
        dict: Dictionary of environment variables from the file.
    """
    try:
        return dotenv_values(file_path)
    except Exception as e:
        print(f"❌ Error loading .env file: {e}")
        return {}

def create_modal_secret(secret_name, env_vars):
    """
    Create or update a Modal secret with specified environment variables.

    Args:
        secret_name (str): Name of the Modal secret.
        env_vars (dict): Dictionary of environment variables to include.
    """
    # Build the Modal CLI command
    secret_command = ["modal", "secret", "create", secret_name, "--force"]
    for key, value in env_vars.items():
        if value:  # Exclude empty values
            secret_command.append(f"{key}={value}")

    # Run the command
    try:
        print(f"🔄 Creating Modal secret '{secret_name}' with all variables from the .env file...")
        subprocess.run(secret_command, check=True)
        print(f"✅ Modal secret '{secret_name}' created/updated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating Modal secret: {e}")
        exit(1)


if __name__ == "__main__":
    # Load environment variables from .env file
    env_vars = load_env_file()

    if not env_vars:
        print("⚠️ No variables found in the .env file.")
    else:
        # Create or update the Modal secret
        create_modal_secret(SECRET_NAME, env_vars)
