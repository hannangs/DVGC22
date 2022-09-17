
titel="jag hatar /"
errorRakning=0

if '/' in titel:
    print(titel)
    titel=titel.replace('/', ' eller ')
    #titel=(titel.translate({ord('/'): None}))
    print(titel)
else:
    print("Fel")

