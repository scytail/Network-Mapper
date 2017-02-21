# NetworkMap

A python script that visually maps network configurations automatically.

**Goal** 

This software will scan provided firewall and interface configurations and automatically generate a visual representations of the network for better understanding of how network is configured.

The goal is to automate this visualization so that users can quickly and easily create easy-to-read visual maps of the network without having to devote a lot of time to manually drawing the network maps.

This will also help less-educated network users to quickly understand and visualize how the network is interconnected with its various components, and provide a deeper understanding of the network, with minimal effort and time.

**Technology Overview**

This project is built upon the Python 3.3 programming language, and uses configuration files (in raw text file format) obtained from the Cisco FWSM 4.1 Command Syntax.

**Prerequisites**

- Python 3.3 (or above)
    - pip
- virtualenv
- graphviz
- internet connection (for set up)

## Getting Started

**Installation**

1. Create a folder to house the script and its files somewhere in your file system (where it is placed is user preference)
2. Move the files (or extract the files if they are in a zip file) into the folder that you created
3. If Python is not installed, then download and install Python from the [Python website](https://www.python.org/downloads/).
    - When installing, make *SURE* the installer is told to add python to the path variable (the checkbox for this is by default unchecked on some systems). The option for this is usually on the first screen of the installer executable.
4. Navigate to the directory that the script will execute from in a CLI (like command prompt or terminal). This is done by using the `cd` command.
5. Install `virtualenv` by running the command `pip install virtualenv` from the CLI window.
2. Execute the command `virtualenv venv` in the CLI. This will create a virtual python environment called venv and will save the environment files in a local directory called `venv`.
    - Note that, if the default python installation is 2.7 (execute `python --version` to check), the command `virtualenv venv -p /full/path/to/python3/directory` should be used instead.
<<<<<<< HEAD
3. Activate the virtual environment by running `source venv/Scripts/activate` (or, on a Windows installation, `.venv\Scripts\activate`) in the CLI.
=======
3. Activate the virtual environment by running `source venv/Scripts/activate` (or, on a Windows installation, `.\venv\Scripts\activate`).
>>>>>>> origin/master
    - After executing this script, there will be `(venv)` written before the path in the CLI.
4. Install the required dependencies by running `pip install -r requirements.txt` in the CLI. Depending on the internet connection and the disk speed, this command may take a few minutes to complete.
5. Exit the virtual environment with the command `deactivate` in the CLI. The `(venv)` indicator will disappear from the CLI.
6. Download the Graphviz library installer from the [Graphviz website](http://www.graphviz.org/Download.php) and install it.

**Execution**

1. Navigate to the directory that the script will execute from in a CLI (like command prompt or terminal)
2. Enter the virtual environment: `source venv/Scripts/activate` or, on a Windows installation: `.\venv\Scripts\activate`
3. Run the script: `python NetworkMap.py <arguments>`
    - It is recommended to have the configuration files in the same folder as the `NetworkMap.py` script itself, although it is not required
4. Leave the virtual environment when finished: `deactivate`
5. View the Graph by looking at the `output.png` file. The other `output` file is the DOT diagram corresponding to the picture.

**The following arguments are required:**

`-c <filename>` OR `--contexts <filename>`: The name of the FWSM contexts file. (NOTE that this is a single file including the running config of each individual context.)

`-f <filename>` OR `--config <filename>`: The name of the distribution switch config file.

`-s <filename>` OR `--system <filename>`: The name of the FWSM system level file.

`-v <filename>` OR `--vlans <filename>`: The name of the distribution switch vlans file.

**Troubleshooting**

- Sometimes, if the virtual environment is not set up correctly, the wrong installation of python will be used. type in `which python` to check the location of the python installation being used.
- Virtualenv automatically installs to the default Python installation (if there are multiple versions of Python installed). Make sure the proper version of python is being used by the virtual environment.
    - To force virtualenv to use a specific version of python when creating a virtual environment, run `virtualenv venv -p /path/to/specific/python/installation/directory`.
- On some Windows systems, the extensions of files (like `.txt` or `.py`) are hidden in the file browser by default. These extensions are still required when executing the script, however. run the `dir` command in a CLI to see the full file names.
- When python is installed, it updates the System's `Path` variable. If a command prompt window is already open before installing Python, it will not have the updated variable, and thus will not recognize python as an installed program, even if it was installed properly. Restarting the CLI will fix this issue.
    - In some extreme cases, if this does not fix the problem, a full system restart may be needed.
- If Python was installed for all users (it was installed to the "Program files" folder rather than a user's "AppData" folder), then `pip` will require administrative privileges to install `virtualenv`. This can be fixed by running the CLI as administrator.

## Authors / Owners

- Ben Schwabe [schwabebp@slu.edu]

Please see `LICENCE.md` for more information.
