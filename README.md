# merging-gpx
Script reads all .gpx files in input directory.
Scripts finds minimum and maximum timestamp in every file. Next validation is done i.e.
checking if there are no overlaps/duplicates between files. Files are sorted
in ascending way i.e. from oldest to newest.
If validation is correct script merges all gpx files into one (that can be
uploaded e.g. to Strava).
