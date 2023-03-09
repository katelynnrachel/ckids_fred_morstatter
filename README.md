# ckids_fred_morstatter
Installation
1. Install conda.  "conda -V" prints the version of conda if you have it installed.
2. Install Python.  "python -V" prints the version of conda if you have it installed.

Setup
1. Open a terminal and navigate to the folder containing the files
2. If your conda is outdated, run "conda update conda" and "conda update anaconda"
3. Install a virtual environment (in order to avoid module clashes) by running "conda create -n myenv"
4. Activate the virtual environment with "conda activate myenv"
5. Upon trying to install BERTopic with newer versions of python, you will get an incompatibility error because torch is incompatible with newer versions of python; so I used python version 3.9.  Use "conda install python=3.9" to switch the python version within the virtual environment.
6. Install Jupyter Notebook with "pip install notebook"
7. Install numpy, pandas, matplotlib, and ipywidgets with "pip install numpy pandas matplotlib ipywidgets"
9. Install BERTopic with "pip install bertopic"
10. Start Jupyter Notebook with "jupyter notebook"
11. After you're done working, exit Jupyter Notebook with ctrl+c, and deactivate the virtual environment with "conda deactivate"

Troubleshooting
1. If your computer has python3 and pip3 instead of python and pip, use python3 and pip3 (ex. "python3 -V" or "pip3 install notebook")
2. Make sure data.zip is unzipped
3. It is normal for some directories to be empty (means the person had no tweets about them)
4. The commands above are for Macs, and may not work for Windows

Notes on false positives:
https://docs.google.com/document/d/1BehM1QP6t1GnvGrIsZwk2aThciWTu1pST1QDctO2sE8/edit
