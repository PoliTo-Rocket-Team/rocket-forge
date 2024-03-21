# Efesto Rocket Forge

## Installation on Windows

### Prerequisites
Install git (https://git-scm.com/downloads)

Install 7-Zip (https://www.7-zip.org/)

Install Anaconda (https://www.anaconda.com/download/)

Be sure to enable the "Add Anaconda3 to my PATH environment variable" option during the installation.

### MinGW

Download MinGW (https://winlibs.com/#download-release)

Select UCRTG runtime GCC 13.2.0 (with POSIX threads) + LLVM/Clang/LLD/LLDB 17.0.6 + MinGW-w64 11.0.1 (UCRT) - release 5 Win64 7-Zip archive.

Open winlibs-x86_64-... using 7-Zip File Manager and extract the `mingw64` folder.

Inside `C:/`, create a new `MinGW` folder. Move the `mingw64` folder inside the `MinGW` folder.

You now should have a `C:/MinGW/mingw64/bin` folder and a `C:/MinGW/mingw64/lib` folder, along other files.

Be sure to add `C:\MinGW\mingw64\bin` and `C:\MinGW\mingw64\lib` to `Path` in the environment variables.

### Install dependencies

Create a new conda environment with python version 3.11, using the following commands:
```
conda update -n base -c defaults conda

conda create -n rocket python=3.11

conda activate rocket
```

Install python requirements:
```
pip install tabulate customtkinter
```

Install rocketcea:  
```
pip install rocketcea
```

You can check if rocketcea has been successfully installed using the following command:
```
python -c "from rocketcea.cea_obj import CEA_Obj; C=CEA_Obj(oxName='LOX', fuelName='LH2'); print(C.get_Isp())"
```
Its output must be about `374.303617`.

Now you should be able to run python code. If you want to build it into an executable file, read the following steps.

### Build the executable

Install PyInstaller from source:
```
git clone https://github.com/pyinstaller/pyinstaller.git

cd pyinstaller

pip install .
```

Build PyInstaller bootloader using the MinGW-w64 suite as described in <https://pyinstaller.org/en/stable/bootloader-building.html>
```
cd bootloader

python waf --gcc configure all
```

Find python libraries installation folder. It will be displayed after "Location: " in the output of the following command:
```
pip show rocketcea
```

Assign a temporary variable to that folder:
```
SET "FOLDER=C:\path\to\that\folder"
```

Be sure to disable antivirus for the Rocket Forge installation folder.

Use PyInstaller inside the Rocket Forge installation folder to compile the software using the %FOLDER% variable:
```
pyinstaller --windowed --onefile --add-data "%FOLDER%/rocketcea:rocketcea/" --add-data "%FOLDER%/customtkinter:customtkinter/" --add-data "%FOLDER%/PIL:PIL/" --add-data "icon.png:." --add-data "rocketforge/geometry/help.png:rocketforge/geometry/" --add-data "theme.json:." --icon=icon.png -n "Rocket Forge" --clean main.py 
```
Executable file will be built inside the `dist` folder. To build an updated version of the executable, just use:
```
pyinstaller "Rocket Forge.spec"
```

## Installation on GNU/Linux

Install gfortran <https://fortran-lang.org/en/learn/os_setup/install_gfortran/>

Install python requirements:
```
pip install tabulate customtkinter rocketcea pyinstaller
```
Assign a temporary variable to python libraries folder:
```
FOLDER=/path/to/your/python/libraries/folder
```
Use PyInstaller to compile the software using the $FOLDER variable:
```
pyinstaller --windowed --onefile --add-data "$FOLDER/rocketcea:rocketcea/" --add-data "$FOLDER/customtkinter:customtkinter/" --add-data "$FOLDER/PIL:PIL/" --add-data "icon.png:." --add-data "rocketforge/geometry/help.png:rocketforge/geometry/" --add-data "theme.json:." --icon=icon.png -n "Rocket Forge" --clean main.py 
```