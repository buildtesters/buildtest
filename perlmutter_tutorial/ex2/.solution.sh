#1
buildtest buildspec find --tags

#2
buildtest buildspec find --helpfilter
buildtest buildspec find --helpformat

#3
buildtest buildspec find --format name,description

#4
buildtest buildspec find --filter tags=e4s

#5
buildtest buildspec find invalid

#6
buildtest buildspec validate -t e4s

#7
buildtest buildspec show hello_world_openmp