import ctypes
import matplotlib.font_manager as fm
import requests
import shutil
import os
import winreg as reg

def is_font_installed(font_name):
    fm.findSystemFonts(fontpaths=None, fontext="ttf")  
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    return font_name in available_fonts

def download_font(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
    else:
        raise Exception(f"Failed to download font from {url}")

def install_font(font_path):
    font_install_dir = os.path.expanduser("~/Library/Fonts")

    if not os.path.exists(font_install_dir):
        os.makedirs(font_install_dir)
    
    try:
        shutil.copy(font_path, font_install_dir)
        print(f"Font installed successfully")
    except Exception as e:
        print(f"Failed to install font: {e}")

def install_font_windows(font_path, font_name):
    fonts_dir = os.path.join(os.environ['WINDIR'], "Fonts")
    font_dest_path = os.path.join(fonts_dir, os.path.basename(font_path))

    try:
        shutil.copy(font_path, font_dest_path)
        print(f"Font installed successfully")
    except Exception as e:
        print(f"Failed to install font: {e}")
        return
    
    try:
        with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts", 0, reg.KEY_SET_VALUE) as key:
            reg.SetValueEx(key, font_name, 0, reg.REG_SZ, os.path.basename(font_path))
        print(f"Font registered successfully")
    except PermissionError:
        print(f"Permission denied to register font")
        return
    except Exception as e:
        print(f"Failed to register font: {e}")
        return
    
    try:
        ctypes.windll.gdi32.AddFontResourceW(font_dest_path)
        ctypes.windll.user32.SendMessageW(0xffff, 0x001D, 0, 0)
        print(f"Font loaded successfully")
    except Exception as e:
        print(f"Failed to notify system: {e}")
        return

    
font_url = "https://drive.google.com/uc?export=download&id=1lkqaon_9qbtV0r_L3xqnoG5HOSsbf5gH"
font_path = "cour.ttf"
font = "Courier New"

if not is_font_installed(font):
    download_font(font_url, font_path)
    fm.fontManager.addfont(font_path)
    if os.name == 'nt':
        install_font_windows(font_path, font)
    else:
        install_font(font_path)
else:
    print(f"{font} is already installed")

