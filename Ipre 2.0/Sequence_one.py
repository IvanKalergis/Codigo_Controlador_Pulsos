# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'General_Pulses.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from pyqtgraph import PlotWidget


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(906, 703)
        self.Sequence_Creation = QGroupBox(Form)
        self.Sequence_Creation.setObjectName(u"Sequence_Creation")
        self.Sequence_Creation.setGeometry(QRect(20, 0, 1021, 711))
        self.horizontalLayoutWidget = QWidget(self.Sequence_Creation)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(20, 30, 347, 51))
        self.horizontalLayout_5 = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_6 = QLabel(self.horizontalLayoutWidget)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_5.addWidget(self.label_6)

        self.Loop_Sequence = QSpinBox(self.horizontalLayoutWidget)
        self.Loop_Sequence.setObjectName(u"Loop_Sequence")

        self.horizontalLayout_5.addWidget(self.Loop_Sequence)

        self.Run_Sequence = QPushButton(self.horizontalLayoutWidget)
        self.Run_Sequence.setObjectName(u"Run_Sequence")

        self.horizontalLayout_5.addWidget(self.Run_Sequence)

        self.Stop_Sequence = QPushButton(self.horizontalLayoutWidget)
        self.Stop_Sequence.setObjectName(u"Stop_Sequence")

        self.horizontalLayout_5.addWidget(self.Stop_Sequence)

        self.groupBox_2 = QGroupBox(self.Sequence_Creation)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(20, 80, 851, 321))
        self.Sequence_Diagram = PlotWidget(self.groupBox_2)
        self.Sequence_Diagram.setObjectName(u"Sequence_Diagram")
        self.Sequence_Diagram.setGeometry(QRect(10, 60, 831, 221))
        self.current_iteration_2 = QLabel(self.groupBox_2)
        self.current_iteration_2.setObjectName(u"current_iteration_2")
        self.current_iteration_2.setGeometry(QRect(10, 30, 201, 19))
        self.Iteration_frame = QSpinBox(self.groupBox_2)
        self.Iteration_frame.setObjectName(u"Iteration_frame")
        self.Iteration_frame.setGeometry(QRect(190, 30, 91, 24))
        self.horizontalLayoutWidget_3 = QWidget(self.groupBox_2)
        self.horizontalLayoutWidget_3.setObjectName(u"horizontalLayoutWidget_3")
        self.horizontalLayoutWidget_3.setGeometry(QRect(520, 20, 321, 41))
        self.horizontalLayout_14 = QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.Stop_Simulation = QPushButton(self.horizontalLayoutWidget_3)
        self.Stop_Simulation.setObjectName(u"Stop_Simulation")
        self.Stop_Simulation.setMaximumSize(QSize(111, 32))

        self.horizontalLayout_14.addWidget(self.Stop_Simulation)

        self.Update = QPushButton(self.horizontalLayoutWidget_3)
        self.Update.setObjectName(u"Update")
        self.Update.setMaximumSize(QSize(121, 32))

        self.horizontalLayout_14.addWidget(self.Update)

        self.horizontalLayoutWidget_2 = QWidget(self.groupBox_2)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(310, 20, 211, 41))
        self.horizontalLayout_13 = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.label_14 = QLabel(self.horizontalLayoutWidget_2)
        self.label_14.setObjectName(u"label_14")

        self.horizontalLayout_13.addWidget(self.label_14)

        self.ms = QSpinBox(self.horizontalLayoutWidget_2)
        self.ms.setObjectName(u"ms")
        self.ms.setMaximumSize(QSize(111, 24))

        self.horizontalLayout_13.addWidget(self.ms)

        self.current_iteration = QLabel(self.groupBox_2)
        self.current_iteration.setObjectName(u"current_iteration")
        self.current_iteration.setGeometry(QRect(20, 290, 158, 19))
        self.Duration_Loop = QLabel(self.groupBox_2)
        self.Duration_Loop.setObjectName(u"Duration_Loop")
        self.Duration_Loop.setGeometry(QRect(660, 290, 161, 19))
        self.Define_Pulse = QGroupBox(self.Sequence_Creation)
        self.Define_Pulse.setObjectName(u"Define_Pulse")
        self.Define_Pulse.setGeometry(QRect(480, 400, 391, 291))
        self.verticalLayoutWidget = QWidget(self.Define_Pulse)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 30, 382, 261))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.StartTime = QDoubleSpinBox(self.verticalLayoutWidget)
        self.StartTime.setObjectName(u"StartTime")

        self.horizontalLayout.addWidget(self.StartTime)

        self.label_2 = QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.Puls_Width = QDoubleSpinBox(self.verticalLayoutWidget)
        self.Puls_Width.setObjectName(u"Puls_Width")

        self.horizontalLayout.addWidget(self.Puls_Width)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.Channel_Pulse = QComboBox(self.verticalLayoutWidget)
        self.Channel_Pulse.addItem("")
        self.Channel_Pulse.addItem("")
        self.Channel_Pulse.addItem("")
        self.Channel_Pulse.addItem("")
        self.Channel_Pulse.addItem("")
        self.Channel_Pulse.addItem("")
        self.Channel_Pulse.addItem("")
        self.Channel_Pulse.addItem("")
        self.Channel_Pulse.addItem("")
        self.Channel_Pulse.addItem("")
        self.Channel_Pulse.addItem("")
        self.Channel_Pulse.addItem("")
        self.Channel_Pulse.addItem("")
        self.Channel_Pulse.addItem("")
        self.Channel_Pulse.addItem("")
        self.Channel_Pulse.addItem("")
        self.Channel_Pulse.addItem("")
        self.Channel_Pulse.addItem("")
        self.Channel_Pulse.addItem("")
        self.Channel_Pulse.addItem("")
        self.Channel_Pulse.addItem("")
        self.Channel_Pulse.addItem("")
        self.Channel_Pulse.setObjectName(u"Channel_Pulse")

        self.horizontalLayout_3.addWidget(self.Channel_Pulse)


        self.horizontalLayout_2.addLayout(self.horizontalLayout_3)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_10 = QLabel(self.verticalLayoutWidget)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_11.addWidget(self.label_10)

        self.Pulses_box = QComboBox(self.verticalLayoutWidget)
        self.Pulses_box.setObjectName(u"Pulses_box")

        self.horizontalLayout_11.addWidget(self.Pulses_box)

        self.label_7 = QLabel(self.verticalLayoutWidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMaximumSize(QSize(51, 24))

        self.horizontalLayout_11.addWidget(self.label_7)

        self.Function = QLineEdit(self.verticalLayoutWidget)
        self.Function.setObjectName(u"Function")
        self.Function.setMaximumSize(QSize(71, 21))

        self.horizontalLayout_11.addWidget(self.Function)


        self.verticalLayout.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_11 = QLabel(self.verticalLayoutWidget)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMaximumSize(QSize(91, 16))

        self.horizontalLayout_9.addWidget(self.label_11)

        self.Iterations_start = QSpinBox(self.verticalLayoutWidget)
        self.Iterations_start.setObjectName(u"Iterations_start")

        self.horizontalLayout_9.addWidget(self.Iterations_start)

        self.label_12 = QLabel(self.verticalLayoutWidget)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMaximumSize(QSize(16, 24))

        self.horizontalLayout_9.addWidget(self.label_12)

        self.Iterations_end = QSpinBox(self.verticalLayoutWidget)
        self.Iterations_end.setObjectName(u"Iterations_end")
        self.Iterations_end.setMaximumSize(QSize(111, 24))

        self.horizontalLayout_9.addWidget(self.Iterations_end)


        self.verticalLayout.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer)

        self.label_13 = QLabel(self.verticalLayoutWidget)
        self.label_13.setObjectName(u"label_13")

        self.horizontalLayout_12.addWidget(self.label_13)

        self.Type_Change = QComboBox(self.verticalLayoutWidget)
        self.Type_Change.addItem("")
        self.Type_Change.addItem("")
        self.Type_Change.setObjectName(u"Type_Change")

        self.horizontalLayout_12.addWidget(self.Type_Change)


        self.verticalLayout.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.Add_Pulse = QPushButton(self.verticalLayoutWidget)
        self.Add_Pulse.setObjectName(u"Add_Pulse")
        self.Add_Pulse.setMaximumSize(QSize(85, 32))

        self.horizontalLayout_17.addWidget(self.Add_Pulse)


        self.verticalLayout.addLayout(self.horizontalLayout_17)

        self.Define_Channels_2 = QGroupBox(self.Sequence_Creation)
        self.Define_Channels_2.setObjectName(u"Define_Channels_2")
        self.Define_Channels_2.setGeometry(QRect(30, 400, 381, 281))
        self.Add_Channel = QPushButton(self.Define_Channels_2)
        self.Add_Channel.setObjectName(u"Add_Channel")
        self.Add_Channel.setGeometry(QRect(230, 240, 113, 32))
        self.Clear_Channels = QPushButton(self.Define_Channels_2)
        self.Clear_Channels.setObjectName(u"Clear_Channels")
        self.Clear_Channels.setGeometry(QRect(20, 240, 113, 32))
        self.Channel_List = QListWidget(self.Define_Channels_2)
        QListWidgetItem(self.Channel_List)
        self.Channel_List.setObjectName(u"Channel_List")
        self.Channel_List.setGeometry(QRect(20, 120, 331, 101))
        self.label_8 = QLabel(self.Define_Channels_2)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(10, 30, 61, 41))
        self.Delay_OFF = QDoubleSpinBox(self.Define_Channels_2)
        self.Delay_OFF.setObjectName(u"Delay_OFF")
        self.Delay_OFF.setGeometry(QRect(90, 40, 81, 24))
        self.label_4 = QLabel(self.Define_Channels_2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 70, 61, 41))
        self.Delay_ON = QDoubleSpinBox(self.Define_Channels_2)
        self.Delay_ON.setObjectName(u"Delay_ON")
        self.Delay_ON.setGeometry(QRect(90, 80, 81, 24))
        self.Type_Channel = QLineEdit(self.Define_Channels_2)
        self.Type_Channel.setObjectName(u"Type_Channel")
        self.Type_Channel.setGeometry(QRect(240, 80, 121, 21))
        self.label_5 = QLabel(self.Define_Channels_2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(180, 20, 88, 61))
        self.Channel_Identifier = QComboBox(self.Define_Channels_2)
        self.Channel_Identifier.addItem("")
        self.Channel_Identifier.addItem("")
        self.Channel_Identifier.addItem("")
        self.Channel_Identifier.addItem("")
        self.Channel_Identifier.addItem("")
        self.Channel_Identifier.addItem("")
        self.Channel_Identifier.addItem("")
        self.Channel_Identifier.addItem("")
        self.Channel_Identifier.addItem("")
        self.Channel_Identifier.addItem("")
        self.Channel_Identifier.addItem("")
        self.Channel_Identifier.addItem("")
        self.Channel_Identifier.addItem("")
        self.Channel_Identifier.addItem("")
        self.Channel_Identifier.addItem("")
        self.Channel_Identifier.addItem("")
        self.Channel_Identifier.addItem("")
        self.Channel_Identifier.addItem("")
        self.Channel_Identifier.addItem("")
        self.Channel_Identifier.addItem("")
        self.Channel_Identifier.addItem("")
        self.Channel_Identifier.addItem("")
        self.Channel_Identifier.setObjectName(u"Channel_Identifier")
        self.Channel_Identifier.setGeometry(QRect(240, 40, 131, 26))
        self.label_15 = QLabel(self.Define_Channels_2)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QRect(180, 60, 88, 61))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.Sequence_Creation.setTitle(QCoreApplication.translate("Form", u"Pulse Blaster Experiment", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"Loop: ", None))
        self.Run_Sequence.setText(QCoreApplication.translate("Form", u"Run", None))
        self.Stop_Sequence.setText(QCoreApplication.translate("Form", u"Stop", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"Frames", None))
        self.current_iteration_2.setText(QCoreApplication.translate("Form", u"Channels on each iteration: ", None))
        self.Stop_Simulation.setText(QCoreApplication.translate("Form", u"Play/Stop", None))
        self.Update.setText(QCoreApplication.translate("Form", u"Update", None))
        self.label_14.setText(QCoreApplication.translate("Form", u"ms per iteration:", None))
        self.current_iteration.setText(QCoreApplication.translate("Form", u"current iteration: ( )", None))
        self.Duration_Loop.setText(QCoreApplication.translate("Form", u"Duration: ( )", None))
        self.Define_Pulse.setTitle(QCoreApplication.translate("Form", u"Add pulse to sequence", None))
        self.label.setText(QCoreApplication.translate("Form", u"Start Time:", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Pulse Width", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Channel:", None))
        self.Channel_Pulse.setItemText(0, QCoreApplication.translate("Form", u"N", None))
        self.Channel_Pulse.setItemText(1, QCoreApplication.translate("Form", u"PB0", None))
        self.Channel_Pulse.setItemText(2, QCoreApplication.translate("Form", u"PB1", None))
        self.Channel_Pulse.setItemText(3, QCoreApplication.translate("Form", u"PB2", None))
        self.Channel_Pulse.setItemText(4, QCoreApplication.translate("Form", u"PB3", None))
        self.Channel_Pulse.setItemText(5, QCoreApplication.translate("Form", u"PB4", None))
        self.Channel_Pulse.setItemText(6, QCoreApplication.translate("Form", u"PB5", None))
        self.Channel_Pulse.setItemText(7, QCoreApplication.translate("Form", u"PB6", None))
        self.Channel_Pulse.setItemText(8, QCoreApplication.translate("Form", u"PB7", None))
        self.Channel_Pulse.setItemText(9, QCoreApplication.translate("Form", u"PB8", None))
        self.Channel_Pulse.setItemText(10, QCoreApplication.translate("Form", u"PB9", None))
        self.Channel_Pulse.setItemText(11, QCoreApplication.translate("Form", u"PB10", None))
        self.Channel_Pulse.setItemText(12, QCoreApplication.translate("Form", u"PB11", None))
        self.Channel_Pulse.setItemText(13, QCoreApplication.translate("Form", u"PB12", None))
        self.Channel_Pulse.setItemText(14, QCoreApplication.translate("Form", u"PB13", None))
        self.Channel_Pulse.setItemText(15, QCoreApplication.translate("Form", u"PB14", None))
        self.Channel_Pulse.setItemText(16, QCoreApplication.translate("Form", u"PB15", None))
        self.Channel_Pulse.setItemText(17, QCoreApplication.translate("Form", u"PB16", None))
        self.Channel_Pulse.setItemText(18, QCoreApplication.translate("Form", u"PB17", None))
        self.Channel_Pulse.setItemText(19, QCoreApplication.translate("Form", u"PB18", None))
        self.Channel_Pulse.setItemText(20, QCoreApplication.translate("Form", u"PB19", None))
        self.Channel_Pulse.setItemText(21, QCoreApplication.translate("Form", u"PB20", None))

        self.label_10.setText(QCoreApplication.translate("Form", u"Vary a pulse width:", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"f:(W*i)", None))
        self.Function.setText("")
        self.label_11.setText(QCoreApplication.translate("Form", u"Iteration from:", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"to", None))
        self.label_13.setText(QCoreApplication.translate("Form", u"Type:", None))
        self.Type_Change.setItemText(0, QCoreApplication.translate("Form", u"Add new pulse, with/without variations", None))
        self.Type_Change.setItemText(1, QCoreApplication.translate("Form", u"Vary an already added pulse", None))

        self.Add_Pulse.setText(QCoreApplication.translate("Form", u"Add", None))
        self.Define_Channels_2.setTitle(QCoreApplication.translate("Form", u"Define Channels", None))
        self.Add_Channel.setText(QCoreApplication.translate("Form", u"Add", None))
        self.Clear_Channels.setText(QCoreApplication.translate("Form", u"Clear", None))

        __sortingEnabled = self.Channel_List.isSortingEnabled()
        self.Channel_List.setSortingEnabled(False)
        ___qlistwidgetitem = self.Channel_List.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("Form", u"The added channels will be shown here", None));
        self.Channel_List.setSortingEnabled(__sortingEnabled)

        self.label_8.setText(QCoreApplication.translate("Form", u"Delay OFF:", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Delay ON:", None))
        self.Type_Channel.setText(QCoreApplication.translate("Form", u"green", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Channel:", None))
        self.Channel_Identifier.setItemText(0, QCoreApplication.translate("Form", u"N", None))
        self.Channel_Identifier.setItemText(1, QCoreApplication.translate("Form", u"PB0", None))
        self.Channel_Identifier.setItemText(2, QCoreApplication.translate("Form", u"PB1", None))
        self.Channel_Identifier.setItemText(3, QCoreApplication.translate("Form", u"PB2", None))
        self.Channel_Identifier.setItemText(4, QCoreApplication.translate("Form", u"PB3", None))
        self.Channel_Identifier.setItemText(5, QCoreApplication.translate("Form", u"PB4", None))
        self.Channel_Identifier.setItemText(6, QCoreApplication.translate("Form", u"PB5", None))
        self.Channel_Identifier.setItemText(7, QCoreApplication.translate("Form", u"PB6", None))
        self.Channel_Identifier.setItemText(8, QCoreApplication.translate("Form", u"PB7", None))
        self.Channel_Identifier.setItemText(9, QCoreApplication.translate("Form", u"PB8", None))
        self.Channel_Identifier.setItemText(10, QCoreApplication.translate("Form", u"PB9", None))
        self.Channel_Identifier.setItemText(11, QCoreApplication.translate("Form", u"PB10", None))
        self.Channel_Identifier.setItemText(12, QCoreApplication.translate("Form", u"PB11", None))
        self.Channel_Identifier.setItemText(13, QCoreApplication.translate("Form", u"PB12", None))
        self.Channel_Identifier.setItemText(14, QCoreApplication.translate("Form", u"PB13", None))
        self.Channel_Identifier.setItemText(15, QCoreApplication.translate("Form", u"PB14", None))
        self.Channel_Identifier.setItemText(16, QCoreApplication.translate("Form", u"PB15", None))
        self.Channel_Identifier.setItemText(17, QCoreApplication.translate("Form", u"PB16", None))
        self.Channel_Identifier.setItemText(18, QCoreApplication.translate("Form", u"PB17", None))
        self.Channel_Identifier.setItemText(19, QCoreApplication.translate("Form", u"PB18", None))
        self.Channel_Identifier.setItemText(20, QCoreApplication.translate("Form", u"PB19", None))
        self.Channel_Identifier.setItemText(21, QCoreApplication.translate("Form", u"PB20", None))

        self.label_15.setText(QCoreApplication.translate("Form", u"Type:", None))
    # retranslateUi

