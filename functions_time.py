from datetime import datetime

# Function find_minimum_date returns minimum timestamp found on list containing .gpx file
def find_minimum_date(gpx_input_list):
   minimum_ts = datetime(2040, 12, 31)
   for val in gpx_input_list:
      if val.find("<time>") != -1 and val.find("</time>") != -1 and val.find("<trkpt") != -1:
         date_point = val[val.find("<time>") + 6:val.find("</time>") + 1]
         current_ts = datetime(int(date_point[0:4]),
                               int(date_point[5:7]),
                               int(date_point[8:10]),
                               int(date_point[11:13]),
                               int(date_point[14:16]),
                               int(date_point[17:19]))
         if current_ts < minimum_ts:
            minimum_ts = current_ts
   return minimum_ts

# Function find_maximum_date returns maximum timestamp found on list containing .gpx file
def find_maximum_date(gpx_input_list):
   maximum_ts = datetime(2000, 1, 1)
   for val in gpx_input_list:
      if val.find("<time>") != -1 and val.find("</time>") != -1 and val.find("</trkpt>") != -1:
         date_point = val[val.find("<time>") + 6:val.find("</time>") + 1]
         current_ts = datetime(int(date_point[0:4]),
                               int(date_point[5:7]),
                               int(date_point[8:10]),
                               int(date_point[11:13]),
                               int(date_point[14:16]),
                               int(date_point[17:19]))
         if current_ts > maximum_ts:
            maximum_ts = current_ts
   return maximum_ts
