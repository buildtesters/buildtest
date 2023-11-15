#1
buildtest report --helpfilter
buildtest report --helpformat

#2
buildtest report --filter returncode=0

#3
buildtest report --filter tags=e4s

#4
buildtest report --fail --row-count
