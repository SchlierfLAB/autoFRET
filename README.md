# pyBAT and pyVIZ

For detailed information please read the following article: 

Farewell to single well: An automated single-molecule FRET platform for multiwell-plate screening of biomolecular
conformations and dynamics (https://www.biorxiv.org/content/10.1101/2023.02.28.530427v1)

Sample data can be found at: http://dx.doi.org/10.25532/OPARA-202

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

#### Additional packages required for the scanning software

- zaber-motion
- pyserial

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
the file corresponding e.g. pyBATVIZ_ENV.yml):

```bash
$ conda env create --name pyBATVIZ_ENV --file enviroment.yml
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
- MacOS: MacBook pro with an M1 pro 8 core CPU and 16GB memory (no SMT)
- Windows: Workstation 1 with an Intel Xeon E3-1270 4 core CPU and 32GB memory (SMT)
- Windows: Workstation 2 with an Intel i7-8700k 6 core CPU and 32GB memory (SMT)

| Tool                | MacBook pro | Windows Workstation 1 | Windows Workstation 2 |
|---------------------|-------------|-----------------------|-----------------------|
| pyBAT 1 process     | 24 Hours    | -                     | -                     |
| pyBAT 7 processes  | 3 Hours     | 13 Hours              | -                     |
| pyBAT 11 processes | -           | -                     | 7.3 Hours             |  
