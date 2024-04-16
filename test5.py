import os
import subprocess
import click
import shutil
import sys

# Global variable to hold the name of the selected or created environment
selected_env_name = None
# Function to activate Conda in the shell
def activate_conda():
    try:
        os.environ["PATH"] = "~/miniconda/bin:" + os.environ["PATH"]
        os.environ["CONDA_EXE"] = "~/miniconda/bin/conda"
        os.environ["CONDA_PREFIX"] = "~/miniconda"
        os.environ["CONDA_DEFAULT_ENV"] = "base"
        os.environ["CONDA_SHLVL"] = "1"
        os.environ["_CE_M"] = ""
        os.environ["_CE_CONDA"] = ""
    except Exception as e:
        click.echo(f"Error activating Conda: {e}")
        return False
    return True



# Activate Conda when the script is run
if not activate_conda():
    sys.exit(1)

    # Function to manually switch between environments
def switch_env():
    env_name = click.prompt("Enter the name of the environment you want to switch to")
    try:
        activate_env_globally(env_name)
    except Exception as e:
        click.echo(f"Error switching to environment '{env_name}': {e}")
        return False
    return True

# Function to activate a Conda environment in the local shell
def activate_conda_env(env_name):
    global selected_env_name
    selected_env_name = env_name
    try:
        subprocess.run(f"conda activate {env_name}", shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

# Function to prompt the user to initialize Conda
def prompt_conda_init():
    click.echo("Before proceeding, please initialize Conda by running:")
    click.echo("$ conda init")
    click.echo("Once Conda is initialized, you can run this script again.")
    click.echo("Exiting...")
    raise SystemExit(1)

# Function to check if Conda is initialized and return its installation directory
def check_conda_initialized():
    return os.environ.get("CONDA_EXE")

# Function to check if Conda is installed and return its installation directory
def check_conda_installed():
    try:
        result = subprocess.run(
            ["which", "conda"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        conda_path = result.stdout.strip()
        return conda_path if conda_path else None
    except subprocess.CalledProcessError:
        return None

# Function to install Miniconda
def install_conda():
    click.echo("Installing Miniconda as an interactive shell...")

    # Check if Miniconda is already installed
    existing_conda_path = check_conda_installed()
    if existing_conda_path:
        click.echo(f"Miniconda is already installed at: {existing_conda_path}")
        return existing_conda_path

    # Download and install Miniconda
    subprocess.run(
        ["wget", "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh", "-O", "miniconda.sh"],
        check=True,
    )
    subprocess.run(
        ["bash", "miniconda.sh", "-b", "-p", os.path.expanduser("~/miniconda")], check=True
    )
    os.remove("miniconda.sh")

    # Add Conda to PATH temporarily
    os.environ["PATH"] = os.path.expanduser("~/miniconda/bin") + ":" + os.environ["PATH"]

    # Initialize Conda for bash shell
    subprocess.run(["conda", "init", "bash"], check=True)

    click.echo("Installation completed successfully.")
    return os.path.expanduser("~/miniconda")

# Function to prompt the user to install Conda or exit
def prompt_install_or_exit():
    click.echo("Conda is not installed.")
    choice = click.prompt("Do you want to install Conda now? (yes/no)", type=str)
    if choice.lower().startswith("y"):
        install_conda()
    else:
        click.echo("Exiting...")
        raise SystemExit(1)

# Function to activate a Conda environment globally by name
def activate_env_globally(env_name):
    click.echo(f"Activating environment '{env_name}' globally...")
    try:
        os.environ["CONDA_DEFAULT_ENV"] = env_name
        click.echo(f"Environment '{env_name}' activated globally successfully.")
    except Exception as e:
        click.echo(f"Error: {e}")

# Function to list all Conda environments and prompt the user to select one
def list_and_select_env():
    envs_info = subprocess.run(["conda", "info", "--envs"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    envs_list = envs_info.stdout.strip().split("\n")
    click.echo("Available Conda environments:")
    for i, env_path in enumerate(envs_list[1:]):
        env_name = os.path.basename(env_path.strip().split()[0])
        click.echo(f"{i+1}. {env_name}")
    choice = click.prompt("Enter the number of the environment you want to use or '0' to create a new environment", type=int)
    if choice == 0:
        create_and_activate_new_env()  # Create and activate new environment
    elif choice > 0 and choice <= len(envs_list) - 1:
        selected_env = os.path.basename(envs_list[choice].strip().split()[0])
        activate_env_globally(selected_env)  # Activate selected existing environment globally
    else:
        click.echo("Invalid choice.")

# Function to create a new Conda environment and activate it globally
def create_and_activate_new_env():
    click.echo("Creating a new Conda environment...")
    new_env_name = click.prompt("Please enter the name for the new Conda environment")
    try:
        subprocess.run(["conda", "create", "--name", new_env_name], check=True)
        click.echo(f"New environment '{new_env_name}' created successfully.")
        activate_env_globally(new_env_name)  # Activate newly created environment globally
    except subprocess.CalledProcessError as e:
        click.echo(f"Error: {e}")

# Function to reinstall Conda
def reinstall_conda():
    click.echo("Reinstalling Conda...")
    subprocess.run(["rm", "-rf", os.path.expanduser("~/miniconda"), os.path.expanduser("~/.conda")], check=True)
    install_conda()
    activate_env_globally("base")  # Activate base environment
    raise SystemExit(0)

# Function to uninstall Conda
def uninstall_conda():
    click.confirm("This action will uninstall Conda and its dependencies. Do you want to proceed?", abort=True)
    click.echo("Uninstalling Conda and its dependencies...")

    # Remove the Miniconda installation directory
    miniconda_dir = os.path.expanduser("~/miniconda")
    if os.path.exists(miniconda_dir):
        shutil.rmtree(miniconda_dir)

    # Remove the user-specific configuration directory
    shutil.rmtree(os.path.expanduser("~/.conda"), ignore_errors=True)

    # Remove any Conda-related initialization scripts from .bashrc or .bash_profile
    bash_files = ["~/.bashrc", "~/.bash_profile"]
    for file_path in bash_files:
        full_path = os.path.expanduser(file_path)
        if os.path.exists(full_path):
            with open(full_path, "r") as f:
                file_content = f.read()
            if "conda initialize" in file_content:
                subprocess.run(["sed", "-i", "/# >>> conda initialize >>>/,/# <<< conda initialize <<</d", full_path],
                               check=True)

    click.echo("Uninstallation completed successfully.")
    reinit_shell()
    click.echo("Exiting...")
    raise SystemExit(0)

# Function to reinitialize the shell from the local .bashrc file
def reinit_shell():
    click.echo("Reinitializing shell...")
    subprocess.run(["bash", "-c", "source ~/.bashrc"])


@click.command()
def main():
    # Check if Conda is initialized
    if not check_conda_initialized():
        prompt_conda_init()

    # Check if Conda is installed
    existing_conda_path = check_conda_installed()
    if existing_conda_path:
        click.echo(f"Miniconda is already installed at: {existing_conda_path}")
    else:
        prompt_install_or_exit()

    # Activate base environment after installation or reinstallation
    activate_env_globally("base")

    # Prompt the user to select an action
    click.echo("What would you like to do?")
    click.echo("1. Use an existing Conda environment")
    click.echo("2. Create a new Conda environment")
    click.echo("3. Reinstall Conda")
    click.echo("4. Uninstall Conda and its dependencies")
    click.echo("5. Manually switch between environments")
    click.echo("6. Exit")
    choice = click.prompt("Enter your choice", type=int)

    if choice == 1:
        list_and_select_env()
    elif choice == 2:
        create_and_activate_new_env()
    elif choice == 3:
        reinstall_conda()
    elif choice == 4:
        uninstall_conda()
    elif choice == 5:
        switch_env()
    elif choice == 6:
        click.echo("Exiting...")
        raise SystemExit(0)
    else:
        click.echo("Invalid choice.")


if __name__ == "__main__":
    main()
