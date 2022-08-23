# init import with default libs.

import platform
import os, subprocess

# env name to be used for installation
env_name = 'test_env_auto'

# define some print cols
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# get system for file selection
system = platform.system()

# test if conda is installed
if subprocess.run(['conda', 'list'], shell=True, stdout=subprocess.DEVNULL).returncode == 0:
    pass
else:
    print('Please install conda on your system.\nhttps://anaconda.org')


if system == 'Darwin':
    print(bcolors.OKBLUE + 'Start installing on Darwin (MacOS)')
    # get mac yml path
    yml_mac_file = os.path.abspath('requirements/Mac_enviroment_Bat_T.yml')
    # test
    if not os.path.isfile(yml_mac_file):
        yml_mac_file = input('Could not grep Mac_enviroment_Bat_T.yml.\nPlease enter the '
                                             'corresponding file path')

        # conda env create --name pyBatTreeENV --file enviroment.yml
        subprocess.run(['conda', 'env', 'create', '--name', f'{env_name}', '--file', f'{yml_mac_file}'])

        # test install success
        if env_name in str(subprocess.run('conda env list'.split(), stdout=subprocess.PIPE).stdout):
            print(f'Installed new env: {env_name}\nPlease activate it in the terminal with: conda activate {env_name}')
        else:
            print(bcolors.WARNING + 'Seems like the installation failed. Please'
                                    ' follow the instructions in the README file for manual installation')

    else:
        # conda env create --name pyBatTreeENV --file enviroment.yml
        subprocess.run(['conda', 'env', 'create', '--name', f'{env_name}', '--file', f'{yml_mac_file}'])

        # test install success
        if env_name in str(subprocess.run('conda env list'.split(), stdout=subprocess.PIPE).stdout):
            print(f'Installed new env: {env_name}\nPlease activate it in the terminal with: conda activate {env_name}')
        else:
            print(bcolors.WARNING + 'Seems like the installation failed. Please'
                                    ' follow the instructions in the README file for manual installation')

elif system == 'Windows':
    print(bcolors.OKBLUE + 'Start installing on Windows')
    # get win yml path
    yml_windows_file = os.path.abspath('requirements\Windows_enviroment_Bat_T.yml')
    # test
    if not os.path.isfile(yml_windows_file):
        yml_windows_file = input('Could not grep Windows_enviroment_Bat_T.yml.\nPlease enter the '
                                 'corresponding file path')

        # conda env create --name pyBatTreeENV --file enviroment.yml
        subprocess.run(['conda', 'env', 'create', '--name', f'{env_name}', '--file', f'{yml_windows_file}'], shell=True)

        # test install success
        if env_name in str(subprocess.run(['conda', 'env', 'list'], shell=True, stdout=subprocess.PIPE).stdout):
            print(f'Installed new env: {env_name}')
        else:
            print(bcolors.WARNING + 'Installation failed. Please follow the instructions in the README file '
                                    'for manual installation')


    else:
        # conda env create --name pyBatTreeENV --file enviroment.yml
        subprocess.run(['conda', 'env', 'create', '--name', f'{env_name}', '--file', f'{yml_windows_file}'], shell=True)

        # test install success
        if env_name in str(subprocess.run(['conda', 'env', 'list'], shell=True, stdout=subprocess.PIPE).stdout):
            print(f'Installed new env: {env_name}')
        else:
            print(bcolors.WARNING + 'Installation failed. Please follow the instructions in the README file '
                                    'for manual installation')


else:
    print(bcolors.WARNING + 'Your OS seems not to be supported by the autoinstall script')


