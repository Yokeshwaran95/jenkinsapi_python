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
from requests import ConnectionError
from jenkinsapi import jobs
from jenkinsapi import job
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

if len(sys.argv) < 3:
    print("Usage : ", sys.argv[0], " <sprint start date> <sprint end date>")
    sys.exit(-1)

mydb = mysql.connector.connect(
  host="136.18.207.134",
  user="yokesh",
  passwd="visteon",
  database="mydb"
)

cursor = mydb.cursor()

cursor.execute("SHOW DATABASES")
for x in cursor:
    print(x)

sql = "DROP TABLE JOBSANDBUILDTABLE"
cursor.execute(sql)
cursor.execute("CREATE TABLE JOBSANDBUILDTABLE (jobname VARCHAR(255), Build_Type VARCHAR(255), Build_Number VARCHAR(255), Build_Status VARCHAR(255), Build_Causes VARCHAR(255), Total_changes VARCHAR(255), Build_date DATE)")


sprint_start_date=sys.argv[1]
sprint_start_date = datetime.strptime(sprint_start_date, "%d/%m/%Y")
sprint_end_date=sys.argv[2]
sprint_end_date = datetime.strptime(sprint_end_date, "%d/%m/%Y")
plot_data=[]
utc=pytz.UTC
username="cjlr"
token="ba39248440718ebd74d2b8d1f8fa0011"
ci_jenkins_url="http://chipd007.chennai.visteon.com:9090"
server=jenkins.Jenkins(ci_jenkins_url, username=username, password=token)
stable_builds,failure_builds,other_status_builds=0,0,0
try:
    for j in server.get_jobs():
        job_instance = server.get_job(j[0])
        #print(job_instance)
        if ('DEV_BUILD' in job_instance.name) or ('INT_NB' in job_instance.name):
            #print(job_instance)
            if ('DEV_BUILD') in job_instance.name:
                build_type="Daily Build"
            if ('INT_NB') in job_instance.name:
                build_type="Nightly Build"
            job_name=job_instance.name
            job=server.get_job(job_instance.name)
            starting_build_number=job.get_first_buildnumber()
            end_build_number=job.get_last_completed_buildnumber()
            print(job)
            try:
                for i in range(starting_build_number, end_build_number):
            #no_of_changes=len(build_metadata.get_changeset_items())
                    build_metadata=server[job_name].get_build_metadata(i)
                    build_date=build_metadata.get_timestamp()
                    build_status=str(build_metadata.get_status())
                    build_actions=build_metadata.get_actions()
                    no_of_changes=str(len(build_metadata.get_changeset_items()))
                    build_date=build_date.replace(tzinfo=utc)
                    print(build_date)
                    sprint_end_date=sprint_end_date.replace(tzinfo=utc)
                    sprint_start_date = sprint_start_date.replace(tzinfo=utc)
            
                    if (build_date > sprint_start_date) and (build_date < sprint_end_date):
                        try:
                            print(no_of_changes)
                            i=str(i)
                            job=str(job)
                            print(i)
                            print(build_date)
                            #print(type(build_date))
                            #print(type(build_type))
                            build_type=str(build_type)
                            print(build_status)
                            if (build_status== "FAILURE") or (build_status== "UNSTABLE"):
                                try:
                                    build_failure_reason=build_actions["text"]
                                    build_failure_reason=str(build_failure_reason)
                                    #print(type(build_failure_reason))
                                except KeyError:
                                    print("OOPS!! build may be failed due to an unknown cause")
                                    build_failure_reason=str("Unknown Failure")
                            else:
                                build_failure_reason=str("Success")
                                                
                    #cursor = connection.cursor(prepared=True)                
                            sql_insert_query = """ INSERT INTO `JOBSANDBUILDTABLE`
                                    (`jobname`,`Build_Type`, `Build_Number`, `Build_Status`, `Build_Causes`, `Total_changes`, `Build_Date`) VALUES (%s,%s,%s,%s,%s,%s,%s)"""

                            insert_tuple = (job, build_type, i, build_status, build_failure_reason, no_of_changes,build_date)
                            
                    #sql = "UPDATE customers SET address = 'Canyon 123' WHERE address = 'Valley 345'"
                            result  = cursor.execute(sql_insert_query, insert_tuple)
                            mydb.commit()
                            print ("Record inserted successfully into JOBSANDBUILDTABLE")
                        except mysql.connector.Error as error:
                            mydb.rollback()
                            print("Failed to insert into MySQL table {}".format(error))
                        
                        
                    
            except NotFound as error:
                i=i+1
                build_metadata=server[job_name].get_build_metadata(i)
                build_date=build_metadata.get_timestamp()
                build_status=build_metadata.get_status()
                no_of_changes=len(build_metadata.get_changeset_items())
                print(job)
                build_date=build_date.replace(tzinfo=utc)
                print(build_date)
                print(i)
except requests.ConnectionError:
    print("The connection is lost")
   