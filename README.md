## autoFRET - pyMULTI, pyBAT and pyVIZ ##

For information about possible applications and performance of autoFRET please read the following article: 

Farewell to single well: An automated single-molecule FRET platform for multiwell-plate screening of biomolecular
conformations and dynamics (https://www.biorxiv.org/content/10.1101/2023.02.28.530427v1)

Sample data can be found at: http://dx.doi.org/10.25532/OPARA-202

Detailed information about installation, usage and underlying algorithms of the software package please refer to the autoFRET Wiki: https://github.com/SchlierfLAB/autoFRET/wiki

<img width="750" alt="image" src="https://user-images.githubusercontent.com/58071484/224969134-7bb64d26-30a7-4565-82e6-1e9878f76c8e.png">

### System requirements ###
Python 3.7 with the following non-standard libraries: Numpy (1.21.6), Pandas (1.3.5), PyQt (5.15.7), Watchdog (0.9.0), Numba (0.56.4), Scipy (1.7.3), Matplotlib (3.5.3), Joblib (1.1.1), Cv2 (4.6.0), Zaber Motion Library (2.14.6), and pySerial (3.5). Everything was tested on Windows 10 and macOS Monterey. In principle, any OS with support for Python 3 should be sufficient. As descript in detail in the SI, the multiwell-plate measurement software pyMULTI communicates with the Zaber stage (ASR100B120B-E03T3A) controller X-MCC2 and the TCSPC modul HydraHarp 400 via USB connection. For data analysis (pyBAT) and visualization (pyVIZ) no non-standard hardware is required.

### Installation guide ###
Install Python 3.7 with Anaconda following the standard procedures. Download the autoFRET software package from GitHub. Unzip autoFRET-main.zip to a location of choice on your hard disk drive. To install the measurement software pyMULTI, run the “autoinstallMULTI.py” file (main folder). To install the analysis and visualization software (pyBAT and pyVIZ), run “autoinstallBATVIZ.py” (main folder). This should take roughly 5 minutes. Both installers will create new conda environments: “pyMULTI_ENV” for the measurement software and “pyBATVIZ_ENV” for the analysis and visualization software. Internal functional dependencies can be found in the python package directories “FRET_backend“, “OnTheFlyBurst_Scripts“, and “Zaber control software“. Dependency files of other formats, e.g., YML-files for the installer, can be found in the requirements directory. The software files for the measurement software “pyMULTI.py” and “pySingle.py” are found in the folder “Zaber control software“. Raw data during a measurement can be analyzed using “pyBAT_otf.py”. To analyze raw data after a measurement, execute “pyBAT.py”. For the visualization of an analyzed measurement execute “pyVIZ.py”. 

### Demo ###
**Raw data analysis with pyBAT.**
Execute the main analysis file “pyBAT.py” with the active conda environment “pyBATVIZ_ENV” (set as interpreter). Open “File“ in the menue and select “Open file“. Press on the folder icon next to “Drag ht3 File”, navigate to the “DNA_Ruler_DEMO/DNA_Ruler/A01” folder, and select the raw data file “A01_0.ht3”. Press the folder icon next to “Drag first hhd File”, navigate to the requirements folder, and select the IRF file “IRF_L530_EryB_KI_X.hhd“. Press the folder icon next to “Drag second hhd File”, navigate to the requirements folder, and select the IRF file “IRF_L640_ATTO655_KI.hhd“. After the fluorescence decays are loaded, adjust the IRF (grey lines) positions using the plus and minus below the plots. As a next step, press the "DD + DA" button and select the time window (channels) of the donor/acceptor emission after donor excitation using the cross hair in the first panel (in our case channel 50 to 1200). Subsequently, press the "AA" button and define the time window (channels) of the acceptor emission after acceptor excitation in the second panel (in our case channel 1250 to 2500). Before starting the analysis, set the upper inter-photon threshold for burst search to IPT_Burst=0.3 ms, the lower inter-photon time threshold for background estimation to IPT_BG=0.03 and the threshold for the total number of photons to Nph=50. After pressing “Refresh“, around 947 bursts and 509 background regions should be detected in the time trace (lower panel). Finally, press the “Analyze“ button and select the “DNA_Ruler_DEMO/DNA_Ruler” folder. 

**Visualization of analyzed data in pyVIZ.**
Execute the main visualization file “pyVIZ.py” with the active conda environment “pyBATVIZ_ENV” (set as interpreter). Open “File“ in the menue and select “Open file“. Navigate to the “DNA_Ruler_DEMO/DNA_Ruler” folder. After pressing enter, a single well FRET efficiency histogram (grey bars) should appear in the left panel and a 2D FRET efficiency histogram (rainbow colormap) of all analyzed wells should in the right panel. In order to correct the FRET efficiency and display only double labeled molecules, set the correction factors to Alpha=0.0608, Beta=0.0267, and Gamma=0.8426, the stoichiometry filter to 0.25 < S < 0.75, and the ALEX-2CDE filter to 0 < ALEX-2CDE < 15. Press “Refresh”.  

**Expected output.**
During data analysis the console in Python displays the files processed by the CPU cores. All raw data are analyzed, when the run time is displayed in the console. After a successful analysis session each folder contains the two binary files “BData1.bin” and “PData1.bin”. 
After loading the analyzed data into pyVIZ and applying the corresponding correction factors and filters, the left panel should show a FRET efficiency histogram containing two Gaussian distributions centered around E=0.15 and E=0.8. The right panel should show a 2D FRET efficiency histogram with repeats of the same distribution. 

**Expected run time for demo on a "normal" desktop computer.**
On a common desktop computer, the data analysis of the example files should not take longer than 5 minutes. Visualization of the demo data with pyVIZ should take not more than some seconds.  

### Instruction for use ###
**pyMULTI.**
Before using pyMULTI for the first time define the “Home” position by centering the objective in well A01 and press the “Set home position”.  

**pyBAT.**
The optimal value for IPT_Burst (burst identification) depends on the brightness of the dyes and the detection efficiency and is usually in the range of 0.005 and 0.03 ms. Note: Low IPT_Burst values discriminate dim FRET populations. The optimal value for IPT_BG (identification of background regions) depends on the frequency of bursts and is usually in the range of 0.005 and 0.03 ms. The IPT_BG should not be lower than IPT_Burst. The optimal value for Nph depends on the brightness of the dyes and the observation time in the confocal volume. Use "Raw Data" to inspect the intensity time trace and choose a Nph above the noise level (typically in the range of 30 and 200 Photons). Note: High Nph values discriminate fast diffusing molecules. The “Number of cores” used to analyze data is set by default to "Auto", where N-1 of the N available threads are used.

