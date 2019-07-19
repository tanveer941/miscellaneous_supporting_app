
# coding: utf-8

# In[42]:


from cx_Oracle import connect as cx_connect
from cx_Oracle import DatabaseError


# In[43]:


ORC_CONN = cx_connect("ALGO_DB_USER", "read", "racadmpe", False)


# In[44]:


ORC_CURSOR = ORC_CONN.cursor()
stmt = ''' select PRJ_FUNC,DEPARTMENT, RECFILENAME,COUNTRY,ROAD_TYPE,LIGHT_CONDITIONS,WEATHER
FROM adms_teststage.ADMS_RESTRUCTURED_ENV_LABELS
where ROWNUM<100 ORDER BY RECFILENAME'''
ORC_CURSOR.execute(stmt)
ORC_CURSOR.arraysize = 50
data = ORC_CURSOR.fetchall()
all_data = []
for item in data:
    colun_names = [column[0] for column in ORC_CURSOR.description]
    # print "colun_names",colun_names
    data = dict(zip(colun_names, item))
    all_data.append(data)


# In[45]:


all_data


# In[46]:


import pandas as pd
ldss_dtfr = pd.DataFrame(all_data)
# ldss_dtfr.to_csv("ldss.csv", encoding='utf-8', index=False)


# In[47]:


ldss_dtfr


# In[48]:


# Add a new project and function column
def get_element(my_list, position):
    return my_list[position]
ldss_dtfr['PROJECT'] = ldss_dtfr.PRJ_FUNC.str.split('_').apply(get_element, position=0)
ldss_dtfr['FUNCTION'] = ldss_dtfr.PRJ_FUNC.str.split('_').apply(get_element, position=1)
ldss_dtfr


# In[49]:


# Index the Dataframe by recording name
idx_rec_dtfr = ldss_dtfr.set_index(['RECFILENAME'])
idx_rec_dtfr


# In[50]:


# Delete the PRJ_FUNC column
del idx_rec_dtfr['PRJ_FUNC']
idx_rec_dtfr


# In[51]:


# data_grp = sel_data.set_index(['COUNTRY','DEPARTMENT','LIGHT_CONDITIONS','PRJ_FUNC','ROAD_TYPE','WEATHER'])
# data_grp
# Get distinct rec names
# distinct_rec_names = idx_rec_dtfr.index.unique()
# # dir(distinct_rec_names)
# rec_names_lst = distinct_rec_names.tolist()
# rec_names_lst, len(rec_names_lst)


# In[58]:


ORC_CURSOR = ORC_CONN.cursor()
stmt = ''' SELECT DISTINCT(SR_SIGN_CLASS), "RecIdFileName"
FROM adms_teststage.MFC400_SR_LDROI_B 
WHERE "RecIdFileName" IN {} ORDER BY "RecIdFileName" '''.format(tuple(rec_names_lst))
ORC_CURSOR.execute(stmt)
ORC_CURSOR.arraysize = 50
data = ORC_CURSOR.fetchall()
obj_data = []
for item in data:
    colun_names = [column[0] for column in ORC_CURSOR.description]
    # print "colun_names",colun_names
    data = dict(zip(colun_names, item))
    obj_data.append(data)
    
obj_data


# In[61]:


ldroi_dtfr = pd.DataFrame(obj_data)
ldroi_dtfr.columns = ['RECFILENAME','SR_SIGN_CLASS']
ldroi_dtfr


# In[70]:


merged_dtfr = pd.merge(ldss_dtfr, ldroi_dtfr, on='RECFILENAME', how='right')
mergd_idxd_ldroi = merged_dtfr.set_index(['RECFILENAME'])
del mergd_idxd_ldroi['PRJ_FUNC']
mergd_idxd_ldroi


# In[77]:


distinct_rec_names = mergd_idxd_ldroi.index.unique()
# dir(distinct_rec_names)
rec_names_lst = distinct_rec_names.tolist()
rec_names_lst, len(rec_names_lst)


# In[71]:


sel_data = mergd_idxd_ldroi.loc['Snapshot_2015.07.23_at_12.56.57.rec']
sel_data


# In[53]:


# ech_rec_dtfr = sel_data.reset_index()
# country = ech_rec_dtfr['COUNTRY'].unique().tolist()
# dpt_type = ech_rec_dtfr['DEPARTMENT'].unique().tolist()
# lc_type = ech_rec_dtfr['LIGHT_CONDITIONS'].unique().tolist()
# prj_type = ech_rec_dtfr['PROJECT'].unique().tolist()
# func_type = ech_rec_dtfr['FUNCTION'].unique().tolist()
# rd_type = ech_rec_dtfr['ROAD_TYPE'].unique().tolist()
# wthr_type = ech_rec_dtfr['WEATHER'].unique().tolist()
# rd_type


# In[74]:


clmn_names_lst = mergd_idxd_ldroi.columns.tolist()
clmn_names_lst


# In[78]:


# Iterate through each recording

lst_data = []
for ech_rec in rec_names_lst:
    rec_dict = {}
    sel_data = mergd_idxd_ldroi.loc[ech_rec]
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
#     print sel_data
    ech_rec_dtfr = sel_data
#     print ech_rec_dtfr
    rec_dict['RECFILENAME'] = ech_rec
    
    for ech_clmn_name in clmn_names_lst:
#         print ech_rec_dtfr[ech_clmn_name]
        if type(ech_rec_dtfr) is pd.Series:
            clmn_data = ech_rec_dtfr[ech_clmn_name]
#             print ">>>", clmn_data
            rec_dict[ech_clmn_name] = [clmn_data]
        else:
            clmn_data = ech_rec_dtfr[ech_clmn_name].unique().tolist()
            rec_dict[ech_clmn_name] = clmn_data
#     print "rec_dict :: ", rec_dict
    lst_data.append(rec_dict)
    


# In[79]:


lst_data


# In[80]:


# Dump the data into a JSON
import json
with open("ldss.json", 'w+') as outfile:
    json.dump(lst_data, outfile, indent=4)

