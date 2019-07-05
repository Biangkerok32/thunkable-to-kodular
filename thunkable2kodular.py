#encoding: utf-8
from sys import argv
from os import path,mkdir,walk,chdir
from shutil import rmtree
from zipfile import is_zipfile,ZipFile,ZIP_DEFLATED
from glob import iglob
from fileinput import FileInput
from ntpath import basename

replace_list=[["ThunkablePushNotification","PushNotifications"],["ThunkableFloatingActionButton","MakeroidFab"],["ThunkableAdMobInterstitial","AdMobInterstitial"],["ThunkableAdMobBanner","AdmobBanner"],["ThunkableSwitch\",\"$Version\":\"6=","SwitchToggle\",\"$Version\":\"3"],["ThunkableSwitch","SwitchToggle"]]

if len(argv)==2:
    print("Converting "+argv[1]+" to Kodular...")
    temp_folder_name="."+basename(argv[1])+"_temp"
    if path.isfile(argv[1]):
        if path.exists(temp_folder_name):
            rmtree(temp_folder_name)
        mkdir(temp_folder_name)
        if is_zipfile(argv[1]):
            aia_file=ZipFile(argv[1])
            aia_file.extractall(path=temp_folder_name)
            aia_file.close()
            #=== I need to change this part because LF are converted to CRLF
            for i in iglob(temp_folder_name+"/src/com/*/*/*",recursive=1):
                for t in replace_list:
                    for line in FileInput(i,inplace=1):
                        print(line.replace(t[0],t[1]),end="")
            #===
            extension=path.splitext(argv[1])[1]
            new_file_name=path.splitext(argv[1])[0]
            new_aia_file=ZipFile(new_file_name+"_kodular"+extension,"w",ZIP_DEFLATED)
            temp_dir_path=path.realpath(temp_folder_name)
            chdir(temp_folder_name)
            for dirs,sdirs,files in walk(temp_dir_path):
                for f in files:
                    new_aia_file.write(path.relpath(dirs)+"/"+f)
            new_aia_file.close()
            chdir("..")
            rmtree(temp_folder_name)
            print("Done! You can import "+new_file_name+"_kodular"+extension+" in Kodular.")
        else:
            print(argv[1]+" is not a valid AIA file")
            rmtree(temp_folder_name)
else:
    print("Drop an AIA file to "+path.basename(argv[0])+" or type \""+path.splitext(path.basename(argv[0]))[0]+" <AIA file>\" in the terminal")
