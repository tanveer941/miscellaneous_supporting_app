

from neo4jrestclient.query import Q
from neo4jrestclient.client import GraphDatabase
from neo4jrestclient import client

gdb = GraphDatabase("http://10.223.244.129:7474/db/data/", username="neo4j", password="tan_neo4j")
#
recname= '''Continuous_2011.02.11_at_11.52.06.rec'''

q='''  MATCH (CommonData)<-[cd:cd]-(RecordingName)-[c:c]->(Country)-
                [rt:rt]->(RoadType)-
                [w:w]->(WeatherCondition)-
                [lc:lc]->(LightCondition)
                WHERE RecordingName.name = '{}'
                RETURN RecordingName.name as RecName, Country.name as Country, RoadType.name as RoadType,
                 WeatherCondition.name as WeatherCondition, LightCondition.name as LightCondition, CommonData.project as Project,
                 CommonData.function as Function, CommonData.department as Department '''.format(recname)

q =''' MATCH (RecordingName:RecordingName)
RETURN RecordingName.name '''
#
#
# q=''' MATCH (RecordingName)-[c:c]->(Country)
# WHERE RecordingName.name = 'Continuous_2011.02.11_at_11.52.06.rec'
# RETURN RecordingName.name as RecName,Country.name as Country'''

#
result = gdb.query(q = q, data_contents=True)

print "result :: ", dir(result)
print "rows::", result.rows
# print "columns::", result.graph





# from py2neo import Graph
# graph = Graph("http://10.223.244.129:7474/db/data/", username="neo4j", password="tan_neo4j")
# x = graph.run(q)
#
# print dir(x)
#
# print x.data()
# for d in x:
#     print(d)
