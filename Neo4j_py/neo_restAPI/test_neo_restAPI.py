
from neo4jrestclient.client import GraphDatabase
import json


gdb = GraphDatabase("http://10.223.242.11:7474/db/data/", username="neo4j", password="tan_neo4j")
# pyinstaller rec_summary_events_rc.py -w --add-data summary.txt;.
# print gdb

data_lst_dct = [{"RECFILENAME": "Continuous_2011.07.04_at_14.37.07.rec", "PROJECT": "MFC400", "FUNCTION": "SR", "DEPARTMENT": "DEV", "COUNTRY": ["Germany", "Austria"],
                 "ROAD_TYPE": ["Highway", "City"], "LIGHT_CONDITIONS": ["Day", "Night"], "WEATHER": ["Dry", "Rain"]},
                {"RECFILENAME": "Snapshot_2015.07.23_at_12.56.57.rec", "PROJECT": "MFC300", "FUNCTION": "SR", "DEPARTMENT": "DEV", "COUNTRY": ["USA", "Great_Britain"],
                 "ROAD_TYPE": ["Other", "Motorway"], "LIGHT_CONDITIONS": ["Day", "Dusk"], "WEATHER": ["Rain"]},
                {"RECFILENAME": "20141215_1540_{08627FB2-FDC3-414E-92B3-EBE39884DA8F}.rrec", "PROJECT": "MFC500", "FUNCTION": "SR", "DEPARTMENT": "DEV", "COUNTRY": ["TAIWAN", "Austria"],
                 "ROAD_TYPE": ["Country_Road", "Highway"], "LIGHT_CONDITIONS": ["Dusk", "Night"], "WEATHER": ["Dry"]},
                ]

# data_lst_dct = ''
with open("ldss.json") as outfile:
    # self.config_schema = OrderedDict(json.load(outfile))
    data_lst_dct = json.load(outfile)


for ech_rcord_dict in data_lst_dct:

    print ("ech_rcord_dict :: ", ech_rcord_dict["RECFILENAME"])
    # Create recording node
    rec_node = gdb.node(name=ech_rcord_dict["RECFILENAME"])
    rec_node.labels.add("RecordingName")
    print ("Created rec node.....")
    # Create common data node
    cmn_data_node = gdb.node(project=ech_rcord_dict["PROJECT"], function=ech_rcord_dict["FUNCTION"],
                             department=ech_rcord_dict["DEPARTMENT"])
    cmn_data_node.labels.add("CommonData")
    # Establish relationship with rec and common data node
    rec_node.relationships.create("cd", cmn_data_node)
    print ("Created common data node.....")

    # Create country node
    cntry_node = gdb.node(name=ech_rcord_dict["COUNTRY"])
    cntry_node.labels.add("Country")
    # Establish relationship with rec and country node
    rec_node.relationships.create("c", cntry_node)
    print ("Created country node.....")

    # Create road type node
    road_typ_node = gdb.node(name=ech_rcord_dict["ROAD_TYPE"])
    road_typ_node.labels.add("RoadType")
    # Establish relationship with rec and country node
    cntry_node.relationships.create("rt", road_typ_node)
    print ("Created road type node.....")

    # Create weather node
    wthr_cond_node = gdb.node(name=ech_rcord_dict["WEATHER"])
    wthr_cond_node.labels.add("WeatherCondition")
    # Establish relationship with rec and country node
    road_typ_node.relationships.create("w", wthr_cond_node)
    print ("Created Weather condition node.....")

    # Create light condition node
    lght_cond_node = gdb.node(name=ech_rcord_dict["LIGHT_CONDITIONS"])
    lght_cond_node.labels.add("LightCondition")
    # Establish relationship with rec and country node
    wthr_cond_node.relationships.create("lc", lght_cond_node)
    print ("Created light condition node.....")

    # Create object type node
    obj_typ_node = gdb.node(name=ech_rcord_dict["SR_SIGN_CLASS"])
    obj_typ_node.labels.add("ObjectType")
    # Establish relationship with light conditions
    lght_cond_node.relationships.create("ob", obj_typ_node)
    print ("Created object type node.....\n")



