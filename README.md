# xcsoar_cupx_decoder
 
This python-script can be used to extract files from a cupx-file, that can be processed by XCsoar.

The only dependency is binwalk (Installing: sudo apt install binwalk).

The script is called with the cupx-file's path as an argument (python cupx_convert.py YourFilesName.cupx) and viola...
...all files required for XCsoar are now located inside a newly created folder, named after the cupx-file.

In order to make it work inside XCsoar:
Copy all files from inside the folder into your XCSoarData-folder on your device, select the .cup-file as a waypoint file and the .txt-file as waypoint-details-file and have fun!!!
