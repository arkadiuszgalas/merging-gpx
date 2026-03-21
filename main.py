import datetime
import os
from pathlib import Path

# Ideas for improvements:
# 1. Checking if input directory is not empty
# 2. Checking if gpx filenames have correct naming conventions (places and spaces)
# 3. Moving creating output file to function
# 4. Changing all operation on files and directories to Path objects
# 5. Changing absolute paths into relative

def find_minimum_date(gpx_input_list):
   minimum_ts = datetime.datetime(2040, 12, 31)
   for val in gpx_input_list:
      if val.find("<time>") != -1 and val.find("</time>") != -1 and val.find("<trkpt") != -1:
         date_point = val[val.find("<time>") + 6:val.find("</time>") + 1]
         current_ts = datetime.datetime(int(date_point[0:4]),
                                        int(date_point[5:7]),
                                        int(date_point[8:10]),
                                        int(date_point[11:13]),
                                        int(date_point[14:16]),
                                        int(date_point[17:19]))
         if current_ts < minimum_ts:
            minimum_ts = current_ts
   return minimum_ts

def find_maximum_date(gpx_input_list):
   maximum_ts = datetime.datetime(2000, 1, 1)
   for val in gpx_input_list:
      if val.find("<time>") != -1 and val.find("</time>") != -1 and val.find("</trkpt>") != -1:
         date_point = val[val.find("<time>") + 6:val.find("</time>") + 1]
         current_ts = datetime.datetime(int(date_point[0:4]),
                                        int(date_point[5:7]),
                                        int(date_point[8:10]),
                                        int(date_point[11:13]),
                                        int(date_point[14:16]),
                                        int(date_point[17:19]))
         if current_ts > maximum_ts:
            maximum_ts = current_ts
   return maximum_ts

def bubble_sort(input_list):
   n = len(input_list)
   for k in range(n):
      for j in range(n - k - 1):
         if input_list[j][0] > input_list[j + 1][0]:
            input_list[j], input_list[j + 1] = input_list[j + 1], input_list[j]

def set_filename(input_list,gpx_input_list):
   n = len(input_list)
   start_place = input_list[0][2][0:input_list[0][2].find("_")]
   end_place_first_sep = input_list[n - 1][2].find("_")
   end_place_second_sep = input_list[n - 1][2][end_place_first_sep + 1:].find("_")
   end_place = input_list[n - 1][2][end_place_first_sep + 1:end_place_first_sep + end_place_second_sep + 1]
   filename_out = ''
   for val in gpx_input_list:
      if val.find("<metadata>") != -1 and val.find("</metadata>") != -1:
         date_trip = val[val.find("<time>") + 6:val.find("time") + 15]
         date_trip = date_trip.translate(str.maketrans('', '', '-'))
   datetime_now = str(datetime.datetime.now())
   datetime_now = datetime_now.replace('-','_')
   datetime_now = datetime_now.replace(':','_')
   datetime_now = datetime_now.replace(' ','_')
   datetime_now = datetime_now.replace('.','_')[:-3]

   # creating final version of filename
   filename_out = start_place + '_' + end_place + '_' + date_trip + '_' + datetime_now
   return filename_out

# List gpx_times contains minimum timestamp, maximum timestamp and filename found in input directory
gpx_times = []

files_list = os.listdir('/Users/arkadiuszgalas/Documents/python/merging-gpx/input')
dir_name = os.path.dirname(__file__)
dir_name_input = os.path.join(dir_name,'input')

# Building list: minimum timestamp, maximum timestamp, filename
for file_gpx in files_list:
   gpx_file_input_path = os.path.join(dir_name_input,file_gpx)
   gpx_file = open(gpx_file_input_path, "r", encoding = "utf8")
   gpx_data = gpx_file.read()
   gpx_data_list = gpx_data.split("\n")
   gpx_file.close()

   min_ts_within_gpx = find_minimum_date(gpx_data_list)
   max_ts_within_gpx = find_maximum_date(gpx_data_list)
   list_tmp = [min_ts_within_gpx,max_ts_within_gpx,file_gpx]
   gpx_times.append(list_tmp)

bubble_sort(gpx_times)

gpx_valid = True

# Validating if there is overlaps in gpx files
for i in range(len(gpx_times) - 1):
   if gpx_times[i][1] >= gpx_times[i+1][0]:
      gpx_valid = False

print(f"Validation status: {gpx_valid}")
if gpx_valid:
   # setting output file name
   filename_output = set_filename(gpx_times,gpx_data_list)

   # checking if output directory exists
   output_dir = Path('/Users/arkadiuszgalas/Documents/python/merging-gpx/output')
   if not output_dir.exists():
      os.makedirs('/Users/arkadiuszgalas/Documents/python/merging-gpx/output')

   # creating output .gpx file in output directory
   dir_name_output = os.path.join(dir_name, 'output')
   gpx_file_path_out = os.path.join(dir_name_output, filename_output)
   outputGpxFile = open(gpx_file_path_out, 'w', encoding = 'utf8')

   for l in range(len(gpx_times)):
      gpx_file_path_w = os.path.join(dir_name_input,gpx_times[l][2])
      gpx_file_w = open(gpx_file_path_w, "r", encoding = "utf8")
      gpx_data_w = gpx_file_w.read()
      gpx_data_list_w = gpx_data_w.split("\n")
      gpx_file_w.close()

      if l == 0:
         for val_w in gpx_data_list_w:
            if val_w.find("</trkseg>") == -1 and val_w.find("</trk>") == -1 and val_w.find("</gpx>") == -1:
               outputGpxFile.write(val_w)
               outputGpxFile.write("\n")
      else:
         for val_w in gpx_data_list_w:
            if val_w.find("<trkpt") != -1:
               outputGpxFile.write(val_w)
               outputGpxFile.write("\n")
   outputGpxFile.write("    </trkseg>")
   outputGpxFile.write("\n")
   outputGpxFile.write("  </trk>")
   outputGpxFile.write("\n")
   outputGpxFile.write("</gpx>")
   outputGpxFile.write("\n")
else:
   print("Validation of gpx filed failed.")
