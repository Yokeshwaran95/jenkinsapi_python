import requests
from jenkinsapi import jenkins
from jenkinsapi.job import Job
import csv
import time
import logging
import warnings
from datetime import datetime, timedelta
import sys
from time import sleep
import pytz
from jenkinsapi import config
from jenkinsapi.artifact import Artifact
from jenkinsapi.result_set import ResultSet
from jenkinsapi.jenkinsbase import JenkinsBase
from jenkinsapi.constants import STATUS_SUCCESS
from jenkinsapi.custom_exceptions import NoResults
from jenkinsapi.custom_exceptions import JenkinsAPIException
from jenkinsapi.custom_exceptions import NotFound
from jenkinsapi import build
from six.moves.urllib.parse import quote
from requests import HTTPError
from requests.exceptions import ConnectionError
from jenkinsapi import jobs
from jenkinsapi import job
from fpdf import FPDF
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
username="cjlr"
token="ba39248440718ebd74d2b8d1f8fa0011"
ci_jenkins_url="http://chipd007.chennai.visteon.com:9090"
server=jenkins.Jenkins(ci_jenkins_url, username=username, password=token)
stable_builds,failure_builds,other_status_builds=0,0,0
pdf_arr=[["BUILD_TYPE","JOB_NAME","LAST JOB BUILD NUMBER", "CURRENT_BUILD_NUMBER","IS JOB RUNNING?", "BUILD STATUS","BUILD_DURATION","BUILD_FAILED_REASON", "TRIGGERED_BY", "BUILD_START_TIME","BUILT ON", "TOTAL_COMMITS", "CCP_TEST_FAILURES"]]

try:
    for j in server.get_jobs():
        job_instance = server.get_job(j[0])
        if ('DEV_BUILD' in job_instance.name) or ('INT_NB' in job_instance.name):
            if ('DEV_BUILD') in job_instance.name:
                build_type="Daily Build"
            if ('INT_NB') in job_instance.name:
                build_type="Nightly Build"
            job_name=job_instance.name
            job=server.get_job(job_instance.name)
            #Built_on_node=job.get_slave()
            print(job)
            job_running=job.is_running()
            #print(type(job.is_running()))
            if(job.is_running()==True):
                current_build=job.get_last_buildnumber()

            else:
                current_build=job.get_last_completed_buildnumber()
            current_build_metadata=server[job_name].get_build_metadata(current_build)
            build_status=current_build_metadata.get_status()
            build_actions=current_build_metadata.get_actions()
            Built_on_node=current_build_metadata.get_slave()
            No_of_changesets=current_build_metadata.get_changeset_items()
            No_of_changesets=len(No_of_changesets)
            build_duration=current_build_metadata.get_duration()
            build_start_time=current_build_metadata.get_timestamp()
            if (build_status== "FAILURE") or (build_status== "UNSTABLE") or (build_status=="ABORTED") or (build_status=="NONE"):
                try:
                    build_failure_reason=build_actions["text"]
                    
                    build_failure_reason=str(build_failure_reason)
                except KeyError:
                    build_failure_reason=str("Reason Unknown")
            else:
                build_failure_reason="Passed"
            print(build_failure_reason)
            #print(type((build_actions["causes"])[-1]))
            build_trigger_cause=((build_actions["causes"])[-1])
            build_trigger_cause=build_trigger_cause["shortDescription"]
            print(build_trigger_cause)
            if ('INT_NB' in job_instance.name):
                try:
                    CCP_Test_Failures=build_actions["failCount"]
                except KeyError:
                    CCP_Test_Failures="NA"
            else:
                CCP_Test_Failures="NA"
            job=str(job)
            build_duration=str(build_duration)
            build_start_time=str(build_start_time)
            print(CCP_Test_Failures)
            build_details=[]
            build_details.append(str(build_type))
            build_details.append(str(job))
            last_build_number=int((current_build)-1)
            last_build_number=str(last_build_number)
            build_details.append(last_build_number)
            build_details.append(str(current_build))
            build_details.append(str(job_running))
            build_details.append(str(build_status))
            build_details.append(str(build_duration))
            build_details.append(str(build_failure_reason))
            build_details.append(str(build_trigger_cause))
            build_details.append(str(build_start_time))
            build_details.append(str(Built_on_node))
            build_details.append(str(No_of_changesets))
            build_details.append(str(CCP_Test_Failures))
            #print(build_details)
            pdf_arr.append(build_details)
            #print(pdf_arr)
            print("\n\n\n")
except ConnectionError:
    print("Connection lost")
except HTTPError:
    print("Connection lost")
print("\n\n\n")
seen = set()
newlist = []
for item in pdf_arr:
    t = tuple(item)
    if t not in seen:
        newlist.append(item)
        seen.add(t)
#print(newlist)
print("\n\n\n")
#print(seen)
print("*********************************************Data Fetched**********************************************")
with open("report.csv", 'w') as reportfile:
    writee=csv.writer(reportfile)
    writee.writerows(newlist)


    

        
        


                

