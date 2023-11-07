from qt import *
from math import *

global R1r, R1v, R1a, R2r, R2v, R2a, R3r, R3v, R3a, VGv, VGr, VSv, VSr
R1r = 1.0
R1v = 0.0
R1a = 0.0
R2r = 2.0
R2v = 0.0
R2a = 0.0
R3r = 3.0
R3v = 0.0
R3a = 0.0
VGv = 4.0
VGr = 0.0
VSv = 5.0
VSr = 0.0

class R_Image_Canvas_Scene(QGraphicsScene):
	def __init__(self):
		super().__init__()
		self.addPixmap(QPixmap("./Circuito.png"))
		self.addItem(Description())

class R_Workspace_Image_Canvas(RW_Splitter):
	def __init__(self):
		super().__init__(False)
		self.Restarting = True
		self.Mode = 0

		self.Scene = R_Image_Canvas_Scene()
		self.Viewport = R_Image_Canvas_Viewport()
		self.Viewport.setScene(self.Scene)
		self.Tools = R_Toolbar(self)

		self.addWidget(self.Tools)
		self.addWidget(self.Viewport)
		self.setSizes([500,1500])

		self.Tools.updateSimulationValues()
		self.Viewport.update()

class R_Toolbar(RW_Linear_Contents):
	def __init__(self, parent: R_Workspace_Image_Canvas):
		super().__init__(True)
		self.Parent = parent

		self.R1 = RCW_Float_Input_Slider("R1 Ω", 0, 1000, 1e3).setValue(R1r)
		self.R2 = RCW_Float_Input_Slider("R2 Ω", 0, 1000, 1e3).setValue(R2r)
		self.R3 = RCW_Float_Input_Slider("R3 Ω", 0, 1000, 1e3).setValue(R3r)
		self.Vg = RCW_Float_Input_Slider("Vg V", 0, 1000, 1e3).setValue(VGv)
		self.Vs = RCW_Float_Input_Slider("Vs V", 0, 1000, 1e3).setValue(VSv)

		self.Linear_Layout.addWidget(self.R1)
		self.Linear_Layout.addWidget(self.R2)
		self.Linear_Layout.addWidget(self.R3)
		self.Linear_Layout.addWidget(self.Vg)
		self.Linear_Layout.addWidget(self.Vs)

		self.R1.Input.valueChanged.connect(self.updateSimulationValues)
		self.R2.Input.valueChanged.connect(self.updateSimulationValues)
		self.R3.Input.valueChanged.connect(self.updateSimulationValues)
		self.Vg.Input.valueChanged.connect(self.updateSimulationValues)
		self.Vs.Input.valueChanged.connect(self.updateSimulationValues)

	def updateSimulationValues(self):
		global R1r, R1v, R1a, R2r, R2v, R2a, R3r, R3v, R3a, VGv, VGr, VSv, VSr
		R1r = self.R1.Input.value() / 1e3
		R2r = self.R2.Input.value() / 1e3
		R3r = self.R3.Input.value() / 1e3
		VGv = self.Vg.Input.value() / 1e3
		VSv = self.Vs.Input.value() / 1e3
		self.Parent.Viewport.update()

class R_Image_Canvas_Viewport(QGraphicsView):
	BG_Color = QColor(250,250,250)

	def __init__(self):
		super().__init__()
		self.Last_Pos_Pan = QPoint(0,0)
		self.Panning_View = False

	def drawBackground(self, painter, rect):
		painter.fillRect(rect, self.BG_Color)
		return super().drawBackground(painter, rect)

class Description(QGraphicsRectItem):
	def __init__(self):
		super().__init__(0,0,1500,600)

	def paint(self, painter, option, widget):
		painter.setPen(QPen(Qt.GlobalColor.black, 2))
		painter.setBrush(QBrush(Qt.GlobalColor.black))
		painter.setFont(QFont("Mono", 26))
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 350, self.mapFromScene(0,0).y() + 100),
			f"{R1r}Ω"
		)
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 750, self.mapFromScene(0,0).y() + 450),
			f"{R2r}Ω"
		)
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 900, self.mapFromScene(0,0).y() + 100),
			f"{R3r}Ω"
		)
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 250, self.mapFromScene(0,0).y() + 450),
			f"{VGv}V"
		)
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 1200, self.mapFromScene(0,0).y() + 450),
			f"{VSv}V"
		)

		painter.setFont(QFont("Mono", 13))
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 350, self.mapFromScene(0,0).y() + 70),
			f"{R1v}V"
		)
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 750, self.mapFromScene(0,0).y() + 420),
			f"{R2v}V"
		)
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 900, self.mapFromScene(0,0).y() + 70),
			f"{R3v}V"
		)
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 250, self.mapFromScene(0,0).y() + 420),
			f"{VGr}Ω"
		)
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 1200, self.mapFromScene(0,0).y() + 420),
			f"{VSr}Ω"
		)

		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 350, self.mapFromScene(0,0).y() + 50),
			f"{R1a}A"
		)
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 750, self.mapFromScene(0,0).y() + 400),
			f"{R2a}A"
		)
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 900, self.mapFromScene(0,0).y() + 50),
			f"{R3a}A"
		)
		super().paint(painter, option, widget)