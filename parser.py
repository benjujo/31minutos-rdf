import wikitextparser as wtp
with open('Articles/Guaripolo.txt', 'r') as file:
    parsed = wtp.parse(file.read())
