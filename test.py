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
        if (ext in ['.flf', '.tlf', '.flc']):
            files_list.append(file)

# Some alphabetical sorting
files_list.sort()

# Creating example file with the text you want
text = "Hello brave new world!"

with open("output.txt", "w") as output_file:

    for font in files_list:
        font_name = os.path.splitext(font)[0].lower()
        font_type = os.path.splitext(font)[1].lower()[1:]
        if font[:7] == "obanner":
            statut = "skipped"
        else:
            cmd = ['figlet', text, '-f', font, '-w', '300']
            try:
                result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            finally:
                if (result.returncode == 0):
                    # Everything's fine
                    output_file.write("Font: {} ({})\n\n".format(font_name, font_type))
                    output_file.write(result.stdout.decode())
                    output_file.write("\n\n")
                    statut = "ok"
                else:
                    # Houston, we got a problem
                    statut = "file error"
        print("Font {} ({}): {}".format(font_name, font_type, statut))


