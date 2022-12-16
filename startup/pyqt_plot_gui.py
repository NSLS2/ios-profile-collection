from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton
import sys
import bluesky_ui_logger

class QT_Plot_GUI(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("/home/xf23id2/.ipython/profile_collection/startup/pyqt_plot_ui.ui", self)
        #uic.loadUi("pyqt_plot_ui.ui", self)


        ######### PD ENERGY SCAN SECTION #############
        def pdenergy_button_action():
            pui_scanid1 = self.pdenergy_lineEdit1.text() 
            pui_scanid2 = self.pdenergy_lineEdit2.text() 
            pui_label = self.pdenergy_lineEdit3.text() 
           
            bluesky_ui_logger.bs_ui_log("plot_PD_EnergyScan(" + pui_scanid1 + "," + pui_scanid2 + ",\"" + pui_label + "\")")
            plot_PD_EnergyScan(int(pui_scanid1), int(pui_scanid2), pui_label)
        
        self.pdenergy_pushButton.clicked.connect(pdenergy_button_action)

        ######### SAMPLE PLOT SECTION #############
        def samplemap_button_action():
            pui_scanid1 = self.sample_lineEdit1.text() 
            pui_scanid2 = self.sample_lineEdit2.text() 
            pui_label = self.sample_lineEdit3.text() 

            pui_tey = self.sample_tey_checkBox.isChecked()
            pui_pfy = self.sample_pfy_checkBox.isChecked()

            if not pui_tey and not pui_pfy:
                pui_tey = True

            if pui_tey:
                bluesky_ui_logger.bs_ui_log("plot_sample_map("+ pui_scanid1 + "," +pui_scanid2 + ",\"" + pui_label + "_TEY\",scan_type = \"TEY\")")
                plot_sample_map(int(pui_scanid1), int(pui_scanid2),pui_label + "_TEY", scan_type = "TEY")
            
            if pui_pfy :
                bluesky_ui_logger.bs_ui_log("plot_sample_map("+ pui_scanid1 + "," +pui_scanid2 + ",\"" + pui_label + "_PFY\",scan_type = \"PFY\")")
                plot_sample_map(int(pui_scanid1), int(pui_scanid2),pui_label + "_PFY", scan_type = "PFY")
        
        self.sample_pushButton.clicked.connect(samplemap_button_action)

        ######### RAW XAS SECTION #############
        def plotrawxas_button_action():
            pui_scanid1 = self.rawxas_scanid1_lineEdit.text() 
            pui_scanid2 = self.rawxas_scanid2_lineEdit.text() 
            pui_label = self.rawxas_label_lineEdit.text() 

            pui_tey = self.rawxas_tey_checkBox.isChecked()
            pui_pfy = self.rawxas_pfy_checkBox.isChecked()
            pui_tfy = self.rawxas_tfy_checkBox.isChecked()
            pui_ipfy = self.rawxas_ipfy_checkBox.isChecked()
            pui_pey = self.rawxas_pey_checkBox.isChecked()
            if not pui_tey and not pui_pfy and not pui_tfy and not pui_ipfy and not pui_pey :
                pui_tey = True

            pui_normto1 = self.rawxas_normto1_checkBox.isChecked()
            normto1_str = "N"
            if pui_normto1 :
                normto1_str = "Y"

            if pui_tey :
                bluesky_ui_logger.bs_ui_log("plot_raw_xas(" + pui_scanid1 + "," + pui_scanid2 + ",\"" + pui_label + "_tey\",scan_type='TEY',normto1= \"" + normto1_str + "\")")
                plot_raw_xas(int(pui_scanid1),int(pui_scanid2),pui_label + "_tey", scan_type='TEY',normto1= normto1_str)
            if pui_pfy :
                bluesky_ui_logger.bs_ui_log("plot_raw_xas(" + pui_scanid1 + "," + pui_scanid2 + ",\"" + pui_label + "_pfy\",scan_type='PFY',normto1= \"" + normto1_str + "\")")
                plot_raw_xas(int(pui_scanid1),int(pui_scanid2),pui_label + "_pfy", scan_type='PFY',normto1= normto1_str)
            if pui_tfy :
                bluesky_ui_logger.bs_ui_log("plot_raw_xas(" + pui_scanid1 + "," + pui_scanid2 + ",\"" + pui_label + "_tfy\",scan_type='TFY',normto1= \"" + normto1_str + "\")")
                plot_raw_xas(int(pui_scanid1),int(pui_scanid2),pui_label + "_tfy", scan_type='TFY',normto1= normto1_str)
            if pui_ipfy :
                bluesky_ui_logger.bs_ui_log("plot_raw_xas(" + pui_scanid1 + "," + pui_scanid2 + ",\"" + pui_label + "_ipfy\",scan_type='IPFY',normto1= \"" + normto1_str + "\")")
                plot_raw_xas(int(pui_scanid1),int(pui_scanid2),pui_label + "_ipfy", scan_type='IPFY',normto1= normto1_str)
            if pui_pey :
                bluesky_ui_logger.bs_ui_log("plot_raw_xas(" + pui_scanid1 + "," + pui_scanid2 + ",\"" + pui_label + "_pey\",scan_type='PEY',normto1= \"" + normto1_str + "\")")
                plot_raw_xas(int(pui_scanid1),int(pui_scanid2),pui_label + "_pey", scan_type='PEY',normto1= normto1_str)

        self.rawxas_pushButton.clicked.connect(plotrawxas_button_action)

        ######### AVERAGE RAW XAS SECTION #############
        def plotavgrawxas_button_action():
            pui_scanid1 = self.avgrawxas_scanid1_lineEdit.text() 
            pui_scanid2 = self.avgrawxas_scanid2_lineEdit.text() 
            pui_label = self.avgrawxas_label_lineEdit.text() 

            pui_tey = self.avgrawxas_tey_checkBox.isChecked()
            pui_pfy = self.avgrawxas_pfy_checkBox.isChecked()
            pui_tfy = self.avgrawxas_tfy_checkBox.isChecked()
            pui_ipfy = self.avgrawxas_ipfy_checkBox.isChecked()
            pui_pey = self.avgrawxas_pey_checkBox.isChecked()
            if not pui_tey and not pui_pfy and not pui_tfy and not pui_ipfy and not pui_pey :
                pui_tey = True

            pui_normto1 = self.avgrawxas_normto1_checkBox.isChecked()
            normto1_str = "N"
            if pui_normto1 :
                normto1_str = "Y"

            if pui_tey :
                bluesky_ui_logger.bs_ui_log("plot_avg_raw_xas(" + pui_scanid1 + "," + pui_scanid2 + ",\"" + pui_label + "_tey\",scan_type='TEY',normto1= \"" + normto1_str + "\")")
                plot_avg_raw_xas(int(pui_scanid1),int(pui_scanid2),pui_label + "_tey", scan_type='TEY',normto1= normto1_str)
            if pui_pfy :
                bluesky_ui_logger.bs_ui_log("plot_avg_raw_xas(" + pui_scanid1 + "," + pui_scanid2 + ",\"" + pui_label + "_pfy\",scan_type='PFY',normto1= \"" + normto1_str + "\")")
                plot_avg_raw_xas(int(pui_scanid1),int(pui_scanid2),pui_label + "_pfy", scan_type='PFY',normto1= normto1_str)
            if pui_tfy :
                bluesky_ui_logger.bs_ui_log("plot_avg_raw_xas(" + pui_scanid1 + "," + pui_scanid2 + ",\"" + pui_label + "_tfy\",scan_type='TFY',normto1= \"" + normto1_str + "\")")
                plot_avg_raw_xas(int(pui_scanid1),int(pui_scanid2),pui_label + "_tfy", scan_type='TFY',normto1= normto1_str)
            if pui_ipfy :
                bluesky_ui_logger.bs_ui_log("plot_avg_raw_xas(" + pui_scanid1 + "," + pui_scanid2 + ",\"" + pui_label + "_ipfy\",scan_type='IPFY',normto1= \"" + normto1_str + "\")")
                plot_avg_raw_xas(int(pui_scanid1),int(pui_scanid2),pui_label + "_ipfy", scan_type='IPFY',normto1= normto1_str)
            if pui_pey :
                bluesky_ui_logger.bs_ui_log("plot_avg_raw_xas(" + pui_scanid1 + "," + pui_scanid2 + ",\"" + pui_label + "_pey\",scan_type='PEY',normto1= \"" + normto1_str + "\")")
                plot_avg_raw_xas(int(pui_scanid1),int(pui_scanid2),pui_label + "_pey", scan_type='PEY',normto1= normto1_str)

        self.avgrawxas_pushButton.clicked.connect(plotavgrawxas_button_action)

        ######### NORM XAS SECTION #############
        def plotnormxas_button_action():
            pui_scanid1 = self.normxas_scanid1_lineEdit.text() 
            pui_scanid2 = self.normxas_scanid2_lineEdit.text() 
            pui_label = self.normxas_label_lineEdit.text() 

            pui_tey = self.normxas_tey_checkBox.isChecked()
            pui_pfy = self.normxas_pfy_checkBox.isChecked()
            pui_tfy = self.normxas_tfy_checkBox.isChecked()
            pui_ipfy = self.normxas_ipfy_checkBox.isChecked()
            pui_pey = self.normxas_pey_checkBox.isChecked()
            if not pui_tey and not pui_pfy and not pui_tfy and not pui_ipfy and not pui_pey :
                pui_tey = True

            pui_normto1 = self.normxas_normto1_checkBox.isChecked()
            normto1_str = "N"
            if pui_normto1 :
                normto1_str = "Y"

            if pui_tey :
                bluesky_ui_logger.bs_ui_log("plot_norm_xas(" + pui_scanid1 + "," + pui_scanid2 + ",\"" + pui_label + "_tey\",scan_type='TEY',normto1= \"" + normto1_str + "\")")
                plot_norm_xas(int(pui_scanid1),int(pui_scanid2),pui_label + "_tey", scan_type='TEY',normto1= normto1_str)
            if pui_pfy :
                bluesky_ui_logger.bs_ui_log("plot_norm_xas(" + pui_scanid1 + "," + pui_scanid2 + ",\"" + pui_label + "_pfy\",scan_type='PFY',normto1= \"" + normto1_str + "\")")
                plot_norm_xas(int(pui_scanid1),int(pui_scanid2),pui_label + "_pfy", scan_type='PFY',normto1= normto1_str)
            if pui_tfy :
                bluesky_ui_logger.bs_ui_log("plot_norm_xas(" + pui_scanid1 + "," + pui_scanid2 + ",\"" + pui_label + "_tfy\",scan_type='TFY',normto1= \"" + normto1_str + "\")")
                plot_norm_xas(int(pui_scanid1),int(pui_scanid2),pui_label + "_tfy", scan_type='TFY',normto1= normto1_str)
            if pui_ipfy :
                bluesky_ui_logger.bs_ui_log("plot_norm_xas(" + pui_scanid1 + "," + pui_scanid2 + ",\"" + pui_label + "_ipfy\",scan_type='IPFY',normto1= \"" + normto1_str + "\")")
                plot_norm_xas(int(pui_scanid1),int(pui_scanid2),pui_label + "_ipfy", scan_type='IPFY',normto1= normto1_str)
            if pui_pey :
                bluesky_ui_logger.bs_ui_log("plot_norm_xas(" + pui_scanid1 + "," + pui_scanid2 + ",\"" + pui_label + "_pey\",scan_type='PEY',normto1= \"" + normto1_str + "\")")
                plot_norm_xas(int(pui_scanid1),int(pui_scanid2),pui_label + "_pey", scan_type='PEY',normto1= normto1_str)

        self.normxas_pushButton.clicked.connect(plotnormxas_button_action)

        ######### AVERAGE NORM XAS SECTION #############
        def plotavgnormxas_button_action():
            pui_scanid1 = self.avgnormxas_scanid1_lineEdit.text() 
            pui_scanid2 = self.avgnormxas_scanid2_lineEdit.text() 
            pui_label = self.avgnormxas_label_lineEdit.text() 

            pui_tey = self.avgnormxas_tey_checkBox.isChecked()
            pui_pfy = self.avgnormxas_pfy_checkBox.isChecked()
            pui_tfy = self.avgnormxas_tfy_checkBox.isChecked()
            pui_ipfy = self.avgnormxas_ipfy_checkBox.isChecked()
            pui_pey = self.avgnormxas_pey_checkBox.isChecked()
            if not pui_tey and not pui_pfy and not pui_tfy and not pui_ipfy and not pui_pey :
                pui_tey = True

            pui_normto1 = self.avgnormxas_normto1_checkBox.isChecked()
            normto1_str = "N"
            if pui_normto1 :
                normto1_str = "Y"

            if pui_tey :
                bluesky_ui_logger.bs_ui_log("plot_avg_norm_xas(" + pui_scanid1 + "," + pui_scanid2 + ",\"" + pui_label + "_tey\",scan_type='TEY',normto1= \"" + normto1_str + "\")")
                plot_avg_norm_xas(int(pui_scanid1),int(pui_scanid2),pui_label + "_tey", scan_type='TEY',normto1= normto1_str)
            if pui_pfy :
                bluesky_ui_logger.bs_ui_log("plot_avg_norm_xas(" + pui_scanid1 + "," + pui_scanid2 + ",\"" + pui_label + "_pfy\",scan_type='PFY',normto1= \"" + normto1_str + "\")")
                plot_avg_norm_xas(int(pui_scanid1),int(pui_scanid2),pui_label + "_pfy", scan_type='PFY',normto1= normto1_str)
            if pui_tfy :
                bluesky_ui_logger.bs_ui_log("plot_avg_norm_xas(" + pui_scanid1 + "," + pui_scanid2 + ",\"" + pui_label + "_tfy\",scan_type='TFY',normto1= \"" + normto1_str + "\")")
                plot_avg_norm_xas(int(pui_scanid1),int(pui_scanid2),pui_label + "_tfy", scan_type='TFY',normto1= normto1_str)
            if pui_ipfy :
                bluesky_ui_logger.bs_ui_log("plot_avg_norm_xas(" + pui_scanid1 + "," + pui_scanid2 + ",\"" + pui_label + "_ipfy\",scan_type='IPFY',normto1= \"" + normto1_str + "\")")
                plot_avg_norm_xas(int(pui_scanid1),int(pui_scanid2),pui_label + "_ipfy", scan_type='IPFY',normto1= normto1_str)
            if pui_pey :
                bluesky_ui_logger.bs_ui_log("plot_avg_norm_xas(" + pui_scanid1 + "," + pui_scanid2 + ",\"" + pui_label + "_pey\",scan_type='PEY',normto1= \"" + normto1_str + "\")")
                plot_avg_norm_xas(int(pui_scanid1),int(pui_scanid2),pui_label + "_pey", scan_type='PEY',normto1= normto1_str)

        self.avgnormxas_pushButton.clicked.connect(plotavgnormxas_button_action)

        ######### NORM ASYNC SECTION #############
        def plotnormasyncxas_button_action():
            pui_scanid1 = self.normasyncxas_scanid1_lineEdit.text() 
            pui_scanid2 = self.normasyncxas_scanid2_lineEdit.text() 
            pui_label = self.normasyncxas_label_lineEdit.text() 
            pui_normid1 = self.normasyncxas_normid1_lineEdit.text() 

            pui_tey = self.normasyncxas_tey_checkBox.isChecked()
            pui_pfy = self.normasyncxas_pfy_checkBox.isChecked()
            pui_tfy = self.normasyncxas_tfy_checkBox.isChecked()
            pui_ipfy = self.normasyncxas_ipfy_checkBox.isChecked()
            pui_trans = self.normasyncxas_trans_checkBox.isChecked()
            pui_pey2pd = self.normasyncxas_pey2pd_checkBox.isChecked()
            pui_pey2pey = self.normasyncxas_pey2pey_checkBox.isChecked()
            if not pui_tey and not pui_pfy and not pui_tfy and not pui_ipfy and not pui_trans and not pui_pey2pd and not pui_pey2pey :
                pui_tey = True

            pui_normto1 = self.normasyncxas_normto1_checkBox.isChecked()
            normto1_str = "N"
            if pui_normto1 :
                normto1_str = "Y"

            if pui_tey :
                bluesky_ui_logger.bs_ui_log("plot_norm_async_xas(" + pui_scanid1 + "," + pui_scanid2 + "," + pui_normid1 +",\"" + pui_label + "_tey\",scan_type='TEY',normto1= \"" + normto1_str + "\")")
                plot_norm_async_xas(int(pui_scanid1),int(pui_scanid2),int(pui_normid1),pui_label + "_tey", scan_type='TEY',normto1= normto1_str)
            if pui_pfy :
                bluesky_ui_logger.bs_ui_log("plot_norm_async_xas(" + pui_scanid1 + "," + pui_scanid2 + "," + pui_normid1 +",\"" + pui_label + "_pfy\",scan_type='PFY',normto1= \"" + normto1_str + "\")")
                plot_norm_async_xas(int(pui_scanid1),int(pui_scanid2),int(pui_normid1),pui_label + "_pfy", scan_type='PFY',normto1= normto1_str)
            if pui_tfy :
                bluesky_ui_logger.bs_ui_log("plot_norm_async_xas(" + pui_scanid1 + "," + pui_scanid2 + "," + pui_normid1 +",\"" + pui_label + "_tfy\",scan_type='TFY',normto1= \"" + normto1_str + "\")")
                plot_norm_async_xas(int(pui_scanid1),int(pui_scanid2),int(pui_normid1),pui_label + "_tfy", scan_type='TFY',normto1= normto1_str)
            if pui_ipfy :
                bluesky_ui_logger.bs_ui_log("plot_norm_async_xas(" + pui_scanid1 + "," + pui_scanid2 + "," + pui_normid1 +",\"" + pui_label + "_ipfy\",scan_type='IPFY',normto1= \"" + normto1_str + "\")")
                plot_norm_async_xas(int(pui_scanid1),int(pui_scanid2),int(pui_normid1),pui_label + "_ipfy", scan_type='IPFY',normto1= normto1_str)
            if pui_trans :
                bluesky_ui_logger.bs_ui_log("plot_norm_async_xas(" + pui_scanid1 + "," + pui_scanid2 + "," + pui_normid1 +",\"" + pui_label + "_trans\",scan_type='TRANS',normto1= \"" + normto1_str + "\")")
                plot_norm_async_xas(int(pui_scanid1),int(pui_scanid2),int(pui_normid1),pui_label + "_trans", scan_type='TRANS',normto1= normto1_str)
            if pui_pey2pd :
                bluesky_ui_logger.bs_ui_log("plot_norm_async_xas(" + pui_scanid1 + "," + pui_scanid2 + "," + pui_normid1 +",\"" + pui_label + "_pey2pd\",scan_type='PEY2PD',normto1= \"" + normto1_str + "\")")
                plot_norm_async_xas(int(pui_scanid1),int(pui_scanid2),int(pui_normid1),pui_label + "_pey2pd", scan_type='PEY2PD',normto1= normto1_str)
            if pui_pey2pey :
                bluesky_ui_logger.bs_ui_log("plot_norm_async_xas(" + pui_scanid1 + "," + pui_scanid2 + "," + pui_normid1 +",\"" + pui_label + "_pey2pey\",scan_type='PEY2PEY',normto1= \"" + normto1_str + "\")")
                plot_norm_async_xas(int(pui_scanid1),int(pui_scanid2),int(pui_normid1),pui_label + "_pey2pey", scan_type='PEY2PEY',normto1= normto1_str)

        self.normasyncxas_pushButton.clicked.connect(plotnormasyncxas_button_action)

        ######### AVERAGE NORM ASYNC SECTION #############
        def plotavgasyncxas_button_action():
            pui_scanid1 = self.avgasyncxas_scanid1_lineEdit.text() 
            pui_scanid2 = self.avgasyncxas_scanid2_lineEdit.text() 
            pui_label = self.avgasyncxas_label_lineEdit.text() 
            pui_normid1 = self.avgasyncxas_normid1_lineEdit.text() 
            pui_normid2 = self.avgasyncxas_normid2_lineEdit.text() 

            pui_tey = self.avgasyncxas_tey_checkBox.isChecked()
            pui_pfy = self.avgasyncxas_pfy_checkBox.isChecked()
            pui_tfy = self.avgasyncxas_tfy_checkBox.isChecked()
            pui_ipfy = self.avgasyncxas_ipfy_checkBox.isChecked()
            pui_pey = self.avgasyncxas_pey_checkBox.isChecked()
            if not pui_tey and not pui_pfy and not pui_tfy and not pui_ipfy and not pui_pey :
                pui_tey = True

            pui_normto1 = self.avgasyncxas_normto1_checkBox.isChecked()
            normto1_str = "N"
            if pui_normto1 :
                normto1_str = "Y"

            if pui_tey :
                bluesky_ui_logger.bs_ui_log("plot_avg_async_xas(" + pui_scanid1 + "," + pui_scanid2 + "," + pui_normid1 +"," + pui_normid2 +",\"" + pui_label + "_tey\",scan_type='TEY',normto1= \"" + normto1_str + "\")")
                plot_avg_async_xas(int(pui_scanid1),int(pui_scanid2),int(pui_normid1),int(pui_normid2),pui_label + "_tey", scan_type='TEY',normto1= normto1_str)
            if pui_pfy :
                bluesky_ui_logger.bs_ui_log("plot_avg_async_xas(" + pui_scanid1 + "," + pui_scanid2 + "," + pui_normid1 +"," + pui_normid2 +",\"" + pui_label + "_pfy\",scan_type='PFY',normto1= \"" + normto1_str + "\")")
                plot_avg_async_xas(int(pui_scanid1),int(pui_scanid2),int(pui_normid1),int(pui_normid2),pui_label + "_pfy", scan_type='PFY',normto1= normto1_str)
            if pui_tfy :
                bluesky_ui_logger.bs_ui_log("plot_avg_async_xas(" + pui_scanid1 + "," + pui_scanid2 + "," + pui_normid1 +"," + pui_normid2 +",\"" + pui_label + "_tfy\",scan_type='TFY',normto1= \"" + normto1_str + "\")")
                plot_avg_async_xas(int(pui_scanid1),int(pui_scanid2),int(pui_normid1),int(pui_normid2),pui_label + "_tfy", scan_type='TFY',normto1= normto1_str)
            if pui_ipfy :
                bluesky_ui_logger.bs_ui_log("plot_avg_async_xas(" + pui_scanid1 + "," + pui_scanid2 + "," + pui_normid1 +"," + pui_normid2 +",\"" + pui_label + "_ipfy\",scan_type='IPFY',normto1= \"" + normto1_str + "\")")
                plot_avg_async_xas(int(pui_scanid1),int(pui_scanid2),int(pui_normid1),int(pui_normid2),pui_label + "_ipfy", scan_type='IPFY',normto1= normto1_str)
            if pui_pey :
                bluesky_ui_logger.bs_ui_log("plot_avg_async_xas(" + pui_scanid1 + "," + pui_scanid2 + "," + pui_normid1 +"," + pui_normid2 +",\"" + pui_label + "_pey\",scan_type='PEY',normto1= \"" + normto1_str + "\")")
                plot_avg_async_xas(int(pui_scanid1),int(pui_scanid2),int(pui_normid1),int(pui_normid2),pui_label + "_pey", scan_type='PEY',normto1= normto1_str)


        self.avgasyncxas_pushButton.clicked.connect(plotavgasyncxas_button_action)

        ####### CUSTOM PLOT SECTION ######
        def custom_x_combobox_action():
            x_selection = self.custom_x_comboBox.currentText()
            x_lineEdit = self.custom_x_lineEdit
            if x_selection == "Custom...":
                x_lineEdit.setEnabled(True)
            else:
                x_lineEdit.setEnabled(False)
        
        self.custom_x_comboBox.activated.connect(custom_x_combobox_action)

        def custom_y_combobox_action():
            y_selection = self.custom_y_comboBox.currentText()
            y_lineEdit = self.custom_y_lineEdit
            if y_selection == "Custom...":
                y_lineEdit.setEnabled(True)
            else:
                y_lineEdit.setEnabled(False)
        
        self.custom_y_comboBox.activated.connect(custom_y_combobox_action)

        yval_dict = {"Photodiode": "sclr_ch2", "Au Mesh" : "sclr_ch3", "Sample TEY" : "sclr_ch4",
        "Sample PFY": "vortex_mca_rois_roi4_count", "Sample PEY": "specs_count"}

        xval_dict = {"Time" : "time", "Photon Energy" : "pgm_energy_readback", "EPU1 Gap" : "epu1.gap", "Au Mesh" : "au_mesh",
        "IOXAS Sample" : "ioxas_x", "Diagnostic" : "diag3_y", "Exit Slit" : "slt2", "Beam Position" : "m1b1_setpoint"}

        def customplot_button_action():
            pui_scanid1 = self.custom_scanid1_lineEdit.text()
            pui_scanid2 = self.custom_scanid2_lineEdit.text()
            pui_label = self.custom_label_lineEdit.text()
            pui_yval = ""
            pui_xval = ""

            y_selection = self.custom_y_comboBox.currentText()
            x_selection = self.custom_x_comboBox.currentText()

            if y_selection == "Custom...":
                pui_yval = self.custom_y_lineEdit.text()
            else :
                pui_yval = yval_dict[y_selection]

            if x_selection == "Custom...":
                pui_xval = self.custom_x_lineEdit.text()
            else :
                pui_xval = xval_dict[x_selection]
            
            bluesky_ui_logger.bs_ui_log("custom_plot(" + pui_scanid1 +"," + pui_scanid2 + ",\"" + pui_label + "\",x_axis=\"" + pui_xval + "\", y_axis=\"" + pui_yval + "\")")
            custom_plot(int(pui_scanid1), int(pui_scanid2), pui_label, x_axis=pui_xval, y_axis=pui_yval)

        self.custom_doplot_pushButton.clicked.connect(customplot_button_action)


def open_plot_gui():
    app = QApplication([])
    testWindow = QT_Plot_GUI()
    testWindow.show()
    sys.exit(app.exec())

#open_plot_gui()
