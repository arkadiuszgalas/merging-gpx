import datetime
import os

# Script creates list containing of: filename, minimum timestamp, maximum timestamp
# Script sorts list by minimum timestamp (found within .gpx file)

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
print(f"VAlidation status: {gpx_valid}")
