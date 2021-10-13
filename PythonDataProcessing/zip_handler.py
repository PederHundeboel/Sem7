from zipfile import ZipFile


# Create a ZipFile Object and load sample.zip in it
with ZipFile('zip1.zip', 'r') as zipObj:

   listOfFileNames = zipObj.namelist()

   for fileName in listOfFileNames:
       print(fileName)
       if fileName.endswith('20m.jp2'):
           print("llo")
           zipObj.extract(fileName, '20m')


