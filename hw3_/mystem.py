import os

def getMystemTxt(path, filename):
    inTxt = "RVS/plain/%s/%s" % (path, filename)
    outTxt = "./RVS/mystem-plain/%s/" % path
    outXML = "./RVS/mystem-xml/%s/" % path
    if not os.path.exists(outTxt):
        os.makedirs(outTxt)
    if not os.path.exists(outXML):
        os.makedirs(outXML)
    outTxt += filename
    outXML += filename[:-4] + ".xml"
    os.system(r"mystem.exe -d %s %s" % (inTxt, outTxt[2:]))
    os.system(r"mystem.exe -d --format xml %s %s" % (inTxt, outXML[2:]))
