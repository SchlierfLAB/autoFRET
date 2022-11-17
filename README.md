# Pybat and Tree

## Installation

### Python packages 
- Numpy
- Pandas 
- PyQt 
- Watchdog 
- Numba 
- Scipy
- Matplotlib
- Joblib
- Opencv

### Quick Setup
For a quick setup make sure that ANACONDA is installed on your system. If not please visit https://anaconda.org and
install the free to use software. ANACONDA is not required in order to use the software but it will make life 
way more easy. You can run the autoinstall.py script which is currently under development. If the installaition
fails please follow the steps below.

We provide an autoinstaller tool with the software. For this you need to run the autoinstall.py file. It will 
automatically set up a conda environment. Please note that the installer is in an early development state
and might not work on all systems. If the installation fails please follow the next steps in order to install 
the required python libraries. 

Open the terminal and navigate to the project requirements directory. Afterwards run the following command (select
the file corresponding to your OS):

```bash

$ conda env create --name pyBatTreeENV --file enviroment.yml

```
you can also change the name of the env. by changing "pyBatTreeENV" in the command above.

Afterwards activate your environment with: 

```bash
$ conda activate <env name>
```

Now run the pyBat or pyTree file. For detailed information on the program refer to the git Wiki or the Usermanual in the Texts folder.

### Performance 
The performance is evaluated on a full 96 well measurement containing roughly 8GB of data.
Systems: 
- MacOS: MacBook pro with an M1 pro 4 core CPU and 16GB memory
- Windows: Workstation with an Intel Xeon E3-1270 4 core CPU and 32GB memory

| Tool               | MacBook pro | Windows Workstation |
|--------------------|----------|--------------------|
| ParBat 7 processes | 3 Hours  | 13 Hours |
| Single Run         | 24 Hours | ??                 |
