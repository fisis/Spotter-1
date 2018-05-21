# # -*- coding: utf-8 -*-
# """
# Created on Sun Jan 18 21:13:54 2013
# @author: <Ronny Eichler> ronny.eichler@gmail.com
#
#
# """
# import logging
#
# from PyQt4 import QtGui
# from PyQt4 import QtCore
# from tab_sourceUi import Ui_tab_source
# import lib.core.grabber as grab
#
#
# class Tab(QtGui.QWidget, Ui_tab_source):
#
#     label = None
#     serial = None
#     accept_events = False
#     tab_type = "source"
#
#     def __init__(self, source_ref, label=None, *args, **kwargs):
#         QtGui.QWidget.__init__(self)
#         self.log = logging.getLogger(__name__)
#         self.setupUi(self)
#         self.source = source_ref
#
#         assert 'spotter' in kwargs
#         self.spotter = kwargs['spotter']
#
#         self.label = "Source"
#
#         assert 'update_all_tabs' in kwargs
#         self.refresh_sidebar = kwargs['update_all_tabs']
#         self.connect( self.SaveBtn , QtCore.SIGNAL('clicked ()'), self.save_prop)
#         self.connect( self.ResetBtn , QtCore.SIGNAL('clicked ()'), self.reset_prop)
#
#         #self.update()
#
#     def reset_prop(self):
#         self.WidthInput.setValue(1280);
#         self.HeightInput.setValue(720);
#         self.FPSInput.setValue(60);
#         self.scaleInput.setValue(0.5);
#         #####################set the values in the frame too#############
#         grab.fps_default = self.FPSInput.value();
#         grab.size_default = (self.WidthInput.value(), self.HeightInput.value());
#         grab.scale = self.scaleInput.value();
#     def save_prop(self):
#         grab.fps_default=self.FPSInput.value();
#         grab.size_default=(self.WidthInput.value(), self.HeightInput.value());
#         grab.scale=self.scaleInput.value();
#         print('save')
#
#     def update(self):
#         pass
#         #if self.serial.is_connected():
#         #    if not self.btn_serial_connect.isChecked():
#         #        self.btn_serial_connect.setText('Disconnect')
#         #        self.btn_serial_connect.setChecked(True)
#         #    # Human readable values of bytes sent/received
#         #    tx = utils.binary_prefix(self.serial.bytes_tx())
#         #    rx = utils.binary_prefix(self.serial.bytes_rx())
#         #    self.lbl_bytes_sent.setText(tx)
#         #    self.lbl_bytes_received.setText(rx)
#         #else:
#         #    self.btn_serial_connect.setText('Connect')
#         #    self.btn_serial_connect.setChecked(False)
#
#     #def refresh_port_list(self):
#     #    """ Populates the list of available serial ports in the machine.
#     #    May not work under windows at all. Would then require the user to
#     #    provide the proper port. Either via command line or typing it into the
#     #    combobox.
#     #    """
#     #    candidate = None
#     #    for i in range(self.combo_serialports.count()):
#     #        self.combo_serialports.removeItem(0)
#     #    for p in utils.get_port_list():
#     #        if len(p) > 2 and "USB" in p[2]:
#     #            candidate = p
#     #        self.combo_serialports.addItem(p[0])
#     #    if candidate:
#     #        self.combo_serialports.setCurrentIndex(self.combo_serialports.findText(candidate[0]))
#
#     #def toggle_connection(self):
#     #    """
#     #    Toggle button to either connect or disconnect serial connection.
#     #    """
#     #    # This test is inverted. When the function is called the button is
#     #    # already pressed, i.e. checked -> representing future state, not past
#     #    if not self.btn_serial_connect.isChecked():
#     #        self.btn_serial_connect.setText('Connect')
#     #        self.btn_serial_connect.setChecked(False)
#     #        self.serial.close()
#     #        # FIXME: Missing! Connect signal to trigger
#     #        self.update_all_tabs()
#     #    else:
#     #        self.serial.serial_port = str(self.combo_serialports.currentText())
#     #        try:
#     #            sc = self.serial.auto_connect(self.serial.serial_port)
#     #        except Exception, e:
#     #            print e
#     #            self.btn_serial_connect.setChecked(False)
#     #            return
#     #        if sc:
#     #            self.btn_serial_connect.setText('Disconnect')
#     #            self.btn_serial_connect.setChecked(True)
#     #            # FIXME: Missing! Connect signal to trigger
#     #            self.update_all_tabs()
#
#     def closeEvent(self, QCloseEvent):
#         # Source tab shall be invincible!
#         return False