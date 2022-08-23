import subprocess, sys, os
import tkinter as tk
from tkinter import filedialog

def get_parent():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory()

def get_locs(root_dir):
    # extracts all .bin and .npy files from the subdirs in root

    hir_structure = os.walk(root_dir)

    bins = list()
    hists = list()

    for folder, subfolders, files in hir_structure:
        if folder != root_dir:
            for f in files:
                if f.endswith('.bin'):
                    bins.append(os.path.join(folder,f))
                elif f.endswith('.npy'):
                    hists.append(os.path.join(folder,f))

    return (bins, hists)

def kill_files(file_dirs):

    for file in file_dirs:
        subprocess.run(['rm', f'{file}'])




if __name__ == '__main__':
    print('Deleting HIST and .bin files from folder')

    #folder_loc = get_parent()
    folder_loc = 'U:/Techniques/High-Troughput TCSPC/smFRET_Software/Sample_Data/typical_small_test'

    locs = get_locs(folder_loc)

    for file_lists in locs:
        kill_files(file_lists)
