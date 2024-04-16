#!/bin/bash

# Function to list all available Conda environments
list_envs() {
    echo "Available Conda environments:"
    conda env list | awk '{print $1}'
}

# Function to prompt the user to activate an existing environment
activate_existing_env() {
    echo "Please enter the name of the existing Conda environment:"
    read env_name

    # Activate the existing Conda environment
    conda activate $env_name

    if [ $? -eq 0 ]; then
        echo "Environment '$env_name' activated successfully."
        echo "Installation completed successfully."
    else
        echo "Error: Failed to activate environment '$env_name'."
    fi
}

echo "What would you like to do?"
echo "1. Install Conda for the first time"
echo "2. Reinstall Conda"
echo "3. Uninstall Conda and its dependencies"
echo "4. Use an existing Conda environment"
read install_choice

case $install_choice in
    1) 
        # Install Conda for the first time
        echo "Installing Miniconda as an interactive shell..."
        wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
        bash miniconda.sh -b -p $HOME/miniconda
        rm miniconda.sh

        # Add Conda to PATH temporarily
        export PATH="$HOME/miniconda/bin:$PATH"

        # Initialize Conda
        conda init

        echo "Installation completed successfully."
        ;;
    2) 
        # Reinstall Conda
        echo "Uninstalling Conda and its dependencies..."
        rm -rf $HOME/miniconda
        rm -rf $HOME/.conda

        # Remove Conda from PATH
        export PATH=$(echo $PATH | tr ':' '\n' | grep -v "$HOME/miniconda/bin" | tr '\n' ':')
        export PATH="${PATH%:}"

        # Source .bashrc to reinitialize shell
        source ~/.bashrc

        # Install Conda as an interactive shell
        echo "Installing Miniconda as an interactive shell..."
        wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
        bash miniconda.sh -b -p $HOME/miniconda
        rm miniconda.sh

        # Add Conda to PATH temporarily
        export PATH="$HOME/miniconda/bin:$PATH"

        # Initialize Conda
        conda init

        echo "Reinstallation completed successfully."
        ;;
    3) 
        # Uninstall Conda and its dependencies
        echo "Uninstalling Conda and its dependencies..."
        rm -rf $HOME/miniconda
        rm -rf $HOME/.conda

        # Remove Conda from PATH
        export PATH=$(echo $PATH | tr ':' '\n' | grep -v "$HOME/miniconda/bin" | tr '\n' ':')
        export PATH="${PATH%:}"

        # Source .bashrc to reinitialize shell
        source ~/.bashrc

        echo "Uninstallation completed successfully."
        ;;
    4) 
        # Use an existing Conda environment
        activate_existing_env
        ;;
    *) 
        echo "Invalid choice."
        ;;
esac

# If Conda is installed or reinstalled, prompt the user to choose the next action
if [[ $install_choice == 1 || $install_choice == 2 ]]; then
    echo "What would you like to do now?"
    echo "1. Set up a new Conda environment"
    echo "2. Activate an existing Conda environment"
    echo "3. List all available Conda environments and select one to activate"
    read next_action

    case $next_action in
        1) 
            # Set up a new Conda environment
            echo "Please enter the name for the new Conda environment:"
            read new_env_name
            echo "Creating a new Conda environment '$new_env_name'..."
            conda create --name $new_env_name
            echo "New environment '$new_env_name' created successfully."
            ;;
        2) 
            # Activate an existing Conda environment
            activate_existing_env
            ;;
        3) 
            # List all available Conda environments and select one to activate
            list_envs
            echo "Please enter the name of the environment you want to activate:"
            read selected_env
            conda activate $selected_env
            ;;
        *) 
            echo "Invalid choice."
            ;;
    esac
fi

