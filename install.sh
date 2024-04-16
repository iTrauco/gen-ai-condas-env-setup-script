#!/bin/bash

# Function to check if Conda is installed
check_conda_installed() {
    if ! command -v conda &> /dev/null; then
        echo "Conda is not installed. Please install Conda first."
        exit 1
    fi
}

# Function to list the ten most recently used Conda environments
list_recent_envs() {
    echo "Ten most recently used Conda environments:"
    conda info --envs | grep '^ *' | awk '{print $1}' | while read -r env_path; do
        env_name=$(basename $env_path)
        last_used=$(ls -lt $env_path/conda-meta | awk 'NR==2{print $6, $7, $8}')
        echo "Environment: $env_name | Last used: $last_used"
    done | head -n 10
}

# Function to create a new Conda environment
create_new_env() {
    echo "Please enter the name for the new Conda environment:"
    read new_env_name
    echo "Creating a new Conda environment '$new_env_name'..."
    conda create --name $new_env_name
    echo "New environment '$new_env_name' created successfully."
}

# Function to destroy all Conda environments
destroy_all_envs() {
    echo "This action will destroy all local Conda environments."
    echo "Please enter your sudo password to proceed:"
    sudo conda env remove --all
    if [ $? -eq 0 ]; then
        echo "All Conda environments have been destroyed."
    else
        echo "Failed to destroy all Conda environments."
    fi
}

# Check if Conda is installed
check_conda_installed

echo "What would you like to do?"
echo "1. Use an existing Conda environment"
echo "2. Create a new Conda environment"
echo "3. Install Conda for the first time"
echo "4. Reinstall Conda"
echo "5. Uninstall Conda and its dependencies"
echo "6. Dev Mode - Destroy all Conda environments"
echo "7. Exit"
read install_choice

case $install_choice in
    1) 
        # Use an existing Conda environment
        if ! conda info --envs | grep -q "^ *"; then
            echo "No Conda environments exist on your system."
            echo "What would you like to do?"
            echo "1. Create a new Conda environment"
            echo "2. Exit"
            read no_env_choice

            case $no_env_choice in
                1) 
                    # Create a new Conda environment
                    create_new_env
                    ;;
                2)
                    # Exit the script
                    echo "Exiting..."
                    exit
                    ;;
                *) 
                    echo "Invalid choice."
                    ;;
            esac
            exit
        fi

        list_recent_envs
        echo "Please enter the name of the environment you want to activate:"
        read selected_env
        conda activate $selected_env
        ;;
    2)
        # Create a new Conda environment
        create_new_env
        ;;
    3) 
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
    4) 
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
    5) 
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
    6) 
        # Dev Mode - Destroy all Conda environments
        destroy_all_envs
        ;;
    7) 
        # Exit the script
        echo "Exiting..."
        exit
        ;;
    *) 
        echo "Invalid choice."
        ;;
esac

