from jenkinsapi.jenkins import Jenkins
import sys
import urllib
import datetime
import pytz
from jenkinsapi import build

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
build_metadata = J[job_name].get_build_metadata(build_number)
no_of_changesets=len(build_metadata.get_changeset_items())
with open("No_of_commits.properties", "w") as txfile:
    txfile.write("YVALUE={0}".format(no_of_changesets))
