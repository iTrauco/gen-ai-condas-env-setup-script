import os
import subprocess
import click

# Function to check if Conda is installed
def check_conda_installed():
    try:
        subprocess.run(["conda", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        return False
    return True

# Function to prompt the user to install Conda or exit
def prompt_install_or_exit():
    click.echo("Conda is not installed.")
    choice = click.prompt("Do you want to install Conda now? (yes/no)", type=str)
    if choice.lower() == "yes":
        install_conda()
    else:
        click.echo("Exiting...")
        raise SystemExit(1)

# Function to install Conda
def install_conda():
    click.echo("Installing Miniconda as an interactive shell...")
    subprocess.run(["wget", "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh", "-O", "miniconda.sh"], check=True)
    subprocess.run(["bash", "miniconda.sh", "-b", "-p", os.path.expanduser("~/miniconda")], check=True)
    os.remove("miniconda.sh")

    # Add Conda to PATH temporarily
    os.environ["PATH"] = os.path.expanduser("~/miniconda/bin") + ":" + os.environ["PATH"]

    # Initialize Conda
    subprocess.run(["conda", "init"], check=True)
    click.echo("Installation completed successfully.")

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
        create_new_env()
    elif choice > 0 and choice <= len(envs_list) - 1:
        selected_env = os.path.basename(envs_list[choice].strip().split()[0])
        subprocess.run(["conda", "activate", selected_env], check=True)
    else:
        click.echo("Invalid choice.")

# Function to create a new Conda environment
def create_new_env():
    click.echo("Creating a new Conda environment...")
    new_env_name = click.prompt("Please enter the name for the new Conda environment")
    subprocess.run(["conda", "create", "--name", new_env_name], check=True)
    click.echo(f"New environment '{new_env_name}' created successfully.")
    subprocess.run(["conda", "activate", new_env_name], check=True)

# Function to reinstall Conda
def reinstall_conda():
    click.echo("Reinstalling Conda...")
    subprocess.run(["rm", "-rf", os.path.expanduser("~/miniconda"), os.path.expanduser("~/.conda")], check=True)
    install_conda()
    reinit_shell()

# Function to uninstall Conda
def uninstall_conda():
    click.confirm("This action will uninstall Conda and its dependencies. Do you want to proceed?", abort=True)
    click.echo("Uninstalling Conda and its dependencies...")
    subprocess.run(["rm", "-rf", os.path.expanduser("~/miniconda"), os.path.expanduser("~/.conda")], check=True)
    click.echo("Uninstallation completed successfully.")
    reinit_shell()
    click.echo("Exiting...")
    raise SystemExit(0)

# Function to reinitialize the shell from the local .bashrc file
# Function to reinitialize the shell from the local .bashrc file
def reinit_shell():
    click.echo("Reinitializing shell...")
    subprocess.run(["bash", "-c", "source ~/.bashrc"])

@click.command()
def main():
    # Check if Conda is installed
    if not check_conda_installed():
        prompt_install_or_exit()

    # Prompt the user to select an action
    click.echo("What would you like to do?")
    click.echo("1. Use an existing Conda environment")
    click.echo("2. Create a new Conda environment")
    click.echo("3. Reinstall Conda")
    click.echo("4. Uninstall Conda and its dependencies")
    click.echo("5. Exit")
    choice = click.prompt("Enter your choice", type=int)

    if choice == 1:
        list_and_select_env()
    elif choice == 2:
        create_new_env()
    elif choice == 3:
        reinstall_conda()
    elif choice == 4:
        uninstall_conda()
    elif choice == 5:
        click.echo("Exiting...")
        raise SystemExit(0)
    else:
        click.echo("Invalid choice.")

if __name__ == "__main__":
    main()

