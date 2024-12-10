import os
import sys
import glob
import subprocess
import re
import shutil
import zipfile
import json

def keep_assembly_dependency(assembly):
  IGNORED_ASSEMBLIES = [
    "AsmResolver",
    "BepInEx.AssemblyPublicizer",
    "Microsoft.Win32",
    "Newtonsoft.Json",
    "System.",
  ]

  for part in IGNORED_ASSEMBLIES:
    if part in assembly:
      return False

  return True


LAST_WORKDIR = os.getcwd()

# Ensure script location is current directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Let's rebuild the project to make sure it's all good
os.chdir('..')

slns = glob.glob("*.sln")
csprojs = glob.glob("*.csproj")

if len(slns) != 1:
  print("Couldn't determine solution file to build.")
  sys.exit(1)

sln = slns[0]

# Uncomment in case you're running this standalone and need to build the project
# subprocess.run(['dotnet', 'build', slns[0]])

if len(csprojs) == 1:
  with open(csprojs[0], 'r') as f:
    CSPROJ_DATA = f.read()
    MATCH = re.search("<TargetFramework>(.*)</TargetFramework>", CSPROJ_DATA)

    if MATCH is not None:
      if MATCH.group(1) == 'netstandard2.1':
        FRAMEWORK = 'netstandard2.1'
      elif MATCH.group(1) == 'net47':
        FRAMEWORK = 'net47'
      elif MATCH.group(1) == 'net471':
        FRAMEWORK = 'net471'
      elif MATCH.group(1) == 'net472':
        FRAMEWORK = 'net472'
      elif MATCH.group(1) == 'net48':
        FRAMEWORK = 'net48'
      elif MATCH.group(1) == 'net481':
        FRAMEWORK = 'net481'
      else:
        # Let's assume it's netstandard2.1
        FRAMEWORK = 'netstandard2.1'
    else:
      # Let's assume it's netstandard2.1
      FRAMEWORK = 'netstandard2.1'

    MATCH_GUID = re.search("<AssemblyName>(.*)</AssemblyName>", CSPROJ_DATA)
    
    if MATCH_GUID is not None:
      MOD_GUID = MATCH_GUID.group(1)
    else:
      print('Failed to find <AssemblyName> to use as mod GUID in .csproj, cannot pack mod as a result.')
      sys.exit(1)

    MATCH_THUNDERSTORENAME = re.search("<ThunderstoreName>(.*)</ThunderstoreName>", CSPROJ_DATA)
    
    if MATCH_THUNDERSTORENAME is not None:
      MOD_THUNDERSTORENAME = MATCH_THUNDERSTORENAME.group(1)
    else:
      print('Failed to find <ThunderstoreName> to use as mod name in .csproj, cannot pack mod as a result.')
      sys.exit(1)

    MATCH_VERSION = re.search("<Version>(.*)</Version>", CSPROJ_DATA)
    
    if MATCH_VERSION is not None:
      MOD_VERSION = MATCH_VERSION.group(1)
    else:
      print('Failed to find <Version> to use as mod version in .csproj, cannot pack mod as a result.')
      sys.exit(1)
else:
  # Let's assume it's netstandard2.1
  FRAMEWORK = 'netstandard2.1'

os.chdir(os.path.join('bin', 'Debug', FRAMEWORK))
ASSEMBLIES = [os.path.abspath(path) for path in glob.glob('*.dll') if keep_assembly_dependency(path)]

if len(ASSEMBLIES) == 0:
  print('Couldn\'t find build files, please check that the project has been built in Debug mode.')
  sys.exit(1)

print('Will copy the following DLLs to the package:')

for assembly in ASSEMBLIES:
  print(' - ' + assembly)

os.chdir(os.path.join('..', '..', '..'))
os.chdir('_Thunderstore')

shutil.rmtree('Output', ignore_errors=True)

os.mkdir('Output')

# Update mod GUID and version
if not os.path.exists('manifest.json'):
  print("Couldn't find manifest.json in output, was it removed?")
  sys.exit(1)

with open('manifest.json', 'r') as f:
  MANIFEST_DATA = json.loads(f.read())

MANIFEST_DATA['name'] = MOD_THUNDERSTORENAME
MANIFEST_DATA['version_number'] = MOD_VERSION

print(f'Set Thunderstore manifest.json name to {MOD_THUNDERSTORENAME} (from .csproj <ThunderstoreName>)')
print(f'Set Thunderstore manifest.json version_number to {MOD_VERSION} (from .csproj <Version>)')

with open('manifest.json', 'w') as f:
  f.write(json.dumps(MANIFEST_DATA, indent=2))

# Pack everything into a zip

with zipfile.ZipFile(os.path.join('Output', f'{MOD_GUID}.zip'), 'w', zipfile.ZIP_DEFLATED) as pkg:
  with open(os.path.join('manifest.json'), 'rb') as f:
    pkg.write('manifest.json')
  with open(os.path.join('icon.png'), 'rb') as f:
    pkg.write('icon.png')
  with open(os.path.join('CHANGELOG.md'), 'rb') as f:
    pkg.write('CHANGELOG.md')
  with open(os.path.join('README.md'), 'rb') as f:
    pkg.write('README.md')

  for assembly in ASSEMBLIES:
    with open(assembly, 'rb') as f:
      pkg.write(assembly, arcname=os.path.basename(assembly))

os.chdir(LAST_WORKDIR)
print('Done!')