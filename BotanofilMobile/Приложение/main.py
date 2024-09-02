from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import requests

from uipy.mainwindow import Ui_MainWindow
from uipy.widget import Ui_widget
from uipy.settings import Ui_Settings

import time
import os
import json
import threading

get_data = lambda id, password: requests.post('http://f0782959.xsph.ru/getdata.php', data={'id': id, 'password': password})

send_command = lambda id, password, command: requests.post('http://f0782959.xsph.ru/updatecommand.php', data={'id': id, 'password': password, 'command': command}) # on_water/off_water | on_light/off_light

update_settings = lambda id, password, settings: requests.post('http://f0782959.xsph.ru/updatesettings.php', data={'id': id, 'password': password, 'settings': settings})

class MainWindow_Win(Ui_MainWindow):
	def refresh_list(self):
		with open(file_path, "r", encoding='utf-8') as read_file:
			data = json.load(read_file)

		self.listWidget.clear()
		for i in data.keys():
			self.listWidget.addItem(i)

	def update_data(self, message=True):
		self.IdLabel.setText("Id: ")
		self.HumidityLabel.setText("Влажность почвы: ")
		self.CompoundLabel.setText("Минеральный состав почвы: ")

		r = get_data(self.select_item['id'], self.select_item['password'])

		try:
			r = r.json()
			self.r = r

			self.IdLabel.setText(f"Id: {self.select_item['id']}")
			self.HumidityLabel.setText(f"Влажность почвы: {r['Data']['hum']}")
			self.CompoundLabel.setText(f"Минеральный состав почвы: {r['Data']['com']}")

			if str(r['Commands']['Water']) == '1' or str(r['Commands']['Water']) == '2':
				self.pushButton.setStyleSheet('background-color: green; color: white')
			else:
				self.pushButton.setStyleSheet('background-color: red; color: white;')
			
			if str(r['Commands']['Light']) == '1' or str(r['Commands']['Light']) == '2':
				self.pushButton_2.setStyleSheet('background-color: green; color: white')
			else:
				self.pushButton_2.setStyleSheet('background-color: red; color: white')
		
		except requests.exceptions.JSONDecodeError:
			if message:
				msg = QMessageBox()
				msg.setIcon(QMessageBox.Information)	
				msg.setText("Неверный ID или пароль контроллера")
				msg.setWindowTitle("Ошибка подключения")
				msg.setStandardButtons(QMessageBox.Ok)
				retval = msg.exec_()

			raise requests.exceptions.ConnectionError

	def itemClicked_event(self, item):
		try:
			self.pushButton.setEnabled(False)
			self.pushButton_2.setEnabled(False)
			self.pushButton_3.setEnabled(False)
			self.editButton.setEnabled(True)
			self.deleteButton.setEnabled(True)

			self.select_item = self.data[item.text()]
			self.select_item_name = item.text()
			self.update_data()

			self.pushButton.setEnabled(True)
			self.pushButton_2.setEnabled(True)
			self.pushButton_3.setEnabled(True)
			self.editButton.setEnabled(True)
			self.deleteButton.setEnabled(True)

		except (requests.exceptions.JSONDecodeError, requests.exceptions.ConnectionError):
			self.pushButton.setEnabled(False)
			self.pushButton_2.setEnabled(False)
			self.pushButton_3.setEnabled(False)
			self.editButton.setEnabled(True)
			self.deleteButton.setEnabled(True)
	
	def water_button(self):
		try:
			if str(self.r['Commands']['Water']) == '1' or str(self.r['Commands']['Water']) == '2':
				r = send_command(self.select_item['id'], self.select_item['password'], 'off_water')
			else:
				r = send_command(self.select_item['id'], self.select_item['password'], 'on_water_admin')

			self.pushButton.setEnabled(False)
			self.pushButton_2.setEnabled(False)
			self.pushButton_3.setEnabled(False)
			self.editButton.setEnabled(True)
			self.deleteButton.setEnabled(True)

			self.update_data()

			self.pushButton.setEnabled(True)
			self.pushButton_2.setEnabled(True)
			self.pushButton_3.setEnabled(True)
			self.editButton.setEnabled(True)
			self.deleteButton.setEnabled(True)
		
		except (requests.exceptions.JSONDecodeError, requests.exceptions.ConnectionError):
			self.pushButton.setEnabled(False)
			self.pushButton_2.setEnabled(False)
			self.pushButton_3.setEnabled(False)
			self.editButton.setEnabled(True)
			self.deleteButton.setEnabled(True)
	
	def light_button(self):
		try:
			if str(self.r['Commands']['Light']) == '1' or str(self.r['Commands']['Light']) == '2':
				r = send_command(self.select_item['id'], self.select_item['password'], 'off_light')
			else:
				r = send_command(self.select_item['id'], self.select_item['password'], 'on_light_admin')

			self.pushButton.setEnabled(False)
			self.pushButton_2.setEnabled(False)
			self.pushButton_3.setEnabled(False)
			self.editButton.setEnabled(True)
			self.deleteButton.setEnabled(True)

			self.update_data()

			self.pushButton.setEnabled(True)
			self.pushButton_2.setEnabled(True)
			self.pushButton_3.setEnabled(True)
			self.editButton.setEnabled(True)
			self.deleteButton.setEnabled(True)

		except (requests.exceptions.JSONDecodeError, requests.exceptions.ConnectionError):
			self.pushButton.setEnabled(False)
			self.pushButton_2.setEnabled(False)
			self.pushButton_3.setEnabled(False)
			self.editButton.setEnabled(True)
			self.deleteButton.setEnabled(True)
	
	def add_button(self):
		global widget
		global wid_ui

		widget = QtWidgets.QWidget()
		wid_ui = Add_Win()
		wid_ui.setupUi(widget)
		widget.show()
	
	def edit(self):
		global edit_ui
		global edit_win
		
		edit_win = QtWidgets.QWidget()
		edit_ui = Edit_Win()
		edit_ui.setupUi(edit_win, self.select_item, self.select_item_name)
		edit_win.show()
	
	def delete(self):
		del data[self.select_item_name]

		with open(file_path, "w+", encoding='utf-8') as write_file:
			json.dump(data, write_file)
		
		self.refresh_list()
	
	def open_settings(self):
		self.update_data()

		global settings_ui
		global settings_win

		settings_win = QtWidgets.QWidget()
		settings_ui = Settings_Ui()
		settings_ui.setupUi(settings_win, self.r['Settings'])
		settings_win.show()

class Add_Win(Ui_widget):
	def cancel(self):
		widget.hide()
	
	def add(self):
		name = self.nameLineEdit.text()
		id = self.IDLineEdit.text()
		password = self.passLineEdit.text()

		data[name] = {}
		data[name]['id'] = id
		data[name]['password'] = password

		with open(file_path, "w+", encoding='utf-8') as write_file:
			json.dump(data, write_file)
		
		widget.hide()
		main_ui.refresh_list()

class Edit_Win(Ui_widget):
	def cancel(self):
		edit_win.hide()
	
	def setupUi(self, widget, data, name):
		super().setupUi(widget)

		self.select_name = name

		self.nameLineEdit.setText(name)
		self.IDLineEdit.setText(data['id'])
		self.passLineEdit.setText(data['password'])

		_translate = QtCore.QCoreApplication.translate
		widget.setWindowTitle(_translate("widget", "Изменить контроллер"))
		self.AddButton.setText(_translate("widget", "Изменить"))

	def add(self):
		name = self.nameLineEdit.text()
		id = self.IDLineEdit.text()
		password = self.passLineEdit.text()
		
		del data[self.select_name]

		data[name] = {}
		data[name]['id'] = id
		data[name]['password'] = password

		with open(file_path, "w+", encoding='utf-8') as write_file:
			json.dump(data, write_file)
		
		edit_win.hide()
		main_ui.refresh_list()

class Settings_Ui(Ui_Settings):
	def cancel(self):
		settings_win.hide()
	
	def save(self):
		super().save()

		water = self.get_data_from_table(self.tableWidget)
		light = self.get_data_from_table(self.tableWidget_light)

		json_ = '{"Water": {"time": ' + str(water) + ', "value": ' + str(self.spinBox.value()) + '}, "Light": ' + str(light) + '}'

		while "'" in json_:
			json_ = json_.replace("'", '"')

		r = update_settings(main_ui.select_item['id'], 'admin', json_)


		settings_win.hide()

def auto_refresh():
	while True:
		try:
			main_ui.update_data(False)

			time.sleep(30)
		except:
			time.sleep(5)

if __name__ == "__main__":
	file_path = './controllers.json'

	if not(os.path.exists(file_path)):
		data = {}
		with open(file_path, "w+", encoding='utf-8') as write_file:
			json.dump(data, write_file)

	with open(file_path, "r", encoding='utf-8') as read_file:
		data = json.load(read_file)
	
	import sys
	app = QtWidgets.QApplication(sys.argv)

	MainWindow = QtWidgets.QMainWindow()
	main_ui = MainWindow_Win()
	main_ui.setupUi(MainWindow, data)

	auto_refresh_process = threading.Thread(target=auto_refresh, daemon=True)
	auto_refresh_process.start()

	MainWindow.show()

	sys.exit(app.exec_())
