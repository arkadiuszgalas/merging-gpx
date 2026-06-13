import datetime
from pathlib import Path
from functions_time import find_minimum_date,find_maximum_date

def bubble_sort(input_list):
   n = len(input_list)
   for k in range(n):
      for j in range(n - k - 1):
         if input_list[j][0] > input_list[j + 1][0]:
            input_list[j], input_list[j + 1] = input_list[j + 1], input_list[j]

def set_filename(input_list,gpx_input_list):
   n = len(input_list)
   input_list_0 = str(input_list[0][2].name)
   start_place = input_list_0[0:input_list_0.find("_")]

   input_list_n_1 = str(input_list[n - 1][2].name)
   end_place_first_sep = input_list_n_1.find("_")
   end_place_second_sep = input_list_n_1[end_place_first_sep + 1:].find("_")
   end_place = input_list_n_1[end_place_first_sep + 1:end_place_first_sep + end_place_second_sep + 1]

   date_trip = ''
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
   filename_out = start_place + '_' + end_place + '_' + date_trip + '_' + datetime_now + '.gpx'
   return filename_out

def check_naming_convention(gpx_files_input_list):
   file_is_correct = True
   for filename in gpx_files_input_list:
      gpx_name = str(filename.name)
      if gpx_name.find("_") != -1 and gpx_name[gpx_name.find("_") + 1:].find("_") != -1:
         file_is_correct = True
      else:
         file_is_correct = False
   return file_is_correct

# Checking if input directory exists
input_dir = Path.cwd() / 'input'
gpx_valid = True

if input_dir.exists():
   # List gpx_times contains minimum timestamp, maximum timestamp and filename found in input directory
   gpx_times = []
   files_list = list(input_dir.glob('*.gpx'))

   # Checking if input directory contains more than one file
   if len(files_list) > 1:
      # Checking if all gpx files from input directory have correct naming convention
      namesCorrect = check_naming_convention(files_list)
      if namesCorrect:
         # Building list: minimum timestamp, maximum timestamp, filename
         for file_gpx in files_list:
            gpx_file = open(file_gpx, "r", encoding = "utf8")
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

         if gpx_valid:
            # setting output file name
            filename_output = set_filename(gpx_times,gpx_data_list)

            # checking if output directory exists
            output_dir = Path.cwd() / 'output'
            output_dir.mkdir(parents = True, exist_ok = True)

            # creating output .gpx file in output directory
            gpx_file_path_out = Path(output_dir, filename_output)
            outputGpxFile = open(gpx_file_path_out, 'w', encoding = 'utf8')

            for l in range(len(gpx_times)):
               gpx_file_path_w = input_dir / gpx_times[l][2]
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
            print("Validation of gpx filed. There are overlapping ranges or duplicates in data.")
      else:
         print("Validation of naming convention failed.")
   else:
      print("Input directory contains less than 2 files. Processing stopped.")
else:
   print("Directory input does not exists. Processing stopped.")
