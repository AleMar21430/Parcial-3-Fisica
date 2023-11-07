from interface import *
import sys

class Window (RW_Window):
	def __init__(self, App: RW_Application):
		super().__init__()

		Items = open("Style_Settings.txt", encoding="utf-8-sig").read()
		Styles = Items.split("+")
		self.Style = ""
		for Style in Styles:
			Data = Style.split("\n", 1)
			self.Style += "\n" + Data[1]
		self.Style = self.Style[1:]
		App.setStyleSheet(self.Style)

		self.setWindowTitle("Parcial 3")

Application = RW_Application(sys.argv)
Main_Window = Window(Application)
Main_Window.setCentralWidget(R_Workspace_Image_Canvas())
Main_Window.showMaximized()
Application.exec()