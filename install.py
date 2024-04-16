import os
import subprocess
import click

# Function to check if Conda is installed
def check_conda_installed():
    try:
        subprocess.run(["conda", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        click.echo("Conda is not installed. Please install Conda first.")
        raise SystemExit(1)

# Function to list the ten most recently used Conda environments
def list_recent_envs():
    click.echo("Ten most recently used Conda environments:")
    envs_info = subprocess.run(["conda", "info", "--envs"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    envs_list = envs_info.stdout.strip().split("\n")
    for env_path in envs_list[1:]:
        env_name = os.path.basename(env_path.strip().split()[0])
        last_used = subprocess.run(["ls", "-lt", f"{env_path.strip().split()[0]}/conda-meta"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout.splitlines()[1].split()[5:]
        last_used = " ".join(last_used)
        click.echo(f"Environment: {env_name} | Last used: {last_used}")

@click.command()
def main():
    # Check if Conda is installed
    check_conda_installed()
    
    click.echo("What would you like to do?")
    click.echo("1. Use an existing Conda environment")
    click.echo("2. Create a new Conda environment")
    click.echo("3. Install Conda for the first time")
    click.echo("4. Reinstall Conda")
    click.echo("5. Uninstall Conda and its dependencies")
    click.echo("6. Dev Mode - Destroy all Conda environments")
    click.echo("7. Exit")
    install_choice = click.prompt("Enter your choice", type=int)

    if install_choice == 1:
        # Use an existing Conda environment
        try:
            envs_info = subprocess.run(["conda", "info", "--envs"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if not envs_info.stdout.strip():
                click.echo("No Conda environments exist on your system.")
                no_env_choice = click.prompt("What would you like to do? (1: Create a new Conda environment, 2: Exit)", type=int)
                if no_env_choice == 1:
                    click.echo("Creating a new Conda environment...")
                    new_env_name = click.prompt("Please enter the name for the new Conda environment")
                    subprocess.run(["conda", "create", "--name", new_env_name], check=True)
                    click.echo(f"New environment '{new_env_name}' created successfully.")
                elif no_env_choice == 2:
                    click.echo("Exiting...")
                    return
                else:
                    click.echo("Invalid choice.")
                    return
                return

            list_recent_envs()
            selected_env = click.prompt("Please enter the name of the environment you want to activate")
            subprocess.run(["conda", "activate", selected_env], check=True)
        except subprocess.CalledProcessError as e:
            click.echo(e.stderr)
    elif install_choice == 2:
        # Create a new Conda environment
        click.echo("Creating a new Conda environment...")
        new_env_name = click.prompt("Please enter the name for the new Conda environment")
        subprocess.run(["conda", "create", "--name", new_env_name], check=True)
        click.echo(f"New environment '{new_env_name}' created successfully.")
    elif install_choice == 3:
        # Install Conda for the first time
        click.echo("Installing Miniconda as an interactive shell...")
        subprocess.run(["wget", "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh", "-O", "miniconda.sh"], check=True)
        subprocess.run(["bash", "miniconda.sh", "-b", "-p", os.path.expanduser("~/miniconda")], check=True)
        os.remove("miniconda.sh")

        # Add Conda to PATH temporarily
        os.environ["PATH"] = os.path.expanduser("~/miniconda/bin") + ":" + os.environ["PATH"]

        # Initialize Conda
        subprocess.run(["conda", "init"], check=True)
        click.echo("Installation completed successfully.")
    elif install_choice == 4:
        # Reinstall Conda
        click.echo("Uninstalling Conda and its dependencies...")
        os.system(f"rm -rf {os.path.expanduser('~/miniconda')}")
        os.system(f"rm -rf {os.path.expanduser('~/.conda')}")

        # Remove Conda from PATH
        os.environ["PATH"] = ":".join(filter(lambda x: x != os.path.expanduser("~/miniconda/bin"), os.environ["PATH"].split(":")))

        # Install Conda as an interactive shell
        click.echo("Installing Miniconda as an interactive shell...")
        subprocess.run(["wget", "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh", "-O", "miniconda.sh"], check=True)
        subprocess.run(["bash", "miniconda.sh", "-b", "-p", os.path.expanduser("~/miniconda")], check=True)
        os.remove("miniconda.sh")

        # Add Conda to PATH temporarily
        os.environ["PATH"] = os.path.expanduser("~/miniconda/bin") + ":" + os.environ["PATH"]

        # Initialize Conda
        subprocess.run(["conda", "init"], check=True)
        click.echo("Reinstallation completed successfully.")
    elif install_choice == 5:
        # Uninstall Conda and its dependencies
        click.echo("Uninstalling Conda and its dependencies...")
        os.system(f"rm -rf {os.path.expanduser('~/miniconda')}")
        os.system(f"rm -rf {os.path.expanduser('~/.conda')}")

        # Remove Conda from PATH
        os.environ["PATH"] = ":".join(filter(lambda x: x != os.path.expanduser("~/miniconda/bin"), os.environ["PATH"].split(":")))

        click.echo("Uninstallation completed successfully.")
    elif install_choice == 6:
        # Dev Mode - Destroy all Conda environments
        click.echo("This action will destroy all local Conda environments.")
        click.confirm("Do you want to proceed?", abort=True)
        subprocess.run(["sudo", "conda", "env", "remove", "--all"], check=True)
        click.echo("All Conda environments have been destroyed.")
    elif install_choice == 7:
        # Exit the script
        click.echo("Exiting...")
        return
    else:
        click.echo("Invalid choice.")

if __name__ == "__main__":
    main()

