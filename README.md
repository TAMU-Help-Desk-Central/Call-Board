# Call-Board
Software to display information on the Call Center displays

## Statistics
![Create Binaries](https://github.com/TAMU-Help-Desk-Central/Call-Board/actions/workflows/create-binary.yml/badge.svg?branch=main)
[![Coverage Status](https://coveralls.io/repos/github/TAMU-Help-Desk-Central/Call-Board/badge.svg?branch=main)](https://coveralls.io/github/TAMU-Help-Desk-Central/Call-Board?branch=main)


## Setup
In order to get the repo and, more specifically, the virtual environment set up, clone the repo, open the directory a terminal, and run:  
```python -m venv .venv```
to create the .venv folder. Then run  
```.\.venv\scripts\activate```
to configure your session to the venv. Now 'where python' should indicate the venv's installation. Finally, run  
```pip install -r requirements.txt```
which will update your virtual environment with all the dependencies. If you ever update dependencies, run  
```pip freeze > requirements.txt```
to update the requirements file with the new dependencies.  
The .venv folder is in the gitignore so that we don't have to keep a copy of the venv on the GitHub.