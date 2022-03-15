import sys
import os
import csv

cupx_file = sys.argv[1]
cupx_file_name = os.path.basename(cupx_file)
cupx_file_stem = os.path.splitext(cupx_file)[0]
binwalk_output_folder_name = "_{}.cupx.extracted".format(cupx_file_stem)
cup_file = "{}.cup".format(cupx_file_stem)

os.system("binwalk -e {}".format(cupx_file))

if os.path.isdir(binwalk_output_folder_name):
    os.rename(binwalk_output_folder_name, "{}_xcsoar".format(cupx_file_stem))
binwalk_output_folder_name = "{}_xcsoar".format(cupx_file_stem)

binwalk_output_files = os.listdir(binwalk_output_folder_name)
for tmp_file in binwalk_output_files:
    if tmp_file[-4:] == ".cup":
        #Give it  multiple tries if required, since renaming the folder might cause some issues when it comes to renaming the .cup-file
        while True:
            try:
                os.rename(os.path.join(binwalk_output_folder_name, tmp_file), os.path.join(binwalk_output_folder_name, "{}.cup".format(cupx_file_stem)))
                break
            except:
                print("ERROR: Renaming {} to {} might have failed!".format(os.path.join(binwalk_output_folder_name, tmp_file), os.path.join(binwalk_output_folder_name, "{}.cup".format(cupx_file_stem))))
    if tmp_file[-4:] == ".zip":
        os.remove(os.path.join(binwalk_output_folder_name, tmp_file))
    if os.path.isdir(os.path.join(binwalk_output_folder_name, tmp_file)):
        os.rename(os.path.join(binwalk_output_folder_name, tmp_file), os.path.join(binwalk_output_folder_name, "{}_pics".format(cupx_file_stem)))

print("Parse {} and extract image paths...".format(os.path.join(binwalk_output_folder_name,cup_file)))
with open(os.path.join(binwalk_output_folder_name,cup_file), 'r') as csv_in_file:
    csv_reader = csv.reader(csv_in_file)
    print("Generate {}...".format(os.path.join(binwalk_output_folder_name, "{}_details.txt".format(cupx_file_stem))))
    output_file = open(os.path.join(binwalk_output_folder_name, "{}_details.txt".format(cupx_file_stem)), 'w')
    pics_folder_name = "{}_pics".format(cupx_file_stem)
    for row in csv_reader:
        # skip the cup header
        if row[0] == "name":
            continue
        # bullet proofing: if the field 14 does not exist skip the row
        if len(row) >= 14 and row[13]:
            output_file.write("[" + row[0] + "]\n")
            if ';' in row[13]:
                for item in row[13].split(';'):
                    if '.jpg' in item:
                        output_file.write("image=" + pics_folder_name + "/" + item + "\n")
                    if '*.pdf' in item:
                        output_file.write("file=docs/" + item + "\n")
            else:
                if '.jpg' in row[13]:
                    output_file.write("image=" + pics_folder_name + "/" + row[13] + "\n")
                if '.pdf' in row[13]:
                    output_file.write("file=docs/" + row[14] + "\n")
        else:
            continue
            # Add newline for better readability
            output_file.write("\n")
    output_file.close()