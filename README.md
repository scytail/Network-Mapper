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
- IPAddress module (usually included with the default python 3.3 installation)
- NetworkX module
- MatPlotLib module

## Getting Started

Install the required modules by using `pip install ModuleName`.

**Execution:**

Linux/Mac:

`$ python3 NetworkMap.py [arguments]`

Windows:

`$ py -3 NetworkMap.py [arguments]`

_note: If one has python 3.* set up as their default python install, then they can simply execute the script with_ `python NetworkMap.py`_, regardless of system._

**The following arguments are accepted:**

- `-f ConfigurationFileName` OR `--file ConfigurationFileName`
    - The name of the configuration file to be read by the software
- `-d DMZName` OR `--dmz DMZName`
    - The name of the DMZ to look for in the provided file

## Authors / Owners

- Kevin Njuguna [njuguna@slu.edu]
- Ben Schwabe [schwabebp@slu.edu]
