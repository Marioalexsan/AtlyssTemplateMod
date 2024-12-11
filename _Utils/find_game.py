from re import search, sub
from os import path, walk, chdir

chdir(path.dirname(path.abspath(__file__)))

def findAtlyss():
    libraryLocations = [
        # Windows
        path.expandvars(r'%ProgramFiles(x86)%\\Steam\\steamapps\\libraryfolders.vdf'),
        path.expandvars(r'%ProgramFiles%\\Steam\\steamapps\\libraryfolders.vdf'),
        path.expandvars(r'%UserProfile%\\Documents\\My Games\\Steam\\libraryfolders.vdf'),
        path.expandvars(r'%ProgramData%\\Steam\\libraryfolders.vdf'),

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

# 
propsFile = "../Directory.Build.props"

if not path.isfile(propsFile):
    print(f"File {propsFile} does not exist. Creating it with a placeholder.")
    with open(propsFile, "w") as file:
        file.write("<ATLYSS_PATH></ATLYSS_PATH>")

with open(propsFile, "r") as file:
    propsData = file.read()

previousPathMatch = search(r"<ATLYSS_PATH>(.*?)</ATLYSS_PATH>", propsData)
previousPath = previousPathMatch.group(1) if previousPathMatch else None

if previousPath and path.exists(previousPath):
    print("Previous ATLYSS_PATH seems valid, won't overwrite it.")
    exit()

print(f"Previous ATLYSS_PATH {previousPath if previousPath else 'is not set or invalid'}")
print("Attempting to override ATLYSS_PATH value...")
newPath = findAtlyss()

if newPath:
    newPathEscaped = newPath.replace("\\", "\\\\")
    if "<ATLYSS_PATH>" in propsData:
        updatedData = sub(r"<ATLYSS_PATH>.*?</ATLYSS_PATH>", f"<ATLYSS_PATH>{newPathEscaped}</ATLYSS_PATH>", propsData)
    else:
        updatedData = propsData + f"\n<ATLYSS_PATH>{newPathEscaped}</ATLYSS_PATH>\n"

    with open(propsFile, "w") as file:
        file.write(updatedData)

    print(f"Set ATLYSS_PATH to {newPath}!")
else:
    print("Couldn't determine install path. Please specify ATLYSS_PATH manually in Directory.Build.props.")
