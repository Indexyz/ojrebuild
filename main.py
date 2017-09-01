import ojdkbuild as grelease
import urllib
import requests
import random
import zipfile
import shutil
import os

BUILD_TAG = "1.8.0.141-1"

def unzipToRandomFolder(filename):
    randomDir = str(random.randint(1, 100000))
    if os.path.isdir(randomDir):
        os.makedirs(randomDir)

    zfile = zipfile.ZipFile(filename, 'r')

    for item in zfile.namelist():
        if not item.endswith('/'):
            f = os.path.join(randomDir, item)
            d = os.path.dirname(f)
            if not os.path.exists(d):
                os.makedirs(d)
            file(f, 'wb').write(zfile.read(item))
    zfile.close()
    return randomDir

def createZip(source, name):
    source = source.decode('utf-8')
    name = name.decode('utf-8')
    filelist = []
    if os.path.isfile(source):
        filelist.append(source)
    else:
        for root, dirs, files in os.walk(source):
            for file in files:
                filelist.append(os.path.join(root, file))
        zf = zipfile.ZipFile(name, 'w', zipfile.zlib.DEFLATED)
        for tar in filelist:
            arcname = tar[len(source):]
            zf.write(tar, arcname)
        zf.close()

def downloadAndUnzip(item):
    print "Downloading: " + item["name"]
    tName = item["name"]
    urllib.urlretrieve(
        item["url"], tName
    )

    rDir = unzipToRandomFolder(tName)
    os.remove(tName)
    javaDirName = ""

    for item in os.listdir(rDir):
        if item.startswith("java"):
            javaDirName = item
            break
        
    createZip(str(rDir) + "/" + javaDirName + "/jre", tName.replace("openjdk", "openjre"))
    shutil.rmtree(rDir)

def main():
    items = grelease.getReleaseAssets(BUILD_TAG)
    items = grelease.getBinaryOfWindows(items)

    for item in items:
        downloadAndUnzip(item)

main()