
#!/usr/bin/env python
import os
import sys
import getopt
from commands import getoutput
from PyQt4 import QtCore
from PyQt4 import QtGui
import re
import time
import logging
import sys
import functools
import subprocess
import time


from glob import glob
import functools
from collections import OrderedDict
import QCGui_project.solexometer.mainwindow as QC_ui
import QCGui_project.solexometer.dialog as QC_dial
import subprocess
from configobj import ConfigObj

class StreamToLogger(object):
        """
        Fake file-like stream object that redirects writes to a logger instance.
        """
        def __init__(self, logger, log_level=logging.INFO):
                self.logger = logger
                self.log_level = log_level
                self.linebuf = ''

        def write(self, buf):
                for line in buf.rstrip().splitlines():
                        self.logger.log(self.log_level, line.rstrip())


def atoi(text):
        return int(text) if text.isdigit() else text

def natural_keys(text):
        '''
        alist.sort(key=natural_keys) sorts in human order
        http://nedbatchelder.com/blog/200712/human_sorting.html
        (See Toothy's implementation in the comments)
        '''
        return [ atoi(c) for c in re.split('(\d+)', text) ]

class DialogWithCheckBox(QtGui.QMessageBox):
 
    def __init__(self, parent= None):
        super(DialogWithCheckBox, self).__init__()
 
        self.checkbox = QtGui.QCheckBox()
        self.checkbox.setChecked(True)
        #Access the Layout of the MessageBox to add the Checkbox
        layout = self.layout()
        layout.addWidget(self.checkbox, 1,2)
 
    def exec_(self, *args, **kwargs):
        """
        Override the exec_ method so you can return the value of the checkbox
        """
        return QtGui.QMessageBox.exec_(self, *args, **kwargs), self.checkbox.isChecked()
 
class MyDialog(QtGui.QDialog, QC_dial.Ui_Dialog):
        launchQC_signal=QtCore.pyqtSignal(bool, list, str, list, str, str,str,str)
        def __init__(self, folder, rlength, parent=None):
                self.folder=folder
                self.rlength=rlength
                self.gbs_path=''
                super(MyDialog, self).__init__(parent)
                count=0

                self.setupUi(self) 
                self.dial_ok.clicked.connect(self.closeDialog)
                self.dial_cancel.clicked.connect(self.close)                
                self.boxes=[]

                for p in form.programs_list:
                        wrong_path=0
                        for key in form.programs_list[p]:
                                if 'path' in key and not os.path.exists(form.programs_list[p][key]): 
                                        wrong_path=1
                        if wrong_path!=1:                
                                self.checkBox = QtGui.QCheckBox(self.scrollAreaWidgetContents)
                                self.gridLayout_3.addWidget(self.checkBox, count, 0, 1, 1)                              
                                self.checkBox.setObjectName("checkBox_%s"%p) 
                                _translate = QtCore.QCoreApplication.translate
                                self.checkBox.setText(_translate("Dialog", "%s"%p))
                                self.boxes.append(self.checkBox)
                                        
                                if p == 'GBS demultiplexing':
                                        self.gbsinfo = QtGui.QLineEdit(self.scrollAreaWidgetContents)
                                        self.gbsinfo.setMinimumWidth(200)
                                        self.gbsinfo.setObjectName("gbs_field")
                                        self.gridLayout_3.addWidget(self.gbsinfo, count, 1, 1, 1)
                                        self.gbsinfo.setDragEnabled(True)
                                        self.gbsinfo.setReadOnly(False)
                                        self.gbsinfo.setEnabled(False)
                                        self.gbsinfo.setAutoFillBackground(True)
                                        self.gbsbrowse = QtGui.QPushButton(self.scrollAreaWidgetContents)
                                        self.gbsbrowse.setMaximumSize(QtCore.QSize(100, 16777215))
                                        self.gridLayout_3.addWidget(self.gbsbrowse, count, 2, 1, 1)
                                        self.gbsbrowse.setText("Info file...")
                                        self.gbsbrowse.setCheckable(False)
                                        self.gbsbrowse.setEnabled(False)                                        
                                        self.gbsbrowse.setObjectName("gbsbrowse")    
                                        self.gbsbrowse.clicked.connect(self.selectFile)
                                        self.checkBox.stateChanged.connect(self.enable_gbs_widget)
                                        
                                elif p == 'Amplicons FLASH test':
                                        if len(self.rlength)!=2:
                                                self.checkBox.setEnabled(False)  
                                        self.horizontalLayout = QtGui.QHBoxLayout()
                                        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
                                        self.horizontalLayout.setSpacing(6)
                                        self.horizontalLayout.setObjectName("horizontalLayout")
                                        self.gridLayout_3.addLayout(self.horizontalLayout, count, 1, 1, 1)
                                        self.flash_p = QtGui.QLineEdit(self.scrollAreaWidgetContents)     
                                        self.flash_p.setObjectName("flash_p")
                                        self.flashlabel = QtGui.QLabel(self.scrollAreaWidgetContents)
                                        self.flashlabel.setObjectName("label")  
                                        self.flashlabel.setStyleSheet("font: italic 10pt \"Cantarell\";""color: grey;")                                        
                                        self.flashlabel.setText(_translate("Dialog", "Trimming threshold p:[0,1]. p="))
                                        self.flash_p.setText("0.05")
                                        self.flash_p.setAutoFillBackground(True)

                                        self.flash_p.setMinimumWidth(60)
                                        self.flash_p.setMaximumWidth(60)
                                        self.horizontalLayout.addWidget(self.flashlabel)      
                                        self.horizontalLayout.addWidget(self.flash_p)
                                        self.flash_p.setEnabled(False)                                        
                                        self.checkBox.stateChanged.connect(self.enable_flash_widget)
                                        
                                elif p=='Reads trimming':
                                        self.horizontalLayout = QtGui.QHBoxLayout()
                                        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
                                        self.horizontalLayout.setSpacing(6)
                                        self.horizontalLayout.setObjectName("horizontalLayout")
                                        self.gridLayout_3.addLayout(self.horizontalLayout, count, 1, 1, 1)
                                        self.trim_p = QtGui.QLineEdit(self.scrollAreaWidgetContents)     
                                        self.trim_p.setObjectName("trim_p")
                                        self.trimlabel = QtGui.QLabel(self.scrollAreaWidgetContents)
                                        self.trimlabel.setObjectName("label")  
                                        self.trimlabel.setStyleSheet("font: italic 10pt \"Cantarell\";""color: grey;")                                        
                                        self.trimlabel.setText(_translate("Dialog", "Trimming threshold p:[0,1]. p="))
                                        self.trim_p.setText("0.01")
                                        self.trim_p.setAutoFillBackground(True)

                                        self.trim_p.setMinimumWidth(60)
                                        self.trim_p.setMaximumWidth(60)
                                        self.horizontalLayout.addWidget(self.trimlabel)      
                                        self.horizontalLayout.addWidget(self.trim_p)
                                        self.trim_p.setEnabled(False)                                        
                                        self.checkBox.stateChanged.connect(self.enable_trim_widget)                                        
                                
                                elif p == 'Amplicons VSEARCH test':
                                        self.checkBox.setEnabled(False)  #until it becomes compatible with gzipped files
                                count+=1                        
                           
                self.nodesBox=QtGui.QComboBox(self)
                nodesList=["Auto", "com001", "com002", "com003", "com004", "com005", "com006"]
                self.nodesBox.addItems(nodesList)
                self.nodesLabel= QtGui.QLabel(self)
                self.nodesLabel.setText('Node to use')
                self.nodesBox.setMaximumWidth(80)
                
                self.gridLayout_3.addWidget(self.nodesLabel, count, 0, 1, 1)
                self.gridLayout_3.addWidget(self.nodesBox, count, 1, 1, 1)                
                self.nodesBox.setObjectName("nodesBox")
                
                _translate = QtCore.QCoreApplication.translate
                self.show()
                
        def enable_gbs_widget(self, state):
                if state == QtCore.Qt.Checked:
                        self.gbsinfo.setEnabled(True)
                        self.gbsbrowse.setEnabled(True)
                else:
                        self.gbsinfo.setEnabled(False)
                        self.gbsbrowse.setEnabled(False)
                        
        def enable_flash_widget(self, state):
                phix_checkbox=self.findChild(QtGui.QCheckBox, "checkBox_PhiX and adapters removal")                
                if state == QtCore.Qt.Checked:
                        self.flash_p.setEnabled(True)
                        phix_checkbox.setChecked(True)
                        phix_checkbox.setEnabled(False)
                else:
                        self.flash_p.setText("0.05")
                        self.flash_p.setEnabled(False)
                        phix_checkbox.setEnabled(True)
        def enable_trim_widget(self, state):
                if state == QtCore.Qt.Checked:
                        self.trim_p.setEnabled(True)
                else:
                        self.trim_p.setText("0.05")
                        self.trim_p.setEnabled(False)
                        
                        
        def selectFile(self):
                        self.gbs_path=QtGui.QFileDialog.getOpenFileName(self, 'Open file')[0]
                        self.gbsinfo.setText(self.gbs_path)

        def closeDialog(self):
                if self.findChild(QtGui.QCheckBox, "checkBox_Amplicons FLASH test").isChecked()==False and self.findChild(QtGui.QCheckBox, "checkBox_Reads trimming").isChecked()==False:
                        self.launchQC_signal.emit(True, self.boxes, self.folder, self.rlength, self.flash_p.text(), self.gbs_path, self.trim_p.text(), str(self.nodesBox.currentText()))
                        self.close()               
                else:        
                        if float(self.flash_p.text())<=1 and float(self.flash_p.text())>=0 and float(self.trim_p.text())<=1 and float(self.trim_p.text())>=0: 
                                if float(self.flash_p.text())<1 and not os.path.exists(form.programs_list["SolexaQA++"]['path']) and self.findChild(QtGui.QCheckBox, "checkBox_Amplicons FLASH test").isChecked():
                                        QtGui.QMessageBox.critical(self, "Error","Amplicons FLASH test needs SolexaQA++ to trim reads at p=%s.\nThere is no path indicated for SolexaQA++ in settings.txt, or it is wrong; correct and restart."%self.flash_p.text())
                                else:
                                        self.launchQC_signal.emit(True, self.boxes, self.folder, self.rlength, self.flash_p.text(), self.gbs_path, self.trim_p.text(),str(self.nodesBox.currentText()))
                                self.close()  
                                
                        else:
                                error=QtGui.QMessageBox.critical(self, "Error","The p threshold must be a value between 0 and 1")
                        
        def closeEvent(self, event):
                        event.accept()
                        form.new_table.setEnabled(True)
                        form.running_table.setEnabled(True)
                        form.completed_table.setEnabled(True)                        
                        self.deleteLater()       

class FORM(QtGui.QMainWindow, QC_ui.Ui_MainWindow):
        def __init__(self, parent=None):
                super(FORM, self).__init__(parent)
                self.setupUi(self)
                self.Config=ConfigObj('settings.txt')
                self.path_new=self.Config["FOLDERS"]["NEW_RUNS_FOLDER"]
                self.path_completed=self.Config["FOLDERS"]["COMPLETED_RUNS_FOLDER"]
                self.RawFolder.setText(self.path_new)
                self.CompletedFolder.setText(self.path_completed)
                self.RawBrowse.clicked.connect(functools.partial(self.selectFile, 'raw'))        
                self.CompletedBrowse.clicked.connect(functools.partial(self.selectFile, 'completed'))
                self.newruns, self.runningruns, self.completedruns = self.list_runs()
                self.new_table.setColumnWidth(0,260)
                self.new_table.setColumnWidth(1,110)
                self.new_table.setColumnWidth(2,100)
                self.new_table.setColumnWidth(3,90)                
                self.new_table.name="New"
                self.running_table.setColumnWidth(0,260)
                self.running_table.setColumnWidth(1,110)
                self.running_table.setColumnWidth(2,70)
                self.running_table.setColumnWidth(3,50)
                self.running_table.setColumnWidth(4,130) 
                self.running_table.name="Running"
                self.completed_table.setColumnWidth(0,260)
                self.completed_table.setColumnWidth(1,90)
                self.completed_table.setColumnWidth(2,80)
                self.completed_table.setColumnWidth(3,90)
                self.completed_table.setColumnWidth(4,90)
                
                self.completed_table.name="Complete"

                self.filltable(self.new_table, self.newruns)
                self.filltable(self.running_table, self.runningruns)
                self.filltable(self.completed_table, self.completedruns)

                self.programs_list=self.list_programs()
                self.show()



        def updatetable(self):
                self.newruns, self.runningruns, self.completedruns = self.list_runs()
                self.filltable(self.new_table, self.newruns)
                self.filltable(self.running_table, self.runningruns)
                self.filltable(self.completed_table, self.completedruns)		

        def list_runs(self):
                # Read settings file
                self.path_new=str(self.RawFolder.text())
                self.path_completed=str(self.CompletedFolder.text())

                if not os.path.exists(self.path_new) or not os.path.exists(self.path_completed):
                        folders_reply=QtGui.QMessageBox.question(self, "Problem",'The paths to the "NEW" and/or "COMPLETED" runs provided\nin the settings file do not exist. Create?', QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
                        if folders_reply==QtGui.QMessageBox.Yes:
                                os.system('mkdir -p %s %s'%(self.path_new,self.path_completed))
                        else:
                                sys.exit()
                runningruns=[]
                newfolder=next(os.walk(self.path_new))[1]
                newruns=[]
                for n in newfolder:
                        if glob('%s/%s/*.fastq.gz'%(self.path_new,n))!=[]:
                                newruns.append('%s'%(n))
                        elif os.path.exists('%s/%s/Data/Intensities/BaseCalls'%(self.path_new,n)):
                                                newruns.append('%s'%(n))
                        
                completedfolder=next(os.walk(self.path_completed))[1]
                completedruns=[]
                for c in completedfolder:
                        if glob('%s/%s/*.fastq.gz'%(self.path_new,c))!=[]:
                                completedruns.append('%s'%c)
                        elif os.listdir('%s/%s'%(self.path_completed,c))!=[]:
                                if os.path.isdir('%s/%s/%s'%(self.path_completed,c,os.listdir('%s/%s'%(self.path_completed,c))[0])):
                                        completedruns.append('%s'%(c))
                                elif os.path.isdir('%s/%s/fQsequences'%(self.path_completed,c,)):
                                        completedruns.append('%s'%c)
                        
                for c in completedruns[:]:
                        if not os.path.exists('%s/%s/checkPoint1done.txt'%(self.path_completed,c)):
                                completedruns.remove(c)
                
                for c in completedruns[:]:
                        if not os.path.exists('%s/%s/checkPoint2done.txt'%(self.path_completed,c)) or len(open('%s/%s/checkPoint2done.txt'%(self.path_completed,c)).readlines())==1:
                                runningruns.append(c)
                                completedruns.remove(c)

                                if (os.path.exists('%s/%s/QC_log.txt'%(self.path_completed,c)) and open('%s/%s/QC_log.txt'%(self.path_completed,c)).readlines()[-1].startswith('Stopped')) or not os.path.exists('%s/%s/QC_log.txt'%(self.path_completed,c)):
                                        runningruns.remove(c)
                 
                newruns=list(set(newruns)-((set(completedruns)| set(runningruns))))
                newruns.sort(key=natural_keys)
                runningruns.sort(key=natural_keys)
                completedruns.sort(key=natural_keys)
                return newruns, runningruns, completedruns


        def filltable(self, table, array):
                #os.system('ls %s>/dev/null'%self.path_completed)
                table.setRowCount(len(array))
                for row in range(len(array)):

                        table.setItem(row, 0, QtGui.QTableWidgetItem(array[row].split('/')[-1]))
                        project_ID, date, rlength, client, jobid, status=self.fill_projectInfo(table.name, array[row])
                        table.setItem(row, 1, QtGui.QTableWidgetItem(project_ID))
                        if table.name=="New" or table.name=="Complete":
                                table.setItem(row, 2, QtGui.QTableWidgetItem(client))			
                                table.setItem(row, 3, QtGui.QTableWidgetItem(date))			
                        else:
                                table.setItem(row, 2, QtGui.QTableWidgetItem(date))
                                table.setItem(row, 3, QtGui.QTableWidgetItem(jobid))
                                table.setItem(row, 4, QtGui.QTableWidgetItem(status))


                        self.drawButtons(table, row, array[row], rlength, jobid)
                        
        def fill_projectInfo(self, table, folder):
                project='unknown'
                date='unknown'
                client='unknown'
                rlength=[]
                jobid='unknown'
                status='unknown'
                r2_check=[]
                try:
                        sampleSheet=open('%s/%s/SampleSheet.csv'%(self.path_new, folder)).readlines()
                except:
                        project='unknown'              
			if os.path.exists('%s/%s/Data/Intensities/BaseCalls/'%(self.path_new, folder)):                                                           #in case a SampleSheet is not present, infer paired status
                        	r2_check=glob('%s/%s/Data/Intensities/BaseCalls/*_R2_*.fastq*'%(self.path_new, folder))
			elif os.path.exists('%s/%s'%(self.path_new, folder)):
				r2_check=glob('%s/%s/*_R2*.fastq*'%(self.path_new, folder))
                        if r2_check!=[]:
                                rlength=['x','x']
                        else:
                                rlength=['x']
                else:
                        for i in range(0,len(sampleSheet)):
                                l=sampleSheet[i]
                                if l.startswith('Experiment Name'):
                                        project=l.split(',')[1].strip()
                                if l.startswith('Date') and table=="New":
                                        date=l.split(',')[1].strip()
                                if l.startswith('Investigator'):
                                        client=l.split(',')[1].strip()
                                if l.startswith('[Reads]') and table=="New":
                                        rlength.append(sampleSheet[i+1].split(',')[0].strip())
                                        if sampleSheet[i+2].split(',')[0].strip()!='' and not sampleSheet[i+2].startswith('['):
                                                rlength.append(sampleSheet[i+2].split(',')[0].strip())

                if table=="Running":
                        if os.path.exists('%s/%s/checkPoint1done.txt'%(self.path_completed, folder)) :
                                checkpoint1=open('%s/%s/checkPoint1done.txt'%(self.path_completed, folder)).readlines()
                                for l in checkpoint1:
                                        if l.startswith('Starting'):
                                                date=l.split(' on ')[1].strip()
                                                date=time.strptime(date)
                                                date=time.strftime("%d/%m/%Y", date)
                        if os.path.exists('%s/%s/QC_log.txt'%(self.path_completed, folder)):
                                        jobid=open('%s/%s/QC_log.txt'%(self.path_completed, folder)).readlines()[0].split('JOB')[1].strip()
                                        for l in open('%s/%s/QC_log.txt'%(self.path_completed, folder)).readlines():
                                                if l.startswith('### Progress'):
                                                        status=l.strip().split('### ')[-1]

                                
                elif table=="Complete":
                        checkpoint2=open('%s/%s/checkPoint2done.txt'%(self.path_completed, folder)).readlines()
                        for l in checkpoint2:
                                if l.startswith('Completed '):
                                        date=l.split(' on ')[1].split('.')[0].strip()
                                        date=time.strptime(date)
                                        date=time.strftime("%d/%m/%Y", date)

                return project.strip(), date, rlength, client, jobid, status


        def drawButtons(self, table, row, folder_name, rlength, jobid):
                if table.name=="New":
                        label="Launch QC"
                        color='#00ab2e'
                        table_button=QtGui.QPushButton(label, clicked=lambda: self.cellClicked(table, row, folder_name, rlength, label, ''))
                        table_button.setStyleSheet('color:%s; background-color:None;font-size:10pt;'%color)
                        table.setCellWidget(row, 4, table_button)                        
                elif table.name=="Complete":
                        label="Summary"
                        color='#3773cc'
                        summary_table_button=QtGui.QPushButton(label, clicked=lambda: self.cellClicked(table, row, folder_name, rlength, 'Summary', ''))
                        summary_table_button.setStyleSheet('color:%s; background-color:None; font-size:10pt;'%color)
                        if glob('%s/%s/QCdata/SolexaQA++/*'%(self.path_completed,folder_name))==[]:
                                summary_table_button.setEnabled(False)
                        table.setCellWidget(row, 4, summary_table_button) 
                        label="Report"
                        color="red"
                        report_table_button=QtGui.QPushButton(label, clicked=lambda: self.cellClicked(table, row, folder_name, rlength, 'Report'))
                        report_table_button.setStyleSheet('color:%s; background-color:None;font-size:10pt;'%color)    
                        table.setCellWidget(row, 5, report_table_button) 
                        report_table_button.setEnabled(False)
                        
                else:
                        label="Kill"
                        color='Black'
                        table_button=QtGui.QPushButton(label, clicked=lambda: self.cellClicked(table, row, folder_name, rlength, label, jobid))
                        table_button.setStyleSheet('color:%s; background-color:None;font-size:10pt;'%color)
                        table.setCellWidget(row, 5, table_button)                        




        def cellClicked(self, table, row, folder_name, rlength, label, jobid):
                if table.name=="Complete":
                        if label=="Summary":   
                                pdfs=glob("%s/%s/QCdata/SolexaQA++/summary/*.pdf"%(self.path_completed,folder_name))
                                for p in pdfs:
                                        process = subprocess.Popen(['/usr/bin/evince', '-w', p], shell=False, stdout=subprocess.PIPE)
                elif table.name=="New":
                        self.open_dialog(folder_name, rlength)
                
                elif table.name=="Running":
#                        dialog = DialogWithCheckBox()
#                        dialog.setWindowTitle("Kill job")
 #                       dialog.setText("Kill Job %s?"%jobid)
  #                      dialog.checkbox.setText("Remove intermediate results")
   #                     dialog.setStandardButtons(QtGui.QMessageBox.Yes |QtGui.QMessageBox.No)
    #                    dialog.setDefaultButton(QtGui.QMessageBox.No)
     #                   dialog.setIcon(QtGui.QMessageBox.Question)
                        reply = QtGui.QMessageBox.question(self, 'Message', "Are you sure to quit?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
                        if reply == QtGui.QMessageBox.Yes:
                                os.system('pkill -TERM -P %s;'%(jobid))
                                os.system("echo 'Stopped on %s' >> %s/%s/QC_log.txt"%(time.time(), self.path_completed, folder_name))                       

                                            

        def open_dialog(self, folder, rlength):
                self.disableMain()
                dialog = MyDialog(folder, rlength)	
                dialog.launchQC_signal.connect(self.launchQC)

                dialog.exec_()
                dialog.show()

        def disableMain(self):
                self.new_table.setEnabled(False)
                self.running_table.setEnabled(False)
                self.completed_table.setEnabled(False)

        def selectFile(self, name):
                if name == 'raw':
                        self.RawFolder.setText(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))
                        self.rawdir=self.RawFolder.text()
                        if self.rawdir=='':
                                self.path_new=self.Config["FOLDERS"]["NEW_RUNS_FOLDER"]
                                self.RawFolder.setText(self.path_new)

		if name == 'completed':
                        self.CompletedFolder.setText(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))
                        self.completedir=self.CompletedFolder.text()
                        if self.completedir=='':
                                self.path_complete=self.Config["FOLDERS"]["COMPLETED_RUNS_FOLDER"]
                                self.CompletedFolder.setText(self.path_complete)

                        
        def launchQC(self, signal, programs, folder, rlength, flash_p, gbs_infopath, trim_p, node):
                logging.info("Launched QC on %s, using node %s"%(folder,node))
                self.new_table.setEnabled(True)
                self.running_table.setEnabled(True)
                self.completed_table.setEnabled(True)
                QC_out='%s/%s'%(self.path_completed, folder)
		r2_check=[]
                if rlength==[]:              
			if os.path.exists('%s/%s/Data/Intensities/BaseCalls/'%(self.path_new, folder)):                                                           #in case a SampleSheet is not present, infer paired status
                        	r2_check=glob('%s/%s/Data/Intensities/BaseCalls/*_R2_*.fastq*'%(self.path_new, folder))
			elif os.path.exists('%s/%s'%(self.path_new, folder)):
				r2_check=glob('%s/%s/*_R2*.fastq*'%(self.path_new, folder))
				print 'Checking %s/%s'%(self.path_new, folder)
				print r2_check
                        if r2_check!=[]:
                                rlength=['x','x']
                        else:
                                rlength=['x']
                homedir=os.getenv('HOME')
                TMPDIR=getoutput('mktemp -d /tmp/%s.XXXXXXXX'%folder.split('/')[-1])
                cmd_file='%s/%s.txt'%(homedir,folder.split('/')[-1])
                os.system('> %s && chmod a+x %s'%(cmd_file, cmd_file))
                cmd_file=open(cmd_file,'a')
                cmd_file.write('''#!/bin/bash
maindir=`pwd`
set +o posix
mkdir -p %s/fQsequences %s/QCdata %s/images;
echo "Starting file finding on $(date '+%%a %%b %%d %%H:%%M:%%S %%Y')" >> %s/checkPoint1done.txt
                '''%(QC_out,QC_out,QC_out, QC_out))

		if glob('%s/%s/Data/Intensities/BaseCalls/*.fastq*'%(self.path_new, folder))!=[]:	#MiSeq folder structure
			cmd_file.write('''
echo "### Progress ### Copying fastq files" >> %s/QC_log.txt;
cp %s/%s/Data/Intensities/BaseCalls/*.fastq* %s/fQsequences 2>&1 | tee -a %s/QC_log.txt;
cp %s/%s/SampleSheet.csv %s
			'''%(QC_out, self.path_new, folder,QC_out,QC_out, self.path_new, folder,QC_out))
		else:								#Generic folder containing fastq files
			cmd_file.write('''
echo "### Progress ### Copying fq files" >> %s/QC_log.txt;
cp %s/%s/*.fastq* %s/fQsequences 2>&1 | tee -a %s/QC_log.txt;			
					'''%(QC_out, self.path_new, folder,QC_out,QC_out))
			
		cmd_file.write('''
echo "Checkpoint1 completed on $(date '+%%a %%b %%d %%H:%%M:%%S %%Y')" >> %s/checkPoint1done.txt
cd %s; for file in fQsequences/*.fastq*; do md5sum "$file" >> %s/fQsequences/md5checksums.txt; done
cd $maindir

                '''%(QC_out, QC_out,QC_out))
                selected_progs=[]

                for p in programs:
                        if p.isChecked()==True:
                                prog_name=p.objectName().split('checkBox_')[1]
                                selected_progs.append(str(prog_name))
                for p in selected_progs:
                        logging.info('Including %s in pipeline, with options:'%p)
                        for elem in self.programs_list[p]:
                                logging.info('\t'+elem+': '+self.programs_list[p][elem])


                cmd_file.write('''
echo "Starting QC analysis on $(date '+%%a %%b %%d %%H:%%M:%%S %%Y')" > %s/checkPoint2done.txt                        
                '''%QC_out)


####### GBS demultiplexing #####################################
                
                if 'GBS demultiplexing' in selected_progs: 
                        cmd_file.write('''
echo "### Progress ### Demultiplexing GBS" >> %s/QC_log.txt;
mkdir %s/fQsequences/multiplexed
mv %s/fQsequences/*.fastq* %s/fQsequences/multiplexed; gzip -d %s/fQsequences/multiplexed/*.fastq.gz
for file in %s/fQsequences/multiplexed/*.fastq; do
java -jar %s --Demultiplexer -f1 "$file" -i %s -o %s/fQsequences 2>&1 | tee -a %s/QC_log.txt
done

sum_counts=0
rowcount=0
while read ID barcode enzyme count totalperc mismatch0count mismatch0perc mismatch1count mismatch1perc basecallcount basecallabove30perc basecallqualavg
do
        [ "$ID" == "sampleID" ] && continue 
        [ "$ID" == "BLANK" ] && continue 
        [ "$ID" == "undetermined" ] && continue 
        let sum_counts=sum_counts+count
        let rowcount=rowcount+1
done < '%s/fQsequences/gbsDemultiplex.stats'
avg=$(bc<<<"scale=4; $sum_counts/$rowcount") 

sd_sum=0
while read ID barcode enzyme count totalperc mismatch0count mismatch0perc mismatch1count mismatch1perc basecallcount basecallabove30perc basecallqualavg
do
        [ "$ID" == "sampleID" ] && continue 
        [ "$ID" == "BLANK" ] && continue 
        [ "$ID" == "undetermined" ] && continue 

	sd_sum=$(bc<<<"$sd_sum+($count-$avg)*($count-$avg)")
done < '%s/fQsequences/gbsDemultiplex.stats'
stderr=$(bc<<<"scale=2; $sd_sum/$rowcount")
stdev=$(bc<<<"scale=2; sqrt($stderr)")
cv=$(bc<<<"scale=2; $stdev/$avg")
echo $'\r'""$'\r'"Mean=$avg"$'\r'"SD=$stdev"$'\r'"CV=$cv">>'%s/fQsequences/gbsDemultiplex.stats'
                        '''%(QC_out,QC_out,QC_out,QC_out,QC_out,QC_out,self.programs_list["GBS demultiplexing"]['path_gbsx'], gbs_infopath, QC_out,QC_out,
                             QC_out,QC_out,QC_out))


####### FastQC #####################################
                
                if 'FastQC' in selected_progs:
                        cmd_file.write('''
echo "### Progress ### FastQC" >> %s/QC_log.txt;
mkdir %s/QCdata/FastQC
for file in %s/fQsequences/*.fastq*; do %s -t 16 -o %s/QCdata/FastQC/ --extract "$file" 2>&1 | tee -a %s/QC_log.txt; done
                        '''%(QC_out,QC_out,QC_out,self.programs_list["FastQC"]['path'],QC_out, QC_out))



####### SolexaQA++ #####################################

                if 'SolexaQA++' in selected_progs:
                        options = ["--%s %s"%(key,value) for key, value in self.programs_list["SolexaQA++"].items() if 'path' not in key]                          
                        cmd_file.write('''
echo "### Progress ### SolexaQA++" >> %s/QC_log.txt;
mkdir %s/QCdata/SolexaQA++
for file in %s/fQsequences/*.fastq*; do %s analysis -d %s/QCdata/SolexaQA++/ %s "$file" 2>&1 | tee -a %s/QC_log.txt; done
%s -p %s/QCdata/SolexaQA++/ -f %s/fQsequences/ 2>&1 | tee -a %s/QC_log.txt
cp %s/QCdata/SolexaQA++/summary/* %s/images
cp `ls %s/QCdata/SolexaQA++/*.pdf | head -8` %s/images
                                        '''%(QC_out, QC_out, QC_out, self.programs_list["SolexaQA++"]['path'], QC_out, ' '.join(options),QC_out,self.programs_list["SolexaQA++"]['summary_script_path'],QC_out, QC_out,QC_out,
                                             QC_out,QC_out,
                                             QC_out,QC_out))                



####### FastQScreen #####################################

                if 'FastQScreen' in selected_progs:
                        options = ["--%s %s"%(key,value) for key, value in self.programs_list["FastQScreen"].items() if key != 'path']  
                        cmd_file.write('''
echo "### Progress ### FastQScreen" >> %s/QC_log.txt;
mkdir %s/QCdata/FastQScreen/
for file in %s/fQsequences/*.fastq*; do %s --aligner bowtie2 --outdir %s/QCdata/FastQScreen/ %s "$file" 2>&1 | tee -a %s/QC_log.txt; done

mkdir %s/fQsequences/subsamples
n_samples=$(ls %s/fQsequences/*_R1_*.fastq* | wc -l);
echo $n_samples
for file in %s/fQsequences/*_R1_*.fastq*;
	do 
		echo "$file"
		lines=$(zcat "$file" | wc -l);
		echo $lines
		reads=$((lines/4))
		echo $reads
		subsize=$(bc -l <<< "scale=2; 100000/$((n_samples))");
		subsize=${subsize%%%%.*};
		subsize=$((subsize<$((reads)) ? subsize : $((reads))))
		echo $subsize;
		zcat "$file"| awk '{ printf("%%s",$0); n++; if(n%%4==0) {printf("\\n");} else { printf("\\t");} }' |awk -v k=$subsize 'BEGIN{srand(systime() + PROCINFO["pid"]);}{s=x++<k?x-1:int(rand()*x);if(s<k)R[s]=$0}END{for(i in R)print R[i]}' |awk -F"\\t" '{print $1"\\n"$2"\\n"$3"\\n"$4 >> "%s/fQsequences/subsamples/subsample_R1.fastq"}'

	done;

for file in %s/fQsequences/*_R2_*.fastq*;
	do 
		echo "$file"
		lines=$(zcat "$file" | wc -l);
		echo $lines
		reads=$((lines/4))
		echo $reads
		subsize=$(bc -l <<< "scale=2; 100000/$((n_samples))");
		subsize=${subsize%%%%.*};
		subsize=$((subsize<$((reads)) ? subsize : $((reads))))
		echo $subsize;
		zcat "$file"| awk '{ printf("%%s",$0); n++; if(n%%4==0) {printf("\\n");} else { printf("\\t");} }' |awk -v k=$subsize 'BEGIN{srand(systime() + PROCINFO["pid"]);}{s=x++<k?x-1:int(rand()*x);if(s<k)R[s]=$0}END{for(i in R)print R[i]}' |awk -F"\\t" '{print $1"\\n"$2"\\n"$3"\\n"$4 >> "%s/fQsequences/subsamples/subsample_R2.fastq"}'

	done;
	
for file in %s/fQsequences/subsamples/*.fastq; do %s --subset 0 --aligner bowtie2 --outdir %s/images/ %s "$file" 2>&1 | tee -a %s/QC_log.txt; done	
                                        '''%(QC_out, QC_out,QC_out,self.programs_list["FastQScreen"]['path'],QC_out,' '.join(options), QC_out,
					     QC_out,
					     QC_out,
					     QC_out,
					     QC_out,
					     QC_out,
					     QC_out,
					     QC_out,self.programs_list["FastQScreen"]['path'],QC_out,' '.join(options), QC_out))


####### PhiX and adapters removal #####################################

                if 'PhiX and adapters removal' in selected_progs:
                        if len(rlength)==1:
                                cmd_file.write('''
echo "### Progress ### PhiX and adapters" >> %s/QC_log.txt;
mkdir -p %s/QCdata/PhiX_removal
mkdir %s/processed
for file in %s/fQsequences/*.fastq*; do %s -x %s -p 16 -U "$file" -S %s/QCdata/PhiX_removal/$(basename "$file").sam 2>&1 | tee -a %s/QC_log.txt; done
for file in %s/QCdata/PhiX_removal/*.sam; do
    grep -v "ref|NC_001422.1" "$file" > %s/QCdata/PhiX_removal/$(basename "$file").clean
    grep "ref|NC_001422.1" "$file" > %s/QCdata/PhiX_removal/$(basename "$file").phix 
    fastq_out_name=$(basename "$file")
    fastq_out_name="${fastq_out_name%%%%.*}"
    
    shopt -s nocasematch
    if [[ $file !=  *"Undetermined"* ]];then
        %s SamToFastq INPUT=%s/QCdata/PhiX_removal/$(basename "$file").clean FASTQ=%s/"$fastq_out_name"_noPhiX.fastq 2>&1 | tee -a %s/QC_log.txt
        %s -k 0 -o %s/processed/processed_"$fastq_out_name".fastq.gz %s %s/"$fastq_out_name"_noPhiX.fastq 2>&1 | tee -a %s/QC_log.txt
    fi
    
    if [[ $file ==  *"Undetermined"* ]];then
         echo "UNDET!"
         mkdir %s/QCdata/PhiX_quality
         %s view -hF 4 -S %s/QCdata/PhiX_removal/$(basename "$file").phix > %s/QCdata/PhiX_removal/$(basename "$file")_FILTERED.phix
         %s SamToFastq VALIDATION_STRINGENCY=LENIENT INPUT=%s/QCdata/PhiX_removal/$(basename "$file")_FILTERED.phix FASTQ=/dev/stdout | gzip >%s/QCdata/PhiX_quality/PhiX_S0_L001_R1.fastq.gz
         if [ -f '%s' ]; then
             %s analysis %s/QCdata/PhiX_quality/*.fastq.gz 2>&1 | tee -a %s/QC_log.txt
         fi
    fi
    rm -r "$file"
    rm -r "$file".clean

    shopt -u nocasematch

done
rm -r %s/QCdata/PhiX_removal
rm -r %s/processed/*noPhiX.fastq
cd %s; for file in processed/*.fastq*; do md5sum "$file" >> %s/processed/md5checksums.txt; done
cd $maindir
                                '''%(QC_out, TMPDIR,QC_out, QC_out,self.programs_list["PhiX and adapters removal"]['path_bowtie2'], 
                                     self.programs_list["PhiX and adapters removal"]['x'], TMPDIR,QC_out,TMPDIR, TMPDIR, 
                                     TMPDIR,self.programs_list["PhiX and adapters removal"]['path_picard'], TMPDIR,TMPDIR,QC_out,
                                     self.programs_list["PhiX and adapters removal"]['path_fastq-mcf'],QC_out,self.programs_list["PhiX and adapters removal"]['adapters_list'],TMPDIR,QC_out,
                                     QC_out,
                                     self.programs_list["PhiX and adapters removal"]['path_samtools'], TMPDIR, TMPDIR,
                                     self.programs_list["PhiX and adapters removal"]['path_picard'],TMPDIR,QC_out,
                                     self.programs_list["SolexaQA++"]['path'],self.programs_list["SolexaQA++"]['path'],QC_out,QC_out,
                                     QC_out,QC_out, QC_out, QC_out))
                                
                        elif len(rlength)==2:
                                cmd_file.write('''
echo "### Progress ### PhiX and adapters\n" >> %s/QC_log.txt;                                
mkdir -p %s/QCdata/PhiX_removal
mkdir %s/processed
shopt -s nullglob; fqfiles=(%s/fQsequences/*.fastq*) 
readarray -t sorted < <(printf '%%s\\0' "${fqfiles[@]}" | sort -z | xargs -0n1)
for ((i=0; i<${#fqfiles[@]} ; i=i+2)); do %s -x %s -p 16 -1 "${fqfiles[i]}" -2 "${fqfiles[i+1]}" -S %s/QCdata/PhiX_removal/$(basename "${fqfiles[i]}").sam 2>&1 | tee -a %s/QC_log.txt; done
count=0
for file in %s/QCdata/PhiX_removal/*.sam; do
    grep -v "ref|NC_001422.1" "$file" > %s/QCdata/PhiX_removal/$(basename "$file").clean
    grep "ref|NC_001422.1" "$file" > %s/QCdata/PhiX_removal/$(basename "$file").phix 
    fastq_out_name1=$(basename "${fqfiles[count]}")
    fastq_out_name1="${fastq_out_name1%%%%.*}"
    fastq_out_name2=$(basename "${fqfiles[count+1]}")
    fastq_out_name2="${fastq_out_name2%%%%.*}" 
    shopt -s nocasematch
    if [[ $file !=  *"Undetermined"* ]];then
        %s SamToFastq INPUT=%s/QCdata/PhiX_removal/$(basename "$file").clean FASTQ=%s/"$fastq_out_name1"_noPhiX.fastq SECOND_END_FASTQ=%s/"$fastq_out_name2"_noPhiX.fastq 2>&1 | tee -a %s/QC_log.txt

        # Paired status check
        cat %s/"$fastq_out_name1"_noPhiX.fastq | awk '{ printf("%%s",$0); n++; if(n%%4==0) { printf("\\n");} else { printf("\\t\\t");} }' |awk '{i=index($1,"/"); printf("%%s\\t%%s\\n",substr($1,1,i-1),$0);}' |sort -k1,1 > %s/sorted1.fq
        cat %s/"$fastq_out_name2"_noPhiX.fastq | awk '{ printf("%%s",$0); n++; if(n%%4==0) { printf("\\n");} else { printf("\\t\\t");} }' |awk '{i=index($1,"/"); printf("%%s\\t%%s\\n",substr($1,1,i-1),$0);}' |sort -k1,1 > %s/sorted2.fq
        join -1 1 -2 1 %s/sorted1.fq %s/sorted2.fq > %s/joined_sorted.fq
        cat %s/joined_sorted.fq | awk '{print substr($2"\\n"$3"\\n"$4"\\n"$5,1)}' > %s/"$fastq_out_name1"_noPhiX_sorted.fastq
        cat %s/joined_sorted.fq | awk '{print substr($6"\\n"$7"\\n"$8"\\n"$9,1)}' > %s/"$fastq_out_name2"_noPhiX_sorted.fastq
        rm -r %s/joined_sorted.fq %s/sorted1.fq %s/sorted2.fq %s/*noPhiX.fastq
        # end
    
        %s -k 0 -o %s/processed/processed_"$fastq_out_name1".fastq.gz -o %s/processed/processed_"$fastq_out_name2".fastq.gz %s %s/"$fastq_out_name1"_noPhiX_sorted.fastq %s/"$fastq_out_name2"_noPhiX_sorted.fastq 2>&1 | tee -a %s/QC_log.txt
    
    fi
    if [[ $file ==  *"Undetermined"* ]];then
         echo "UNDET!"
         mkdir %s/QCdata/PhiX_quality
         %s view -hF 4 -S %s/QCdata/PhiX_removal/$(basename "$file").phix > %s/QCdata/PhiX_removal/$(basename "$file")_FILTERED.phix
         %s SamToFastq VALIDATION_STRINGENCY=LENIENT INPUT=%s/QCdata/PhiX_removal/$(basename "$file")_FILTERED.phix FASTQ=%s/QCdata/PhiX_quality/PhiX_S0_L001_R1.fastq.gz SECOND_END_FASTQ=%s/QCdata/PhiX_quality/PhiX_S0_L001_R2.fastq.gz 2>&1 | tee -a %s/QC_log.txt
         if [ -f '%s' ]; then
             %s analysis %s/QCdata/PhiX_quality/*.fastq.gz 2>&1 | tee -a %s/QC_log.txt
         fi
    fi
    shopt -u nocasematch

    rm -r %s/*noPhiX*.fastq
    rm -r "$file"
    rm -r "$file".clean

    let count=count+2
done
rm -r %s/QCdata/PhiX_removal
cd %s; for file in processed/*.fastq*; do md5sum "$file" >> %s/processed/md5checksums.txt; done
cd $maindir
                                '''%(QC_out,TMPDIR,QC_out, QC_out, self.programs_list["PhiX and adapters removal"]['path_bowtie2'], 
                                     self.programs_list["PhiX and adapters removal"]['x'], TMPDIR, QC_out, TMPDIR, TMPDIR, 
                                     TMPDIR,self.programs_list["PhiX and adapters removal"]['path_picard'], TMPDIR,TMPDIR,TMPDIR,QC_out,
                                     TMPDIR,TMPDIR,TMPDIR,TMPDIR,TMPDIR,TMPDIR,TMPDIR,TMPDIR,TMPDIR,TMPDIR,TMPDIR,TMPDIR,TMPDIR,TMPDIR,TMPDIR,                                     
                                     self.programs_list["PhiX and adapters removal"]['path_fastq-mcf'],QC_out,QC_out,self.programs_list["PhiX and adapters removal"]['adapters_list'],TMPDIR, TMPDIR,QC_out,
                                     QC_out,self.programs_list["PhiX and adapters removal"]['path_samtools'], TMPDIR, TMPDIR,
                                     self.programs_list["PhiX and adapters removal"]['path_picard'], TMPDIR, QC_out, QC_out, QC_out,
                                     self.programs_list["SolexaQA++"]['path'],self.programs_list["SolexaQA++"]['path'],QC_out, QC_out,
                                     TMPDIR, TMPDIR,QC_out,QC_out))
     

####### FLASH merging R1+R2 for amplicons #####################################
                                
                if 'Amplicons FLASH test' in selected_progs:
                                print flash_p
                                if float(flash_p)==1:
                                        cmd_file.write('''
echo "### Progress ### FLASH merging\n" >> %s/QC_log.txt;
mkdir %s/QCdata/FLASH_test_p=%s
shopt -s nullglob; fqfiles=(%s/processed/*.fastq*) 
                                     
                                        '''%(QC_out, QC_out,flash_p,QC_out))
                                else:
                                        cmd_file.write('''
echo "### Progress ### FLASH merging\n" >> %s/QC_log.txt;
mkdir %s/QCdata/FLASH_test_p=%s
mkdir %s/QCdata/FLASH_test_p=%s/trimmed_%s

%s dynamictrim -p %s -d %s/QCdata/FLASH_test_p=%s/trimmed_%s %s/processed/*.fastq*
rm -r %s/QCdata/FLASH_test_p=%s/trimmed_%s/*trimmed.segments*
shopt -s nullglob; fqfiles=(%s/QCdata/FLASH_test_p=%s/trimmed_%s/*.fastq.trimmed*) 
                                        
                                        '''%(QC_out, QC_out,flash_p,QC_out,flash_p,flash_p,
                                             self.programs_list["SolexaQA++"]['path'],flash_p,QC_out,flash_p,flash_p, QC_out,
                                             QC_out,flash_p,flash_p,
                                             QC_out,flash_p,flash_p))
                                        
                                cmd_file.write('''
readarray -t sorted < <(printf '%%s\\0' "${fqfiles[@]}" | sort -z | xargs -0n1)
for ((i=0; i<${#fqfiles[@]} ; i=i+2)); 
do
%s -To -o $(basename "${fqfiles[i]}") -d %s/QCdata/FLASH_test_p=%s -M 300 -t 16 "${fqfiles[i]}" "${fqfiles[i+1]}" --cap-mismatch-quals 2>&1 | tee -a %s/QCdata/FLASH_test_p=%s/FullFLASHlog.txt                                       
done 

%s  %s/QCdata/FLASH_test_p=%s/FullFLASHlog.txt > %s/QCdata/FLASH_test_p=%s/Flash_table.csv

if [ -d '%s/QCdata/FLASH_test_p=%s/trimmed_%s/' ]; then
    rm -r %s/QCdata/FLASH_test_p=%s/trimmed_%s
fi

                                        '''%(self.programs_list["Amplicons FLASH test"]['path_FLASH'], QC_out,flash_p,QC_out,flash_p,
                                             self.programs_list["Amplicons FLASH test"]['log_parser_path'], QC_out,flash_p,QC_out,flash_p,
                                             QC_out,flash_p,flash_p,QC_out,flash_p,flash_p))
                                
                                
                                
####### Reads trimming #####################################
              
                if 'Reads trimming' in selected_progs:
                        if 'PhiX and adapters removal' in selected_progs:
                                cmd_file.write('''
echo "### Progress ### Trimming\n" >> %s/QC_log.txt;
mkdir %s/processed_trimmed
for file in %s/processed/*.fastq*; do %s dynamictrim -d %s/processed_trimmed/ -p %s "$file" 2>&1 | tee -a %s/QC_log.txt; done                        
rm -r %s/processed_trimmed/*.segments*
cd %s; for file in processed_trimmed/*.fastq*; do md5sum "$file" >> %s/processed_trimmed/md5checksums.txt; done
cd $maindir                         
                                '''%(QC_out, QC_out,QC_out,self.programs_list["Reads trimming"]['path'], QC_out,trim_p, QC_out, QC_out, QC_out, QC_out))                               
                        else:
                                cmd_file.write('''
echo "### Progress ### Trimming\n" >> %s/QC_log.txt;
mkdir %s/fQsequences_trimmed
for file in %s/fQsequences/*.fastq*; do %s dynamictrim -d %s/fQsequences_trimmed/ -p %s "$file" 2>&1 | tee -a %s/QC_log.txt; done
rm -r %s/fQsequences_trimmed/*.segments*
cd %s; for file in fQsequences_trimmed/*.fastq*; do md5sum "$file" >> %s/fQsequences_trimmed/md5checksums.txt; done
cd $maindir
                        
                                                        '''%(QC_out, QC_out,QC_out,self.programs_list["Reads trimming"]['path'], QC_out,trim_p,QC_out, QC_out, QC_out, QC_out))                                   
                                

####### GC content #####################################

                if 'GC content' in selected_progs:
                        cmd_file.write('''
echo "### Progress ### GC content" >> %s/QC_log.txt;
mkdir %s/QCdata/GC_content
for file in %s/fQsequences/*.fastq*;do
	if [[ $file !=  *"Undetermined"* ]];then
		/usr/bin/python %s "$file" %s/QCdata/GC_content; Rscript %s/QCdata/GC_content/rgraph.R; rm -rf %s/QCdata/GC_content/rgraph.R;
	fi
done
                        '''%(QC_out, QC_out, QC_out, self.programs_list["GC content"]['path'], QC_out, QC_out, QC_out))
                        
                if ('GC content' in selected_progs and 'Amplicons FLASH test' in selected_progs):
                                cmd_file.write('''
for file in %s/fQsequences/subsamples/*.fastq*;do
	/usr/bin/python %s "$file" %s/images/; Rscript %s/images/rgraph.R; rm -rf %s/images/rgraph.R;
done			
'''%(QC_out, self.programs_list["GC content"]['path'], QC_out, QC_out, QC_out))
                                
                elif ('GC content' in selected_progs and not 'Amplicons FLASH test' in selected_progs):
                                cmd_file.write('''
cp `ls %s/QCdata/GC_content/*.pdf | head -2` %s/images
'''%(QC_out, QC_out))                                

##########################


                cmd_file.write('''
cd %s; find ./ -name md5checksums.txt | while read line; do echo "md5sum -c $line" >> checksum.sh; done; chmod +x checksum.sh
cd %s/images/
cd $maindir
echo "Completed QC analysis on $(date '+%%a %%b %%d %%H:%%M:%%S %%Y')" >> %s/checkPoint2done.txt
rm -r %s/%s.txt
rm -rf %s/fQsequences/subsamples
rm -rf %s
                '''%(QC_out, QC_out, QC_out,  homedir, folder.split('/')[-1], QC_out, TMPDIR))                                
                cmd_file.close()
                
                if os.path.exists('%s'%QC_out):
                        QtGui.QMessageBox.critical(self, "Problem","Output folder already exists. Rename/remove and try again.")
                else:
                        os.system("mkdir -p %s; touch %s/checkPoint1done.txt"%(QC_out,QC_out))
                        if node=='Auto' or node!='Auto':		
				proc = subprocess.Popen(['bash', cmd_file.name], shell=False)
				JobID = proc.pid # <--- access `pid` attribute to get the pid of the child process.
				#Cluster option
                                #JobID=getoutput('bsub -o /%s/%%J.stdout -e /%s/%%J.stderr %s'%(QC_out,QC_out,cmd_file.name)).split("Job <")[1].split(">")[0] ## -m com003.geno chooses the cluster
                        #else:
			#	JobID='001'
			#	os.system('%s'%cmd_file.name)				
                                #JobID=getoutput('bsub -m "%s.geno" -o /%s/%%J.stdout -e /%s/%%J.stderr %s'%(node,QC_out,QC_out,cmd_file.name)).split("Job <")[1].split(">")[0] ## -m chooses the cluster

                        os.system("echo 'Run QC started as JOB %s' >> %s/QC_log.txt"%(JobID, QC_out))
     
        def list_programs(self):
                programs=self.Config["EXECUTABLES AND OPTIONS"]
                return programs

        def ConfigSectionMap(self, section):
                dict1 = OrderedDict()
                options = self.Config.options(section)
                for option in options:
                        try:
                                dict1[option] = self.Config.get(section, option)
                                if dict1[option] == -1:
                                        DebugPrint("skip: %s" % option)
                        except:
                                print("exception on %s!" % option)
                                dict1[option] = None
                return dict1   

        def closeEvent(self, event):
                event.accept() 
                sys.exit()

def print_help():
        print "HELP"
        return
        
        
if __name__ == "__main__":
        if os.path.exists("log.txt"):
                os.system("rm log.txt")
                
        logging.basicConfig(
                level=logging.DEBUG,
                format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
                filename="log.txt",
                filemode='a'
        )
        
        stdout_logger = logging.getLogger('STDOUT')
        sl = StreamToLogger(stdout_logger, logging.INFO)
        sys.stdout = sl
        
        stderr_logger = logging.getLogger('STDERR')
        sl = StreamToLogger(stderr_logger, logging.ERROR)
        sys.stderr = sl                
        app = QtGui.QApplication(sys.argv)
        form = FORM()
        form.show()

        timer = QtCore.QTimer()
        timer.timeout.connect(form.updatetable)
        timer.start(500)	
        sys.exit(app.exec_())
                


# sorting and iteration over pairs in bash: 
#readarray -t sorted < <(printf '%s\0' "${array[@]}" | sort -z | xargs -0n1)
#for ((i=0; i<=${#fqfiles[@]} ; i=i+2)); do %s --conf %s --outdir %s/QCdata/FastQScreen/  "${fqfiles[i]}" "${fqfiles[i+1]}"; done
