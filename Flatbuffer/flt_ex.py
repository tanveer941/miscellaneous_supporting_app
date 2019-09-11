"""
flatc -p -b scm.fbs scm.json

"""


from ReposList import ReposList
from Repo import Repo
import flatbuffers
from datetime import datetime
import time
import json

st_time = datetime.now()
buf = open('scm.bin', 'rb').read()
buf = bytearray(buf)
repo_lst_obj = ReposList.GetRootAsReposList(buf, 0)
# print monster
repo_obj = repo_lst_obj.Repos(0)
name = repo_obj.FullName()

ed_time = datetime.now()
duration = ed_time - st_time

print name
print "duration of flatbuff::", duration.total_seconds() * 1000

#===================================================
st_timej = datetime.now()
with open('scm.json') as ldroi_json:
    ldroi = json.load(ldroi_json)
full_name = ldroi["repos"][0]["full_name"]
print full_name
ed_timej = datetime.now()
duration_json = ed_timej - st_timej
print "duration of JSON::", duration_json.total_seconds() * 1000
