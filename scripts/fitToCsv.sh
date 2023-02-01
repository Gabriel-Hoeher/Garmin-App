#! /bin/bash 

cd ../activity_data

#iterates through all fit files
for i in *.fit; do
    name=$(basename -s .fit $i)
    csv="$name.csv"
    #checks if csv already created
    if [ ! -f "$csv" ]; then
        java -jar ../sdk/java/FitCSVTool.jar $i      
    fi                                           
done