import os, sys
import subprocess
import datetime
import html
from xml.etree import ElementTree as ET

# Check where we are
print(sys.version, sys.version_info)

# List all font files (.flf only)
figlet_path = "/usr/share/figlet"
files_list = []

for file in os.listdir(figlet_path):
    if os.path.isfile(os.path.join(figlet_path, file)):
        ext = os.path.splitext(file)[1]
        if (ext in ['.flf', '.tlf', '.flc']):
            files_list.append(file.lower())

# Some alphabetical sorting
files_list.sort()

# Creating example file with the text you want
text = "Hello brave new world!"

with open("output.txt", "w") as output_file, open("output.html", "w") as html_file:

    # Init HTML output

    html_output = ET.Element('html')
    html_head = ET.Element('head')
    html_meta = ET.Element('meta', attrib={'charset': 'UTF-8'})
    html_style = ET.Element('style')
    html_style.text = ".output_text {font-family: monospace; white-space: pre-line; font-size:10px;}"
    html_head.append(html_meta)
    html_head.append(html_style)
    html_body = ET.Element('body')
    html_output.append(html_head)
    html_output.append(html_body)

    # Test every font

    for font in files_list:

        font_name = os.path.splitext(font)[0].lower()
        font_type = os.path.splitext(font)[1].lower()[1:]

        if font_name[:7] == "obanner":

            statut = "skipped"

        else:

            cmd = ['figlet', text, '-f', font, '-w', '300']

            try:

                result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            finally:

                if (result.returncode == 0):

                    statut = "ok"

                    # Everything's fine => Output files (text mode)
                    out_1 = "Font: {} ({})\n\n".format(font_name, font_type)
                    output_file.write(out_1)
                    output_file.write(result.stdout.decode("UTF-8"))
                    output_file.write("\n\n")

                    # Output file (HTML mode)
                    out = ET.Element('h3')
                    out.text = out_1
                    html_body.append(out)

                    out = ET.Element('pre', attrib={'class': 'output_text'})
                    out.text = result.stdout.decode("UTF-8").replace(' ', html.unescape('&nbsp;'))
                    html_body.append(out)

                else:

                    # Houston, we got a problem
                    statut = "file error"

        print("Font {} ({}): {}".format(font_name, font_type, statut))

    html_time = ET.Element('p')
    html_time.text = "Generation time: " + str(datetime.datetime.now())
    html_body.append(html_time)

    ET.ElementTree(html_output).write(html_file, encoding='unicode', method='html')
