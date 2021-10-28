from zipfile import ZipFile
import shutil

# Create a ZipFile Object and load sample.zip in it
with ZipFile('zip1.zip', 'r') as zipObj:


    zipObj.extractall('20m')

     # listOfFileNames = zipObj.namelist()
     # for fileName in listOfFileNames:
     #     if fileName.endswith('20m.jp2'):
     #         zipObj.extract(fileName, '20m')



# band 8 på 10

# band 11 eller 12 på 20



source_path = "20m\S2A_MSIL2A_20210925T092031_N0301_R093_T34TDK_20210925T124522.SAFE\GRANULE\L2A_*\IMG_DATA"


source_path = "20m\S2A_MSIL2A_20210925T092031_N0301_R093_T34TDK_20210925T124522.SAFE\GRANULE\L2A_T34TDK_A032694_20210925T092343\IMG_DATA"
destination_path = "bands"
new_location = shutil.move(source_path, destination_path)

path = "S2A_*/GRANULE/L2A_*/IMG_DATA"