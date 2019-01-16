#must install tesseract Util.

import config

from subprocess import call


working_directory = config.get_root_directory()+"/data/temp/"

newFileName = "test"
resized_file = working_directory +"/"+newFileName+".png"

output_file = working_directory+"/out"


corpped_file = working_directory +"/timing.png"



call(["tesseract", resized_file, output_file])

file = output_file +".txt"

for line in open(file,'r'):
    #print(line)
    pass