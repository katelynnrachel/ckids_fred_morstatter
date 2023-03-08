# ckids_fred_morstatter
Installation
1. Install conda.  "conda -V" prints the version of conda if you have it installed.
2. Install Python.  "python -V" prints the version of conda if you have it installed.

Setup
1. Open a terminal and navigate to the folder containing the files
2. If your conda is outdated, run "conda update conda" and "conda update anaconda"
3. Install a virtual environment (in order to avoid module clashes) by running "conda create -n myenv"
4. Activate the virtual environment with "conda activate myenv"
5. Install Jupyter Notebook with "pip install notebook"
6. Install BERTopic with "pip install bertopic"
7. Start Jupyter Notebook with "jupyter notebook"
8. After you're done working, exit Jupyter Notebook with ctrl+c, and deactivate the virtual environment with "conda deactivate"

Troubleshooting
1. Make sure data.zip is unzipped
2. It is normal for some directories to be empty (means the person had no tweets about them)
3. The commands above are for Macs, and may not work for Windows

Notes on false positives:
https://docs.google.com/document/d/1BehM1QP6t1GnvGrIsZwk2aThciWTu1pST1QDctO2sE8/edit
