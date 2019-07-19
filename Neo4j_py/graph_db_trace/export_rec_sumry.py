
from neo4jrestclient.client import GraphDatabase
import os


class ExportSummary(object):

    def __init__(self, rec_names_lst):

        self.gdb = GraphDatabase("http://10.223.244.129:7474/db/data/",
                            username="neo4j", password="tan_neo4j")
        self.rec_names_lst = rec_names_lst
        if os.path.isfile('export_summary.txt'):
            os.remove('export_summary.txt')

        self.generate_summry(self.rec_names_lst)


    def generate_summry(self, rec_names_lst):
        """
        [[u'20141215_1540_{08627FB2-FDC3-414E-92B3-EBE39884DA8F}.rrec'],
        [u'20150731_0439_{7B17D7CD-A8C7-4F64-B08B-4702C55F3D32}.rrec']]
        :param rec_names_lst:
        :return:
        """

        for evry_recname in rec_names_lst:
            q = '''MATCH (CommonData)<-[cd:cd]-(RecordingName)-[c:c]->(Country)-
            [rt:rt]->(RoadType)-
            [w:w]->(WeatherCondition)-
            [lc:lc]->(LightCondition)-
            [ob:ob]->(ObjectType)
            WHERE RecordingName.name = '{}'
            RETURN RecordingName.name as RecName, Country.name as Country, RoadType.name as RoadType,
             WeatherCondition.name as WeatherCondition, LightCondition.name as LightCondition, CommonData.project as Project,
             CommonData.function as Function, CommonData.department as Department, ObjectType.name as Objects '''.format(evry_recname)
            result = self.gdb.query(q=q, data_contents=True)
            rows = result.rows
            columns = result.columns
            # print "-->", rows
            if rows is not None:
                for item in rows:
                    dt_lst = [dict(zip(columns, item))]
                sumry_tmplt = self.create_summary(dt_lst)
                print("sumry_tmplt :: ", sumry_tmplt)
                print("\n")
                self.write_smry_to_txt(evry_recname, sumry_tmplt)


    def create_summary(self, result_lst):

        res_dict = result_lst[0]

        res_dict = {str(k): ([str(e) for e in v] if type(v) is list else str(v))
                    for k, v in res_dict.items()}
        updated_dict = {}
        for ech_key, ech_val in res_dict.items():
            if type(ech_val) is list:
                updated_dict["{}_num".format(ech_key)] = len(ech_val)

        res_dict.update(updated_dict)
        # print "res_dict :: ", res_dict
        SUMMARY_TEMPLATE = '''The recording {RecName} has labels for {Project} {Function}
        for {Department} which has observations of {Country_num} Countries {Country} 
        driven in {RoadType_num} road types {RoadType} under {WeatherCondition_num}
        weather conditions {WeatherCondition} with {LightCondition_num}
        Light Conditions {LightCondition} having {Objects_num} Objects {Objects}.
        '''.format(**res_dict)

        return SUMMARY_TEMPLATE

    def write_smry_to_txt(self, evry_recname, smry_txt):

        print("write_smry_to_txt >>>>>>>>>>>>")

        with open("export_summary.txt", "a") as fhandle:
            # fhandle.write(smry_txt + "\n\n")
            fhandle.write(smry_txt + "\n\n")
            # fhandle.write("\n")

if __name__ == '__main__':

    exp_smry_obj = ExportSummary()
    # rec_names_lst = exp_smry_obj.get_recnames()
    # exp_smry_obj.generate_summry(rec_names_lst)