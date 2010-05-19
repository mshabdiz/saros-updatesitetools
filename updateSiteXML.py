#! /usr/bin/python

"""helper script to add entries to Eclipse PDE style site.xml files"""

import os, sys, re
import xml.etree.ElementTree as ET

## Configurable part

inputfilename = "site.xml"
outputpostfix = ".new"
urlbase = "http://downloads.sourceforge.net/dpp/"
urlpostfix = "?use_mirror=dfn"
packagename = "de.fu_berlin.inf.dpp"
featureid = packagename+".feature"
pathbase = "plugins/"

featurefile = "de.fu_berlin.inf.dpp.feature_9.10.2.r1804.jar"
pluginfile = "de.fu_berlin.inf.dpp_9.10.2.r1803.jar"

featureversion_re = re.compile(featureid + "_(.*)\.jar")
pluginversion_re = re.compile(packagename + "_(.*)\.jar")

# if you change things below this line, you should know what
# you're doing!

def usage():
    print sys.argv[0] + " SITE.XML JAR_DIR"
    sys.exit(1)

if __name__ == '__main__':
    if not len(sys.argv) == 3:
        usage()
    inputfilename = sys.argv[1]
    jardir = sys.argv[2]

    if not os.path.isdir(jardir):
        print "Directory " + jardir + " does not exist!"
        sys.exit(1)

    featurefile = None
    featureversion = None
    pluginfile = None
    pluginversion = None
    print "Looking in dir " + jardir
    for f in os.listdir(jardir):
        mf = featureversion_re.search(f)
        mp = pluginversion_re.search(f)
        if mf:
            featurefile = f
            featureversion = mf.group(1)
            print "found feature file " + featurefile +\
                  "version " + featureversion
        if mp:
            pluginfile = f
            pluginversion = mp.group(1)
            print "found plugin file " + pluginfile +\
                  "version " + pluginversion
    
    if (featureversion == None):
        print "Could not determine version of feature, exiting"
        sys.exit(1)
    if (featureversion != pluginversion):
        print "feature version is " + featureversion +\
        " but pluginversion is " + pluginversion + ", something's wrong!"
        print "Exiting!"
        sys.exit(1)

    tree = ET.parse(inputfilename)
    root = tree.getroot()
    found = False
    features = root.findall("feature")
    for f in features:
        if(f.attrib.get("version") == featureversion):
            found = True
            print "feature version " + featureversion + " already exists"

    # if feature is missing, we don't check archive entries!
    if not found:
        # add feature element
        print "feature version " + featureversion + " not found, adding"
        newfeature = ET.SubElement(root,"feature",
                                   url=urlbase+featurefile+urlpostfix,
                                   id=featureid, version=featureversion)
        ET.SubElement(newfeature,"category",name="DPP")
        # add archive element
        ET.SubElement(root,"archive", path=pathbase + pluginfile,
                      url=urlbase+pluginfile+urlpostfix)
        tree.write(inputfilename)
