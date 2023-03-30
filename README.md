## autoFRET - pyMULTI, pyBAT and pyVIZ V 1.0.0

For information about possible applications and performance of autoFRET please read the following article: 

Farewell to single well: An automated single-molecule FRET platform for multiwell-plate screening of biomolecular
conformations and dynamics (https://www.biorxiv.org/content/10.1101/2023.02.28.530427v1)

Sample data can be found at: http://dx.doi.org/10.25532/OPARA-202

Detailed information about installation, usage and underlying algorithms of the software package please refer to the autoFRET Wiki: https://github.com/SchlierfLAB/autoFRET/wiki

<img width="750" alt="image" src="https://user-images.githubusercontent.com/58071484/224969134-7bb64d26-30a7-4565-82e6-1e9878f76c8e.png">

### System requirements
Python 3.7 with the following non-standard libraries: Numpy (1.21.6), Pandas (1.3.5), PyQt (5.15.7), Watchdog (0.9.0), Numba (0.56.4), Scipy (1.7.3), Matplotlib (3.5.3), Joblib (1.1.1), Cv2 (4.6.0), Zaber Motion Library (2.14.6), and pySerial (3.5). Everything was tested on Windows 10 and macOS Monterey. In principle, any OS with support for Python 3 should be sufficient. As descript in detail in the SI, the multiwell-plate measurement software pyMULTI communicates with the Zaber stage (ASR100B120B-E03T3A) controller X-MCC2 and the TCSPC modul HydraHarp 400 via USB connection. For data analysis (pyBAT) and visualization (pyVIZ) no non-standard hardware is required.
