
from PyQt4.QtGui import *
from PyQt4 import QtGui
from rec_summary_ui import Ui_MainWindow
from neo4j.v1 import GraphDatabase
from interpreter.keyword_matching_inter import KeyWordMatching


# import neo4j
# print neo4j.__version__

#pyinstaller --onefile rec_summary_events.py

class RecSummaryEvents(QMainWindow, Ui_MainWindow):


    def __init__(self):
        super(QMainWindow, self).__init__()

        # Initialize the Neo4J connections
        # self.neo_obj = Neo4JConnection("bolt://localhost:7687", "neo4j", "tan_neo4j")
        # self.neo_obj.create_nodes("nodes")
        # self.neo_obj.close()
        # "bolt://10.223.244.129:7687"

        self.neo4_driver = GraphDatabase.driver("bolt://10.223.244.129:7687:7687", auth=("neo4j", "tan_neo4j"))
        self.neo_session = self.neo4_driver.session()
        # self.txn = Transaction(session=self.neo_session)

        self.setupUi()


    def setupUi(self):

        # try:
        super(RecSummaryEvents, self).setupUi(self)
        self.pushButton_fetch.clicked.connect(self.fetch_rec_labels)
        self.progressBar.setValue(0)
        self.pushButton_interpret.clicked.connect(self.interpret_qry)


    def generate_summary(self):

        # Continuous_2011.07.04_at_14.37.07.rec
        self.progressBar.setValue(0)
        self.recname = self.lineEdit_recname.text()
        print "self.recname :>> ", self.recname
        if self.recname != "":
            self.progressBar.setValue(50)
            neo_qry = '''  MATCH (CommonData)<-[cd:cd]-(RecordingName)-[c:c]->(Country)-
                [rt:rt]->(RoadType)-
                [w:w]->(WeatherCondition)-
                [lc:lc]->(LightCondition)
                WHERE RecordingName.name = '{}'
                RETURN RecordingName.name as RecName, Country.name as Country, RoadType.name as RoadType,
                 WeatherCondition.name as WeatherCondition, LightCondition.name as LightCondition, CommonData.project as Project,
                 CommonData.function as Function, CommonData.department as Department '''.format(self.recname)
            with self.neo_session.begin_transaction() as tx:
                self.an = tx.run(neo_qry)
                self.progressBar.setValue(75)
                # print "an :: ", self.an.values()[0][0]
                # self.lineEdit_recname.setText(str(self.an.values()))
                # print "self.an.data() :: ", self.an.data()
                dt_lst = self.an.data()
                print "dt_lst :: ", dt_lst
                self.textBrowser.clear()
                sumry_tmplt = self.create_summary(dt_lst)
                if dt_lst:
                    self.textBrowser.setText(str(sumry_tmplt))
                else:
                    self.textBrowser.setText("No data found...")

        self.progressBar.setValue(100)
                # MainWindow.lineEdit_recname.setText(self.an.values()[0][0])

    def create_summary(self, result_lst):

        res_dict = result_lst[0]

        res_dict = {str(k): ([str(e) for e in v] if type(v) is list else str(v))
                    for k, v in res_dict.iteritems()}
        updated_dict = {}
        for ech_key, ech_val in res_dict.iteritems():
            if type(ech_val) is list:
                updated_dict["{}_num".format(ech_key)] = len(ech_val)

        res_dict.update(updated_dict)
        print "res_dict :: ", res_dict
        SUMMARY_TEMPLATE = '''The recording {RecName} has labels for {Project} {Function} 
        for {Department} which has observations of {Country_num} Countries {Country} 
        driven in {RoadType_num} road types {RoadType} under {WeatherCondition_num} 
        weather conditions {WeatherCondition} with {LightCondition_num} 
        Light Conditions {LightCondition}.
        '''.format(**res_dict)

        return SUMMARY_TEMPLATE

    def fetch_rec_labels(self):

        self.generate_summary()

    def interpret_qry(self):

        qry_input = str(self.lineEdit_query.text())
        self.progressBar.setValue(10)
        if qry_input == '':
            self.textEdt_res.setText("Nothing to query")
        else:
            key_match_obj = KeyWordMatching(qry_input)
            self.progressBar.setValue(40)
            op = key_match_obj.interpret_the_query()
            print "op::", op
            self.textEdt_res.setText(str(op))
            self.progressBar.setValue(90)
        self.progressBar.setValue(100)

class Neo4JConnection(object):

    neo_qry = '''  MATCH (RecName)-[c:c]->(Country) RETURN RecName.Name, Country.Name '''
    NEO_TRACE = []

    def __init__(self, uri, user, password):
        self.neo4_driver = GraphDatabase.driver(uri, auth=(user, password))
        self.neo_session = self.neo4_driver.session()
        # self.txn = Transaction(session=self.neo_session)

        self.exec_qry()

        # self.create_nodes("Nodes")


    def close(self):
        self.neo4_driver.close()

    def exec_qry(self):
        with self.neo_session.begin_transaction() as tx:
            self.an = tx.run(Neo4JConnection.neo_qry)
            print "an :: ", self.an.values()[0][0]
            MainWindow.lineEdit_recname.setText(self.an.values()[0][0])


    def create_nodes(self, message):
        # with self.neo4_driver.session() as session:
        written_data = self.neo_session.write_transaction(self._create_and_return_data, message)
        # print "written_data :: ", written_data
        return written_data


    # @staticmethod
    def _create_and_return_data(self, tx, message):
        # print "tx :: ", tx
        self.result = tx.run(Neo4JConnection.neo_qry,
                        message=message)
        # print "result :: ", self.result.values(), type(self.result.values())
        # if result.single() is not None:
        # print "Neo4JConnection.NEO_TRACE :: ", Neo4JConnection.NEO_TRACE
        # vc = self.result.values()[0]

        # print "str(self.result.values()) ::>> ", vc
        # for ech_itm in self.result.values():
        #     MainWindow.textBrowser.setText(str(ech_itm))
        # MainWindow.lineEdit_recname.setText(str(self.result.values()))
        # return result.values()





if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    # MainWindow = QtGui.QMainWindow()
    MainWindow = RecSummaryEvents()
    # ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
