# Efesto Rocket Forge

## Build from source on Windows

Install Anaconda <https://www.anaconda.com/download/>

Be sure to enable the "Add Anaconda3 to my PATH environment variable" option during the installation.

Install MinGW from <https://winlibs.com/#download-release> and unzip its content inside the `C:/MinGW` folder (if it doesn't exist, just create it). You now should have a `C:/MinGW/mingw64/bin` folder and a `C:/MinGW/mingw64/lib` folder, along other files.

Be sure to add `C:\MinGW\mingw64\bin` and `C:\MinGW\mingw64\lib` to `Path` in the environment variables.

For the following steps, use a **conda environment**, either using **Anaconda prompt** or just by creating it in the Windows command prompt:
```
conda update -n base -c defaults conda

conda create -n rocket python=3.9

conda activate rocket
```

You can install git inside the conda environment using
```
conda install git
```

Install python requirements:
```
pip install -r requirements.txt
```

Install rocketcea:  
```
pip install --global-option build_ext --global-option --compiler=mingw32 rocketcea
```

You can check if rocketcea has been successfully installed using the following command:
```
python -c "from rocketcea.cea_obj import CEA_Obj; C=CEA_Obj(oxName='LOX', fuelName='LH2'); print(C.get_Isp())"
```
Its output must be about `374.303617`.

Now you should be able to run python code. If you want to compile it into an executable file, read the following steps.

Install PyInstaller from source:
```
git clone https://github.com/pyinstaller/pyinstaller.git

cd pyinstaller

pip install .
```

Build PyInstaller bootloader using the MinGW-w64 suite as described in <https://pyinstaller.org/en/stable/bootloader-building.html>
```
cd bootloader

python waf --gcc all
```

Find python libraries installation folder. It will be displayed after "Location: " in the output of the following command:
```
pip show rocketcea
```

Assign a temporary variable to that folder:
```
SET "FOLDER=C:\path\to\that\folder"
```

Use PyInstaller to compile the software using the %FOLDER% variable:
```
pyinstaller --windowed --onefile --add-data "$FOLDER/rocketcea:rocketcea/" --add-data "$FOLDER/customtkinter:customtkinter/" --add-data "icon.png:." --add-data "theme.json:." --icon=icon.png -n "Rocket Forge" --clean main.py 
```

## Build from source on Linux

Install gfortran <https://fortran-lang.org/en/learn/os_setup/install_gfortran/>

Install python requirements
```
pip install -r requirements.txt

pip install rocketcea
```

Install PyInstaller
```
pip install pyinstaller
```
Find libraries installation folder using
```
pip show rocketcea
```
Assign a temporary variable to that folder:
```
FOLDER=/path/to/your/python/libraries/folder
```
Use PyInstaller to compile the software using the $FOLDER variable:
```
pyinstaller --windowed --onefile --add-data "$FOLDER/rocketcea:rocketcea/" --add-data "$FOLDER/customtkinter:customtkinter/" --add-data "icon.png:." --add-data "theme.json:." --icon=icon.png -n "Rocket Forge" --clean main.py 
```