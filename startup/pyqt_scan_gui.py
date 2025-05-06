from PyQt5 import uic, QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QMessageBox
from PyQt5.Qt import Qt
#from PyQt5.Qt import Qt
import sys
import bluesky_ui_logger

searching_flag = 0

class QT_Scan_GUI(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("/home/xf23id2/.ipython/profile_collection/startup/pyqt_scan_ui.ui", self)
        #uic.loadUi("pyqt_scan_ui.ui", self)

        ########### RE STOP FUNCTION ###########
        def stop_button_action():
            RE.stop()
           # bluesky_ui_logger.bs_ui_log("RE.stop()")
           # self.RE.stop()
           # self.RE.state == 'stop'
           # self.RE.is_stopped = True

        def pdxasscan_button_action():
            sui_start = self.pdxas_start_lineEdit.text() 
            sui_finish = self.pdxas_finish_lineEdit.text() 
            sui_velocity = self.pdxas_velocity_lineEdit.text() 
            sui_deadband = self.pdxas_deadband_lineEdit.text() 
            bluesky_ui_logger.bs_ui_log("RE(PD_scan(" + sui_start + "," + sui_finish + "," + sui_velocity + "," + sui_deadband + "))")
            RE(PD_scan(float(sui_start), float(sui_finish), float(sui_velocity), float(sui_deadband)))

        self.pdxas_pdxasscan_pushButton.clicked.connect(pdxasscan_button_action)

        self.pdxas_stop_button.clicked.connect(stop_button_action)

        
        ########### FIND SAMPLE SECTION ###############
        def findsample_button_action():
            sui_start = self.findsample_start_lineEdit.text() 
            sui_stop = self.findsample_stop_lineEdit.text() 
            sui_edge = self.findsample_edge_lineEdit.text() 
            sui_step = self.findsample_step_lineEdit.text() 
            bluesky_ui_logger.bs_ui_log("RE(find_sample(" + sui_edge + "," + sui_start + "," + sui_stop + "," + sui_step + "))")
            RE(find_sample(sui_edge, float(sui_start), float(sui_stop), float(sui_step)))
        self.findsample_findsample_pushButton.clicked.connect(findsample_button_action)

        self.findsample_stop_button.clicked.connect(stop_button_action)

        ########### XAS SCAN SECTION ###############
        def xasscan_button_action():
            sui_start = self.xasscan_start_lineEdit.text() 
            sui_finish = self.xasscan_finish_lineEdit.text() 
            sui_velocity = self.xasscan_velocity_lineEdit.text() 
            sui_deadband = self.xasscan_deadband_lineEdit.text() 
            sui_vortex = self.xasscan_vortex_checkBox.isChecked()
            sui_scaler = self.xasscan_scaler_checkBox.isChecked()

            if not sui_vortex and not sui_scaler:
                sui_vortex = True
            bluesky_ui_logger.bs_ui_log("RE(XAS_scan(" + sui_start + "," + sui_finish + "," + sui_velocity + "," + sui_deadband + ",inc_vortex = " + str(sui_vortex) + ", inc_sclr = " + str(sui_scaler) + "))")
            RE(XAS_scan(float(sui_start), float(sui_finish), float(sui_velocity), float(sui_deadband), inc_vortex = sui_vortex, inc_sclr = sui_scaler))
          

        self.xasscan_doscan_pushButton.clicked.connect(xasscan_button_action)

        def xasscan_vortex_checkbox_action():
            sui_vortex = self.xasscan_vortex_checkBox.isChecked()
            sui_scaler = self.xasscan_scaler_checkBox.isChecked()
            if not sui_vortex and sui_scaler:
                self.xasscan_scaler_checkBox.setEnabled(False)
            else :
                self.xasscan_scaler_checkBox.setEnabled(True)

        self.xasscan_vortex_checkBox.stateChanged.connect(xasscan_vortex_checkbox_action)

        def xasscan_scaler_checkbox_action():
            sui_vortex = self.xasscan_vortex_checkBox.isChecked()
            sui_scaler = self.xasscan_scaler_checkBox.isChecked()
            if sui_vortex and not sui_scaler:
                self.xasscan_vortex_checkBox.setEnabled(False)
            else :
                self.xasscan_vortex_checkBox.setEnabled(True)
        self.xasscan_scaler_checkBox.stateChanged.connect(xasscan_scaler_checkbox_action)

        self.xasscan_stop_button.clicked.connect(stop_button_action)


        ########### PEY XAS SCAN SECTION ###############
        def peyxas_setparams_buttonAction():
            sui_KE = self.peyxas_KE_lineEdit.text() 
            sui_PE = self.peyxas_PE_lineEdit.text() 
            sui_dwelltime = self.peyxas_dwelltime_lineEdit.text() 
            bluesky_ui_logger.bs_ui_log("RE(PEY_init(" + sui_KE + "," + sui_PE + "," + sui_dwelltime + "))")
            RE(PEY_init(float(sui_KE), float(sui_PE), float(sui_dwelltime)))
        self.peyxas_setparams_pushButton.clicked.connect(peyxas_setparams_buttonAction)

        def peyscan_button_action():
            sui_start = self.peyxas_start_lineEdit.text() 
            sui_finish = self.peyxas_finish_lineEdit.text() 
            sui_velocity = self.peyxas_velocity_lineEdit.text() 
            sui_deadband = self.peyxas_deadband_lineEdit.text() 
            bluesky_ui_logger.bs_ui_log("RE(PEY_XAS_scan(" + sui_start + "," + sui_finish + "," + sui_velocity + "," + sui_deadband + "))")
            RE(PEY_XAS_scan(float(sui_start), float(sui_finish), float(sui_velocity), float(sui_deadband)))
        self.peyxas_doscan_pushButton.clicked.connect(peyscan_button_action)

        self.peyxas_stop_button.clicked.connect(stop_button_action)

        ########### MULTISAMPLE BUTTON ACTION ##################
        def multisample_button_action():

            alertWindow = QMessageBox()
            alertWindow.setIcon(QMessageBox.Question)
            alertWindow.setWindowTitle("Alert!")
            alertWindow.setText("Did you save Sample List, Scan Parameters, and Detector Settings?")
            alertWindow.setStandardButtons(QMessageBox.Yes| QMessageBox.No)
            alertWindow.buttonClicked.connect(alert_button_action)

            val = alertWindow.exec_()
            #print("Return Value =", val)

            if val == 16384:
                bluesky_ui_logger.bs_ui_log("RE(multi_sample_edge())")
                RE(multi_sample_edge())
                #print ("SUCCES!")
            else :
                #print ("FAILURE")
                return
        
        def alert_button_action(buttonText):
            return

        self.xasflyscan_pushButton.clicked.connect(multisample_button_action)

        def load_all_excel_button_action():
            bluesky_ui_logger.bs_ui_log("RE(load_all_excel())")
            RE(load_all_excel())

        self.loadexcel_TEYPFY_pushButton.clicked.connect(load_all_excel_button_action)
    
        def xas_stepscan_button_action():
            alertWindow = QMessageBox()
            alertWindow.setIcon(QMessageBox.Question)
            alertWindow.setWindowTitle("Alert!")
            alertWindow.setText("Did you save Sample List, Scan Parameters, and Detector Settings?")
            alertWindow.setStandardButtons(QMessageBox.Yes| QMessageBox.No)
            alertWindow.buttonClicked.connect(alert_button_action)

            val = alertWindow.exec_()
            #print("Return Value =", val)

            if val == 16384:
                bluesky_ui_logger.bs_ui_log("RE(multi_step_scan())")
                RE(multi_step_scan())
                #print ("SUCCES!")
            else :
                #print ("FAILURE")
                return
        
        self.xasstepscan_pushButton.clicked.connect(xas_stepscan_button_action)

        def loadexcel_PEY_button_action():
            bluesky_ui_logger.bs_ui_log("RE(load_all_pey_excel())")
            RE(load_all_pey_excel())

        self.loadexcel_PEY_pushButton.clicked.connect(loadexcel_PEY_button_action)

        def multi_pey_button_action():
            alertWindow = QMessageBox()
            alertWindow.setIcon(QMessageBox.Question)
            alertWindow.setWindowTitle("Alert!")
            alertWindow.setText("Did you save Sample List, Scan Parameters, and Detector Settings?")
            alertWindow.setStandardButtons(QMessageBox.Yes| QMessageBox.No)
            alertWindow.buttonClicked.connect(alert_button_action)

            val = alertWindow.exec_()
            #print("Return Value =", val)

            if val == 16384:
                bluesky_ui_logger.bs_ui_log("RE(multi_pey_edge())")
                RE(multi_pey_edge())
                #print ("SUCCES!")
            else :
                #print ("FAILURE")
                return

        self.peyxasscan_pushButton.clicked.connect(multi_pey_button_action)

        excel_repeater_dict = {"XAS Fly Scan" : "tey_pfy_fly", "XAS Step Scan" : "tey_pfy_step", "PEY XAS Scan" : "pey_xas"}

        def excel_repeater_button_action():
            sui_max = self.excelrepeater_max_lineEdit.text()
            sui_scan_type = excel_repeater_dict[self.excelrepeater_comboBox.currentText()]

            bluesky_ui_logger.bs_ui_log("RE(excel_repeater(" + sui_max + ", \"" + sui_scan_type + "\"))")
            RE(Excel_Repeater(int(sui_max), sui_scan_type))

        
        self.excelrepeater_pushButton.clicked.connect(excel_repeater_button_action)

        self.multisample_stop_Button.clicked.connect(stop_button_action)


        ########### CUSTOM SCAN SECTION ##################

        custom_motor_dict = {"Photon Energy" : pgm.energy, "EPU1 Gap" : epu1.gap, "Au Mesh" : au_mesh, "IOXAS Sample" : ioxas_x, 
        "Diagnostic" : diag3_y,  "Exit Slit" : slt2, "Beam Position" : m1b1_setpoint}
        custom_det_dict = {"Photodiode" : "photodiode" , "Au Mesh" : "au_mesh", "Sample TEY" : "sample_tey",
        "Sample PFY" : "sample_pfy", "Sample TEY and PFY": "sample_tey_pfy", "Sample TEY and PEY" : "sample_tey_pey"}

        def customscan_y_combobox_action():
            y_selection = self.customscan_y_comboBox.currentText()
            y_lineEdit = self.customscan_y_lineEdit
            if y_selection == "Custom...":
                y_lineEdit.setEnabled(True)
            else:
                y_lineEdit.setEnabled(False)
        
        self.customscan_y_comboBox.activated.connect(customscan_y_combobox_action)

        def customscan_x_combobox_action():
            x_selection = self.customscan_x_comboBox.currentText()
            x_lineEdit = self.customscan_x_lineEdit
            if x_selection == "Custom...":
                x_lineEdit.setEnabled(True)
            else:
                x_lineEdit.setEnabled(False)
        
        self.customscan_x_comboBox.activated.connect(customscan_x_combobox_action)

        def customscan_button_action():
            det_selection = self.customscan_y_comboBox.currentText()
            motor_selection = self.customscan_x_comboBox.currentText()
            sui_start = self.customscan_start_lineEdit.text()
            sui_finish= self.customscan_finish_lineEdit.text()
            sui_step = self.customscan_step_lineEdit.text()

            if det_selection == "Custom...":
                det_selection = self.customscan_x_lineEdit.text()
            else :
                det_selection = custom_det_dict[det_selection]

            if motor_selection == "Custom...":
                motor_selection = getattr(sys.modules[__name__], self.customscan_y_lineEdit.text())
            else :
                motor_selection = custom_motor_dict[motor_selection]

            bluesky_ui_logger.bs_ui_log("RE(custom_scan(\"" + str(det_selection) +"\"," + str(motor_selection) + "," + sui_start + "," + sui_finish + "," + sui_step + "))")
            RE(custom_scan(det_selection, motor_selection, float(sui_start), float(sui_finish), float(sui_step)))

        self.customscan_doscan_pushButton.clicked.connect(customscan_button_action)
        self.customscan_stop_button.clicked.connect(stop_button_action)

        ########### TIME SCAN SECTION #############
        timeScan_dict = {"Photodiode" : "photodiode" , "Au Mesh" : "au_mesh", "Sample TEY" : "sample_tey",
        "Sample PFY" : "sample_pfy", "Sample TEY and PFY": "sample_tey_pfy", "Sample TEY and PEY" : "sample_tey_pey"}

        def timescan_button_action():
            det_selection = self.timescan_det_comboBox.currentText()
            bluesky_ui_logger.bs_ui_log("RE(time_scan(\"" + timeScan_dict[det_selection] + "\"))")
            RE(time_scan(timeScan_dict[det_selection]))

        self.timescan_doscan_pushButton.clicked.connect(timescan_button_action)
        self.timescan_stop_button.clicked.connect(stop_button_action)

        ########### COMMAND LINE SECTION ###############

        def customcmd_button_action():
            sui_cmd = self.cmdline_lineEdit.text()
            try:
                bluesky_ui_logger.bs_ui_log(sui_cmd)
                exec(sui_cmd)
            except:
                #print("Error running command: " + sui_cmd)
                return
        
        self.cmdline_pushButton.clicked.connect(customcmd_button_action)

        self.cmdline_stop_button.clicked.connect(stop_button_action)

        def search_lineEdit_action():
            if searching_flag == 1:
                if bluesky_ui_logger.logger_update_flag == 1:
                    bluesky_ui_logger.load_log_as_list()
                search_str = self.cmdline_search_lineEdit.displayText()
                if len(search_str) < 1 :
                    self.cmdline_lineEdit.setText("")
                    return
                bluesky_ui_logger.load_filtered_log(search_str)
                if len(bluesky_ui_logger.gui_filtered_log) < 1:
                    self.cmdline_lineEdit.setText("")
                else:
                    bluesky_ui_logger.filtered_log_line_count = len(bluesky_ui_logger.gui_filtered_log) - 1
                    self.cmdline_lineEdit.setText(bluesky_ui_logger.gui_filtered_log[bluesky_ui_logger.filtered_log_line_count].split(" : ")[1])
                    #print(bluesky_ui_logger.gui_filtered_log)
        self.cmdline_search_lineEdit.textChanged.connect(search_lineEdit_action)


    def keyPressEvent(self, event):
        #print("Key Press")
       # global logger_update_flag
       # global logger_line_count
       # global gui_log
        bluesky_ui_logger.check_file_size()
        global searching_flag
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ControlModifier and event.key() == Qt.Key_R:
            
            searching_flag = (searching_flag + 1) % 2
            search_lineEdit = self.cmdline_search_lineEdit

            if searching_flag == 0:
                search_lineEdit.setText("")
                bluesky_ui_logger.logger_line_count = len(bluesky_ui_logger.gui_log) - 1
                search_lineEdit.setEnabled(False)
            elif searching_flag == 1:
                search_lineEdit.setEnabled(True)
                search_lineEdit.setFocus()
                return

        if searching_flag == 0 :
            if event.key() == Qt.Key_Up :
                if bluesky_ui_logger.logger_update_flag == 1:
                    bluesky_ui_logger.load_log_as_list()
                    bluesky_ui_logger.logger_line_count = len(bluesky_ui_logger.gui_log) - 2
                    #bluesky_ui_logger.logger_update_flag = 0
                    if len(bluesky_ui_logger.gui_log) < 1 :
                        return
                    else :
                        self.cmdline_lineEdit.setText(bluesky_ui_logger.gui_log[bluesky_ui_logger.logger_line_count].split(" : ")[1])
                else :
                    bluesky_ui_logger.logger_line_count -= 1
                    if bluesky_ui_logger.logger_line_count < 0:
                        bluesky_ui_logger.logger_line_count = 0
                    else :
                        self.cmdline_lineEdit.setText(bluesky_ui_logger.gui_log[bluesky_ui_logger.logger_line_count].split(" : ")[1])
            if event.key() == Qt.Key_Down:
                if bluesky_ui_logger.logger_update_flag == 1:
                    bluesky_ui_logger.load_log_as_list()
                    bluesky_ui_logger.logger_line_count = len(bluesky_ui_logger.gui_log) - 2
                    #bluesky_ui_logger.logger_update_flag = 0
                    self.cmdline_lineEdit.setText("")
                else :
                    bluesky_ui_logger.logger_line_count += 1
                    if bluesky_ui_logger.logger_line_count >= len(bluesky_ui_logger.gui_log) - 1:
                        bluesky_ui_logger.logger_line_count = len(bluesky_ui_logger.gui_log) - 1
                        self.cmdline_lineEdit.setText("")
                    else :
                        self.cmdline_lineEdit.setText(bluesky_ui_logger.gui_log[bluesky_ui_logger.logger_line_count].split(" : ")[1])
        elif searching_flag == 1:   
            if len(bluesky_ui_logger.gui_filtered_log) == 0 :
                return
            if len(self.cmdline_search_lineEdit.displayText()) == 0:
                return
            if event.key() == Qt.Key_Up :
                
                bluesky_ui_logger.filtered_log_line_count -= 1
                if bluesky_ui_logger.filtered_log_line_count < 0:
                    bluesky_ui_logger.filtered_log_line_count = 0
                else :
                    self.cmdline_lineEdit.setText(bluesky_ui_logger.gui_filtered_log[bluesky_ui_logger.filtered_log_line_count].split(" : ")[1])
            if event.key() == Qt.Key_Down:
                bluesky_ui_logger.filtered_log_line_count += 1
                if bluesky_ui_logger.filtered_log_line_count >= len(bluesky_ui_logger.gui_filtered_log):
                    bluesky_ui_logger.filtered_log_line_count = len(bluesky_ui_logger.gui_filtered_log) - 1
                    self.cmdline_lineEdit.setText(bluesky_ui_logger.gui_filtered_log[bluesky_ui_logger.filtered_log_line_count].split(" : ")[1])
                else :
                    self.cmdline_lineEdit.setText(bluesky_ui_logger.gui_filtered_log[bluesky_ui_logger.filtered_log_line_count].split(" : ")[1])
            if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:

                bluesky_ui_logger.logger_line_count = len(bluesky_ui_logger.gui_log) - 1
                searching_flag = 0
                self.cmdline_search_lineEdit.setText("")
                self.cmdline_search_lineEdit.setEnabled(False)
                


        

def open_scan_gui():
    app = QApplication([])
    scanWindow = QT_Scan_GUI()
    scanWindow.show()
    sys.exit(app.exec())

#open_scan_gui()
