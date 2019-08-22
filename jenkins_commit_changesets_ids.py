from jenkinsapi.jenkins import Jenkins
import sys
import urllib
import datetime
import pytz
from jenkinsapi import build
import re

if len(sys.argv) < 2:
    print "Usage : ", sys.argv[0], " <JENKINSBUILD_URL>"
    sys.exit(-1)

build_url = urllib.unquote(sys.argv[1])
build = build_url.split('/')
# Build Number from the Build URL
build_number = int(build[-1])
# Job Name from the Build URL
job_name = build[-2]
# Jenkins Server Information from Build URL
server = '/'.join(build[0:3])
J = Jenkins(server)
# Metadata for the given build
s=[]
build_metadata = J[job_name].get_build_metadata(build_number)
build_changes=build_metadata.get_changeset_items()
for i in build_changes:
    Workitems=i["msg"]
    #Workitems="<rtcwi>1299523: Implementation for Work Package 1277682 - FS-IC-603-01-02FUN rev 1.0.0 - camera fault warning[X152_MY21_DEV_STREAM]</rtcwi><rtcwi>1299521: Implementation for Work Package 1277682 - FS-IC-603-01-02FUN rev 1.0.0 - camera fault warning[EVA1_JAG_DEV_STREAM]</rtcwi><rtcwi>1299522: Implementation for Work Package 1277682 - FS-IC-603-01-02FUN rev 1.0.0 - camera fault warning[EVA1_X590_DEV_STREAM]</rtcwi><rtcwi>1299519: Implementation for Work Package 1277682 - FS-IC-603-01-02FUN rev 1.0.0 - camera fa"
#l = re.split('[1-9^]*:', Workitems)
    print(Workitems)
#for i in Workitems:
    i=re.findall('[1-9^]*:', Workitems)
    for j in i:
        arr=j.split(':')
        for k in arr:
            if k=='':
                arr.remove(k)
        s.append(arr)
print(s) 
