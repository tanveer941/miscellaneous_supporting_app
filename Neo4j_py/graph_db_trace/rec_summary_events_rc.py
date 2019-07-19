
from PyQt4.QtGui import *
from PyQt4 import QtGui, QtCore
from rec_summary_ui import Ui_MainWindow
from neo4jrestclient.client import GraphDatabase
from flexible_search import TFIDExtractor
from rigid_search import KeyWordMatching
from export_rec_sumry import ExportSummary

# import neo4j
# print neo4j.__version__

IP_ADDRESS = '10.205.247.160'
# IP_ADDRESS = '10.223.242.11'


LDSS_KEYWORDS = ['Luxemburg', 'MFC400', 'SR', 'DEV', 'Luxemburg', 'Rain', 'Motorway',
                 'Day', 'EVA', 'USA', 'Country_Road', 'Night', 'Highway', 'Great_Britain', 'Dusk', ]

OBJ_KEYWORDS = ['Danger_Animal_Crossing_from_Right', 'Danger_Bend_Left', 'Danger_Exclamation_Mark',
                 'Danger_Exclamation_Mark_Yellow', 'Danger_Road_Works_Right', 'Danger_Road_Works_Right_Yellow',
                 'Danger_Small_Road_From_Left_45_Degree', 'Danger_Small_Road_From_Right_45_Degree',
                 'Danger_Small_Road_From_Right_45_Degree_Yellow', 'Danger_Splippery_Road',
                 'Danger_Traffic_Lights', 'Danger_Two_Bump', 'Danger_Two_Way_Traffic_Yellow',
                 'Dir_Down_Left', 'Dir_Down_Left_Right', 'Dir_Down_Right', 'Dir_Left', 'Dir_Right',
                 'Dir_Right_Ahead', 'Dir_Roundabout', 'Dir_Straight_Ahead', 'Do_Not_Enter', 'Duty_Station',
                 'General_End_Slash_80Deg', 'Give_Way', 'Motor_Way', 'Motor_Way_End_Green', 'No_Passing',
                 'No_Passing_Truck', 'Not_Readable', 'Other_Round_Sign', 'Other_Supplementary_Sign',
                 'Pedestrian_Crossing', 'Prohib_All', 'Prohib_Moped', 'Prohib_Motorbike', 'Prohib_Parking',
                 'Prohib_Pedestrian', 'Prohib_Stopping', 'Prohib_Truck', 'Speed_Limit_030', 'Speed_Limit_040',
                 'Speed_Limit_050', 'Speed_Limit_060', 'Speed_Limit_060_Inv', 'Speed_Limit_065', 'Speed_Limit_070',
                 'Speed_Limit_080', 'Speed_Limit_090', 'Speed_Limit_100', 'Speed_Limit_110', 'Speed_Limit_End_060_Slash_60Deg',
                 'Speed_Limit_End_110_Slash_80Deg', 'Stop', 'Suppl_Expalantion_Pic_SnowPlow',
                 'Suppl_Explanation_Pic_ArrowDownShort', 'Suppl_Explanation_Pic_ArrowUpShort', 'Suppl_Explanation_Pic_ArrowUpShort_Pic_ArrowDownShort',
                 'Suppl_Explanation_Pic_Truck_Pic_CarSide_Pic_TiltedLine', 'Suppl_Explanation_TexRegExp_1500m', 'Suppl_Explanation_TexRegExp_150m', 'Suppl_Explanation_TexRegExp_500m', 'Suppl_Explanation_TexRegExp_700m', 'Suppl_Restriction_Pic_CarSide', 'Suppl_Restriction_Pic_CloudBlackRain', 'Suppl_Restriction_Pic_SnowFlake_Pic_SnowFlake_Inv', 'Suppl_Restriction_Pic_TruckXXt', 'Suppl_Restriction_TexRegExp_0-24', 'Suppl_Restriction_TexRegExp_12t', 'Suppl_Restriction_TexRegExp_7,5t', 'Suppl_Restriction_Tex_ingalleria']


class RecSummaryEvents(QMainWindow, Ui_MainWindow):


    def __init__(self):
        super(QMainWindow, self).__init__()

        # Initialize the Neo4J connections
        # self.neo_obj = Neo4JConnection("bolt://localhost:7687", "neo4j", "tan_neo4j")
        # self.neo_obj.create_nodes("nodes")
        # self.neo_obj.close()
        # "bolt://10.223.244.129:7687"

        # self.neo4_driver = GraphDatabase.driver("bolt://10.223.244.129:7687:7687", auth=("neo4j", "tan_neo4j"))
        # self.neo_session = self.neo4_driver.session()
        self.neo_session = GraphDatabase("http://{}:7474/db/data/".format(IP_ADDRESS),
                            username="neo4j", password="tan_neo4j")
        # self.txn = Transaction(session=self.neo_session)

        self.setupUi()

    def setupUi(self):

        # try:
        super(RecSummaryEvents, self).setupUi(self)
        self.pushButton_fetch.clicked.connect(self.fetch_rec_labels)
        self.progressBar.setValue(0)
        self.pushButton_interpret.clicked.connect(self.interpret_qry)
        self.pushButton_export.clicked.connect(self.export_summary)
        self.pushButton_export.setDisabled(True)
        self.rec_lst_wdgt.itemClicked.connect(self.on_rec_click)
        self.rec_lst_wdgt.itemDoubleClicked.connect(self.show_summary)
        # self.lne_edit_loctn.setText(r"D:/")
        # self.tool_btn_loctn.clicked.connect(self.open_directory)
        bgColor = '#262626'
        style = """QLineEdit{{ color: #EBEBEB; border: 0px solid black; background-color: {0}; color: #EBEBEB; font-size: 30px}} 
        QLineEdit:hover{{ border: 1px solid #ffa02f;}}""".format(
            bgColor)

        self.lineEdit_query.setStyleSheet(style)
        # Fill LDSS elements in the combo box
        for index, element in enumerate(LDSS_KEYWORDS):
            self.chkbl_ComboBox.addItem(LDSS_KEYWORDS[index])
            item = self.chkbl_ComboBox.model().item(index, 0)
            item.setCheckState(QtCore.Qt.Unchecked)
        self.chkbl_ComboBox.currentIndexChanged.connect(self.combo_txt)

        # Fill the LDROI in the checkable combo
        for index, element in enumerate(OBJ_KEYWORDS):
            self.chkbl_objtype_ComboBox.addItem(OBJ_KEYWORDS[index])
            item = self.chkbl_objtype_ComboBox.model().item(index, 0)
            item.setCheckState(QtCore.Qt.Unchecked)
        self.chkbl_objtype_ComboBox.currentIndexChanged.connect(self.combo_txt_objtype)

    def show_summary(self, item):

        self.lineEdit_recname.setText(item.text())
        self.generate_summary()

    def combo_txt_objtype(self, event):
        sel_itm = self.chkbl_objtype_ComboBox.itemText(event)
        # print("sel_itm :: ", sel_itm)
        self.lineEdit_query.setText(str(self.lineEdit_query.text()) + sel_itm + " ")

    def combo_txt(self, event):
        sel_itm = self.chkbl_ComboBox.itemText(event)
        # print("sel_itm :: ", sel_itm)
        self.lineEdit_query.setText(str(self.lineEdit_query.text()) + sel_itm + " ")

    def open_directory(self):

        folder_loc = QFileDialog.getExistingDirectory(None, "Please select a Directory", directory="D:/")
        print("folder_loc :: ", folder_loc)
        self.lne_edit_loctn.setText(str(folder_loc))

    def on_rec_click(self, item):

        # print "item :: ", item.text()
        self.lineEdit_recname.setText(item.text())

    def export_summary(self):

        rec_names_lst = []
        for index in range(self.rec_lst_wdgt.count()):
            rec_names_lst.append(self.rec_lst_wdgt.item(index).text())
        print("rec_names_lst :: ", rec_names_lst)

        exp_smry_obj = ExportSummary(rec_names_lst)
        self.progressBar.setValue(20)
        # rec_names_lst = exp_smry_obj.get_recnames()
        self.progressBar.setValue(60)
        # exp_smry_obj.generate_summry(rec_names_lst)
        self.progressBar.setValue(100)
        return QMessageBox.information(self, "Information",
                                       "Exported summaries for the recordings listed",
                                       QtGui.QMessageBox.Ok)

    def generate_summary(self):

        # Continuous_2011.07.04_at_14.37.07.rec
        self.progressBar.setValue(0)
        self.recname = self.lineEdit_recname.text()
        print("self.recname :>> ", self.recname)
        if self.recname != "":
            self.progressBar.setValue(50)
            neo_qry = '''  MATCH (CommonData)<-[cd:cd]-(RecordingName)-[c:c]->(Country)-
                [rt:rt]->(RoadType)-
                [w:w]->(WeatherCondition)-
                [lc:lc]->(LightCondition)-
                [ob:ob]->(ObjectType)
                WHERE RecordingName.name = '{}'
                RETURN RecordingName.name as RecName, Country.name as Country, RoadType.name as RoadType,
                 WeatherCondition.name as WeatherCondition, LightCondition.name as LightCondition, CommonData.project as Project,
                 CommonData.function as Function, CommonData.department as Department, ObjectType.name as Objects '''.format(self.recname)
            # with self.neo_session.begin_transaction() as tx:
            result = self.neo_session.query(q=neo_qry, data_contents=True)
            rows = result.rows
            columns = result.columns
            print("rows::", rows)
            print("columns::", columns)
            self.progressBar.setValue(75)
            # print "an :: ", self.an.values()[0][0]
            # self.lineEdit_recname.setText(str(self.an.values()))
            # print "self.an.data() :: ", self.an.data()
            if rows is not None:
                for item in rows:
                    dt_lst = [dict(zip(columns, item))]
                print("dt_lst :: ", dt_lst)
                self.summ_txt_edt.clear()
                sumry_tmplt = self.create_summary(dt_lst)
                if dt_lst:
                    self.summ_txt_edt.setText(str(sumry_tmplt))
                else:
                    self.summ_txt_edt.setText("No data found...")
            else:
                self.summ_txt_edt.setText("No data found...")
                # self.rec_lst_wdgt.insertItem(0, "No data found...")

        self.progressBar.setValue(100)
                # MainWindow.lineEdit_recname.setText(self.an.values()[0][0])

    def create_summary(self, result_lst):

        res_dict = result_lst[0]

        res_dict = {str(k): ([str(e) for e in v] if type(v) is list else str(v))
                    for k, v in res_dict.items()}
        updated_dict = {}
        for ech_key, ech_val in res_dict.items():
            if type(ech_val) is list:
                updated_dict["{}_num".format(ech_key)] = len(ech_val)

        res_dict.update(updated_dict)
        print("res_dict :: ", res_dict)
        SUMMARY_TEMPLATE = '''The recording <b>{RecName}</b> has labels for <b>{Project} {Function}</b> 
        for <b>{Department}</b> which has observations of <b>{Country_num}</b> Countries <b>{Country}</b> 
        driven in <b>{RoadType_num}</b> road types <b>{RoadType}</b> under <b>{WeatherCondition_num}</b> 
        weather conditions <b>{WeatherCondition}</b> with <b>{LightCondition_num}</b> 
        Light Conditions <b>{LightCondition}</b> having <b>{Objects_num}</b> Objects <b>{Objects}</b>.
        '''.format(**res_dict)

        return SUMMARY_TEMPLATE

    def fetch_rec_labels(self):

        self.generate_summary()

    def interpret_qry(self):

        self.rec_lst_wdgt.clear()
        qry_input = str(self.lineEdit_query.text())
        self.progressBar.setValue(10)
        if qry_input == '':
            self.textEdt_res.setText("Nothing to query")
        else:

            # Key word matching
            # key_match_obj = KeyWordMatching(qry_input)
            # self.progressBar.setValue(40)
            # op = key_match_obj.interpret_the_query()

            # TFID Extractor
            print(">>>> ", self.rgd_chk_box.checkState())
            if self.rgd_chk_box.checkState() == 0:
                tfid_obj = TFIDExtractor(query=qry_input)
                print("tfid_obj :: ", tfid_obj)
                rec_lst = tfid_obj.get_rec_details()
                print("rec_lst ::", rec_lst)
            else:
                # Rigid search
                kwd_match_obj = KeyWordMatching(qry=qry_input)
                rec_lst = list(kwd_match_obj.match_all())
                # rec_lst = []

            if rec_lst:

                self.rec_lst_wdgt.insertItems(0, rec_lst)
                self.pushButton_export.setDisabled(False)
            else:
                self.rec_lst_wdgt.insertItem(0, "No recording..")
                self.pushButton_export.setDisabled(True)
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
            print("an :: ", self.an.values()[0][0])
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
