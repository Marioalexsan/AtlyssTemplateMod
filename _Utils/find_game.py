from re import search
from platform import system
from os import path, walk, chdir
from psutil import disk_partitions

chdir(path.dirname(path.abspath(__file__)))

def findAtlyss(broad: bool = False):
    libraryLocations = [
        # Windows
        path.expandvars(r'%ProgramFiles(x86)%\Steam\steamapps\libraryfolders.vdf'),
        path.expandvars(r'%ProgramFiles%\Steam\steamapps\libraryfolders.vdf'),
        path.expandvars(r'%UserProfile%\Documents\My Games\Steam\libraryfolders.vdf'),
        path.expandvars(r'%ProgramData%\Steam\libraryfolders.vdf'),

        # Linux
        path.expanduser(r'~/.steam/steam/steamapps/libraryfolders.vdf'),
        path.expanduser(r'~/.local/share/Steam/steamapps/libraryfolders.vdf'),
    ]

    steamLibraries = []
    for location in libraryLocations:
        print(f"Checking library location: {location}")
        if path.isfile(location):
            with open(location, 'r') as file:
                libraries = [line.split('"')[3] for line in file if '"path"' in line]
                steamLibraries.extend(libraries)
                print(f"Found libraries: {libraries}")

    if broad:
        if not steamLibraries:
            print("No predefined libraries found, starting a broader search...")
            if system() == 'Windows':
                drives = []
                for partition in disk_partitions():
                    if 'removable' not in partition.opts:
                        drives.append(partition.mountpoint)
                print(f"Non-removable drives found: {drives}")
            else:
                drives = ['/']
                print("Searching in the root directory on Linux")

            for drive in drives:
                print(f"Searching in drive: {drive}")
                for root, dirs, _ in walk(drive):
                    if 'steamapps' in dirs:
                        steamLibraries.append(root)
                        print(f"Found steamapps in: {root}")

    for library in steamLibraries:
        common_path = path.join(library, "steamapps", "common")
        if path.exists(common_path):
            for dirpath, dirnames, _ in walk(common_path):
                if "ATLYSS" in dirnames:
                    installationPath = path.join(dirpath, "ATLYSS")
                    print(f"Atlyss found at: {installationPath}")
                    return installationPath

    print("Atlyss installation not found.")
    return None

with open("../Directory.Build.props", "r") as file:
    propsData = file.read()

previousPath = search("<ATLYSS_PATH>(.*)</ATLYSS_PATH>", propsData)

try:
    previousPath.group(1)
except AttributeError:
    with open("../Directory.Build.props", "w") as file:
        file.write("<ATLYSS_PATH></ATLYSS_PATH>")

    # makes sure that theres at least a grammar constraint inside it
    with open("../Directory.Build.props", "r") as file:
        propsData = file.read()

    previousPath = search("<ATLYSS_PATH>(.*)</ATLYSS_PATH>", propsData)

if path.exists(previousPath.group(1)):
    print("Previous ATLYSS_PATH seems valid, won't overwrite it.")
    exit()
else:
    print(f"Previous ATLYSS_PATH {previousPath} is invalid!")
    print(f"Attempting to override ATLYSS_PATH value...")
    newPath = findAtlyss()

    if newPath != None:
        newData = f"<ATLYSS_PATH>{newPath}</ATLYSS_PATH>".replace("\\", "\\\\")
        with open("../Directory.Build.props", "w") as file:
            file.write(newData)
        print(f"Set ATLYSS_PATH to {newData}!")
    else:
        print(f"ATLYSS installation could not be found. Attempting to override ATLYSS_PATH value with a broader search...")
        newPath = findAtlyss(True)
        if newPath != None:
            newData = f"<ATLYSS_PATH>{newPath}</ATLYSS_PATH>".replace("\\", "\\\\")
            with open("../Directory.Build.props", "w") as file:
                file.write(newData)
            print(f"Set ATLYSS_PATH to {newData}!")
        else:
            print("Couldn't determine install path, try manually specifying ATLYSS_PATH in Directory.Build.props.")
