# 🗺️ GPX File Merger

**merging-gpx.py** is a simple Python script that merges multiple `.gpx` files 
into a single GPX file.  
It’s useful for combining GPS tracks from different recordings into one 
continuous route.
---

## 📋 Features

- Merge multiple `.gpx` files into one
- Merged tracks are sorted from oldest to newest
- Output file is saved to output directory in main directory

---

## 🚀 Ideas for improvements
1. Adding check if gpx filenames have correct naming conventions (places and spaces)
2. Moving creating output file to function
3. Changing all operation on files and directories into Path objects
4. Changing absolute paths into relative ones
5. Moving all functions to separate module
6. Checking if gpx files were generated the same day
