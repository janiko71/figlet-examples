import os, sys
import subprocess

# Check where we are
print(sys.version, sys.version_info)

# List all font files (.flf only)
figlet_path = "/usr/share/figlet"
files_list = []

for file in os.listdir(figlet_path):
    if os.path.isfile(os.path.join(figlet_path, file)):
        ext = os.path.splitext(file)[1]
        if (ext == '.flf'):
            filename = os.path.splitext(file)[0].lower()
            files_list.append(filename)

# Some alphabetical sorting
files_list.sort()

# Creating example file with the text you want
text = "Hello brave new world!"

for font in files_list:
    print("Font name:" + font)
    if font[:7] == "obanner":
        print("Skipped...")
    else:
        cmd = ['figlet', text, '-f', font, '-w', '300']
        result = subprocess.run(cmd, stdout=subprocess.PIPE)
        #print(result.stdout.decode())


