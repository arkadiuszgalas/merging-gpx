# 🗺️ GPX File Merger

**merging-gpx.py** is a simple Python script that merges multiple `.gpx` files 
into a single GPX file.  
It’s useful for combining GPS tracks from different recordings into one 
continuous route.
---

## 📋 Features

- Merge multiple `.gpx` files into one
- Merged tracks are sorted from oldest to newest
- Output file is saved to output directory in main directory /Users/arkadiuszgalas/Documents/python/merging-gpx/output
- Merged files should have naming pattern [Place1]_[Place2]_[other_information].gpx e.g. Prague_Brno_2072024.gpx
- Merged files should not be duplicated
- Merged files should not overlap (in sense of time registered in files)
---

## 🚀 Ideas for improvements
1. Moving creating output file to function
2. Changing all operation on files and directories into Path objects
3. Changing absolute paths into relative ones
4. Moving all functions to separate module
5. Checking if gpx files were generated the same day
