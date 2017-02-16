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

1. Navigate to the directory that the script will execute from in a CLI (like command prompt or terminal)
2. Execute the command `virtualenv venv`. This will create a virtual python environment called venv and will save the environment files in a local directory called `venv`.
    - Note that, if the default python installation is 2.7 (execute `python --version` to check), the command `virtualenv venv -p /full/path/to/python3/directory` should be used instead.
3. Activate the virtual environment by running `source venv/Scripts/activate` (or, on a Windows installation, `.venv\Scripts\activate`).
    - After executing this script, there will be `(venv)` written before the path in the CLI.
4. Install the required dependencies by running `pip install -r requirements.txt`. Depending on the internet connection and the disk speed, this command may take a few minutes to complete.
5. Exit the virtual environment with the command `deactivate`. The small `(venv)` indicator will disappear from the CLI.
6. Download the graphviz library from the [Graphviz website](http://www.graphviz.org/Download.php)

**Execution**

1. Navigate to the directory that the script will execute from in a CLI (like command prompt or terminal)
2. Enter the virtual environment: `source venv/Scripts/activate` or, on a Windows installation: `.\venv\Scripts\activate`
3. Run the script: `python NetworkMap.py <arguments>`
4. Leave the virtual environment when finished: `deactivate`

**The following arguments are required:**

`-c <filename>` OR `--contexts <filename>`: The name of the FWSM contexts file.

`-f <filename>` OR `--config <filename>`: The name of the distribution switch config file.

`-s <filename>` OR `--system <filename>`: The name of the FWSM system level file.

`-v <filename>` OR `--vlans <filename>`: The name of the distribution switch vlans file.

**Troubleshooting**

- Sometimes, if the virtual environment is not set up correctly, the wrong installation of python will be used. type in `which python` to check the location of the python installation being used.
- Virtualenv automatically installs the default Python installation (if there are multiple versions of Python installed). Make sure the proper version of python is being used by the virtual environment.
    - To force virtualenv to use a specific version of python when creating a virtual environment, run `virtualenv venv -p /path/to/specific/python/installation/directory`.

## Authors / Owners

- Ben Schwabe [schwabebp@slu.edu]

Please see `LICENCE.md` for more information.
