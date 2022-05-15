# Call-Board
Software to display information on the Call Center displays

# Setup
In order to get the repo and, more specifically, the virtual environment set up, clone the repo, open the directory in cmd, and run:  
&emsp; python -m venv .venv  
to create the .venv folder. Then run  
&emsp; .\.venv\scripts\activate  
to configure your cmd session to the venv. Now 'where python' should indicate the venv's installation. Finally, run  
&emsp; pip install -r requirements.txt  
which will update your virtual environment with all the dependencies. If you ever update dependencies, run  
&emsp; pip freeze > requirements.txt  
to update the requirements file with the new dependencies.  
The .venv folder is in the gitignore so that we don't have to keep a copy of the venv on the github.