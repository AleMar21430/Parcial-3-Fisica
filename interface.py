from qt import *
from math import *

global R1r, R1v, R1a, R2r, R2v, R2a, R3r, R3v, R3a, VGv, VGr, VSv, VSr, Ia1, Ia2
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
Ia1 = 0.0
Ia2 = 0.0

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
		self.Vgr = RCW_Float_Input_Slider("Vg Ω", 0, 1000, 1e3).setValue(VGr)

		self.Vs = RCW_Float_Input_Slider("Vs V", 0, 1000, 1e3).setValue(VSv)
		self.Vsr = RCW_Float_Input_Slider("Vs Ω", 0, 1000, 1e3).setValue(VSr)

		self.Linear_Layout.addWidget(self.R1)
		self.Linear_Layout.addWidget(self.R2)
		self.Linear_Layout.addWidget(self.R3)
		self.Linear_Layout.addWidget(self.Vg)
		self.Linear_Layout.addWidget(self.Vgr)
		self.Linear_Layout.addWidget(self.Vs)
		self.Linear_Layout.addWidget(self.Vsr)

		self.R1.Input.valueChanged.connect(self.updateSimulationValues)
		self.R2.Input.valueChanged.connect(self.updateSimulationValues)
		self.R3.Input.valueChanged.connect(self.updateSimulationValues)
		self.Vg.Input.valueChanged.connect(self.updateSimulationValues)
		self.Vs.Input.valueChanged.connect(self.updateSimulationValues)
		self.Vgr.Input.valueChanged.connect(self.updateSimulationValues)
		self.Vsr.Input.valueChanged.connect(self.updateSimulationValues)

	def updateSimulationValues(self):
		global R1r, R1v, R1a, R2r, R2v, R2a, R3r, R3v, R3a, VGv, VGr, VSv, VSr, Ia1, Ia2
		R1r = self.R1.Input.value()  / 1e3
		R2r = self.R2.Input.value()  / 1e3
		R3r = self.R3.Input.value()  / 1e3
		VGv = self.Vg.Input.value()  / 1e3
		VGr = self.Vgr.Input.value() / 1e3
		VSv = self.Vs.Input.value()  / 1e3
		VSr = self.Vsr.Input.value() / 1e3

		# Malla 1: -(R1 + R2)* i1 + R2 * i2 = Vg
		# Malla 2: R2 * i1 - (R3 + R2) * I2 = -Vs
		#https://quickmath.com/webMathematica3/quickmath/equations/solve/advanced.jsp#c=solve_solveequationsadvanced&v1=-%2528x%2By%2529*i%2By*j%2520%253D%2520V%250Ay*i-%2528z%2By%2529*j%2520%2520%253D-W&v2=i%250Aj
		Ia1 = round( -(VGv * R2r + (VGv - VSv) * R2r) / (R2r * (R3r + R1r) + R1r * R2r) , 3)
		Ia2 = round( -((VGv - VSv) * R2r - VSv * R1r) / (R2r * (R3r + R1r) + R1r * R2r) , 3)
		R1a = round( Ia1       , 3)
		R2a = round( Ia1 - Ia2 , 3)
		R3a = round( Ia2       , 3)
		R1v = round( R1r * R1a , 3)
		R2v = round( R2r * R2a , 3)
		R3v = round( R3r * R3a , 3)

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

		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 350, self.mapFromScene(0,0).y() + 300),
			f"{Ia1}  A"
		)
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 880, self.mapFromScene(0,0).y() + 300),
			f"{Ia2}  A"
		)

		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 350, self.mapFromScene(0,0).y() + 100),
			f"{R1r}  Ω"
		)
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 750, self.mapFromScene(0,0).y() + 450),
			f"{R2r}  Ω"
		)
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 880, self.mapFromScene(0,0).y() + 100),
			f"{R3r}  Ω"
		)
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 250, self.mapFromScene(0,0).y() + 450),
			f"{VGv}  V"
		)
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 1200, self.mapFromScene(0,0).y() + 450),
			f"{VSv}  V"
		)

		painter.setFont(QFont("Mono", 13))
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 350, self.mapFromScene(0,0).y() + 70),
			f"{R1v}  V"
		)
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 750, self.mapFromScene(0,0).y() + 420),
			f"{R2v}  V"
		)
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 880, self.mapFromScene(0,0).y() + 70),
			f"{R3v}  V"
		)
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 250, self.mapFromScene(0,0).y() + 420),
			f"{VGr}  Ω"
		)
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 1200, self.mapFromScene(0,0).y() + 420),
			f"{VSr}  Ω"
		)

		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 350, self.mapFromScene(0,0).y() + 50),
			f"{R1a}  A"
		)
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 750, self.mapFromScene(0,0).y() + 400),
			f"{R2a}  A"
		)
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 880, self.mapFromScene(0,0).y() + 50),
			f"{R3a}  A"
		)
		super().paint(painter, option, widget)