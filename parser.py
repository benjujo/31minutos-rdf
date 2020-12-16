import wikitextparser as wtp
import os

with open('Articles/Guaripolo.txt', 'r') as file:
    parsed = wtp.parse(file.read())
    print(parsed.templates[0])

path = 'Articles/'
##borre las carpetas para no tener problemas
fileList = os.listdir(path)
for file in fileList:
    file = open(path+file, "r")
    parsed = wtp.parse(file.read())
    templates= parsed.templates
    if templates:
        print(templates[0])