from qt import *
from math import *
import time

def resistance_to_colors(resistance_ohms):
	color_codes = {
		0: Qt.GlobalColor.black,   # Black
		1: QColor(139, 69, 19),    # Brown
		2: Qt.GlobalColor.red,     # Red
		3: QColor(255, 165, 0),    # Orange
		4: Qt.GlobalColor.yellow,  # Yellow
		5: Qt.GlobalColor.green,   # Green
		6: Qt.GlobalColor.blue,    # Blue
		7: QColor(255, 0, 144),    # Violet
		8: Qt.GlobalColor.gray,    # Gray
		9: Qt.GlobalColor.white    # White
	}

	tolerance_code = {
		1: QColor(139, 69, 19),   # Brown  (±1%)
		2: Qt.GlobalColor.red,    # Red    (±2%)
		3: Qt.GlobalColor.green,  # Green  (±0.5%)
		4: Qt.GlobalColor.blue,   # Blue   (±0.25%)
		5: QColor(255, 0, 144),   # Violet (±0.1%)
		6: Qt.GlobalColor.gray    # Gray   (±0.05%)
	}

	number = str(resistance_ohms)
	mult = int(number.find("."))
	if mult < 2:
		color_band1 = color_codes[0]
		color_band2 = color_codes[int(number[0])]
	else:
		color_band1 = color_codes[int(number[0])]
		color_band2 = color_codes[int(number[1])]

	color_band3 = color_codes[mult]
	color_band4 = tolerance_code[2]

	return [color_band1, color_band2, color_band3, color_band4]


global R1r, R1v, R1a, R2r, R2v, R2a, R3r, R3v, R3a, VGv, VGr, VSv, VSr, Ia1, Ia2, P1, P2, P3, Pg, Ps, R1p, R2p, R3p
R1r = 0
R1v = 0
R1a = 0
R2r = 0
R2v = 0
R2a = 0
R3r = 0
R3v = 0
R3a = 0
VGv = 0
VGr = 0
VSv = 0
VSr = 0
Ia1 = 0
Ia2 = 0
P1 = 0
P2 = 0
P3 = 0
Pg = 0
Ps = 0
R1p = 0.25
R2p = 0.25
R3p = 0.25

def map_in_range(value, in_min, in_max, out_min, out_max):
	value = max(min(value, in_max), in_min)
	in_range = in_max - in_min
	out_range = out_max - out_min
	mapped_value = (value - in_min) * out_range / in_range + out_min
	return mapped_value

class R_Image_Canvas_Scene(QGraphicsScene):
	def __init__(self):
		super().__init__()
		self.addPixmap(QPixmap("./Circuito.png"))
		self.Items = Description()
		self.addItem(self.Items)

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
		self.last_time = time.time()

		self.update_timer = QTimer()
		self.update_timer.timeout.connect(self.tick)
		self.update_timer.start(1000 / 30)
	
	def tick(self):
		current_time = time.time()
		delta = current_time - self.last_time
		self.last_time = current_time
		self.Scene.Items.t1 += delta * VGv / 1000
		self.Scene.Items.t2 += delta * VSv / 1000
		self.Scene.update()

class R_Toolbar(RW_Linear_Contents):
	def __init__(self, parent: R_Workspace_Image_Canvas):
		super().__init__(True)
		self.Parent = parent

		self.R1 = RCW_Float_Input_Slider("R1 Ω", 0, 1000, 1e3).setValue(R1r)
		self.R2 = RCW_Float_Input_Slider("R2 Ω", 0, 1000, 1e3).setValue(R2r)
		self.R3 = RCW_Float_Input_Slider("R3 Ω", 0, 1000, 1e3).setValue(R3r)
		self.Vg = RCW_Float_Input_Slider("Vg V", 0, 1000, 1e3).setValue(VGv)
		self.Vs = RCW_Float_Input_Slider("Vs V", 0, 1000, 1e3).setValue(VSv)

		self.Vgr = RCW_Float_Input_Slider("Vg Ω", 0, 1000, 1e3).setValue(VGr)
		self.Vsr = RCW_Float_Input_Slider("Vs Ω", 0, 1000, 1e3).setValue(VSr)

		R1P_button = RW_Option()
		R1P_button.addItem("1/4 W")
		R1P_button.addItem("1/2 W")
		R1P_button.addItem("1   W")
		R1P_button.addItem("2   W")
		
		R2P_button = RW_Option()
		R2P_button.addItem("1/4 W")
		R2P_button.addItem("1/2 W")
		R2P_button.addItem("1   W")
		R2P_button.addItem("2   W")

		R3P_button = RW_Option()
		R3P_button.addItem("1/4 W")
		R3P_button.addItem("1/2 W")
		R3P_button.addItem("1   W")
		R3P_button.addItem("2   W")
		
		self.Linear_Layout.addWidget(self.R1)
		self.Linear_Layout.addWidget(R1P_button)
		self.Linear_Layout.addWidget(self.R2)
		self.Linear_Layout.addWidget(R2P_button)
		self.Linear_Layout.addWidget(self.R3)
		self.Linear_Layout.addWidget(R3P_button)
		self.Linear_Layout.addWidget(self.Vg)
		self.Linear_Layout.addWidget(self.Vs)
		#self.Linear_Layout.addWidget(self.Vgr)
		#self.Linear_Layout.addWidget(self.Vsr)
		
		R1P_button.currentIndexChanged.connect(lambda: self.updatePotency("R1p", R1P_button.currentText()))
		R2P_button.currentIndexChanged.connect(lambda: self.updatePotency("R2p", R2P_button.currentText()))
		R3P_button.currentIndexChanged.connect(lambda: self.updatePotency("R3p", R3P_button.currentText()))

		self.R1.Input.valueChanged.connect(self.updateSimulationValues)
		self.R2.Input.valueChanged.connect(self.updateSimulationValues)
		self.R3.Input.valueChanged.connect(self.updateSimulationValues)
		self.Vg.Input.valueChanged.connect(self.updateSimulationValues)
		self.Vs.Input.valueChanged.connect(self.updateSimulationValues)
		self.Vgr.Input.valueChanged.connect(self.updateSimulationValues)
		self.Vsr.Input.valueChanged.connect(self.updateSimulationValues)

	def updatePotency(self, variable, text: str):
		global R1p, R2p, R3p
		if   variable == "R1p":
			if text.startswith("1/4"):   R1p = 0.25
			elif text.startswith("1/2"): R1p = 0.5
			elif text.startswith("1"):   R1p = 1
			elif text.startswith("2"):   R1p = 2
		elif variable == "R2p":
			if text.startswith("1/4"):   R2p = 0.25
			elif text.startswith("1/2"): R2p = 0.5
			elif text.startswith("1"):   R2p = 1
			elif text.startswith("2"):   R2p = 2
		elif variable == "R3p":
			if text.startswith("1/4"):   R3p = 0.25
			elif text.startswith("1/2"): R3p = 0.5
			elif text.startswith("1"):   R3p = 1
			elif text.startswith("2"):   R3p = 2

		#self.Parent.Viewport.update()

	def updateSimulationValues(self):
		global R1r, R1v, R1a, R2r, R2v, R2a, R3r, R3v, R3a, VGv, VGr, VSv, VSr, Ia1, Ia2, P1, P2, P3, Pg, Ps
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
		try: Ia1 = round( abs(-(VGv * R2r + (VGv - VSv) * R2r) / (R2r * (R3r + R1r) + R1r * R2r)), 3)
		except: pass
		try: Ia2 = round( abs(-((VGv - VSv) * R2r - VSv * R1r) / (R2r * (R3r + R1r) + R1r * R2r)) , 3)
		except: pass
		R1a = round( Ia1       , 3)
		R2a = round( Ia1 - Ia2 , 3)
		R3a = round( Ia2       , 3)
		R1v = round( R1r * R1a , 3)
		R2v = round( R2r * R2a , 3)
		R3v = round( R3r * R3a , 3)

		P1 = round( R1a * R1a * R1r , 3)
		P2 = round( R2a * R2a * R2r , 3)
		P3 = round( R3a * R3a * R3r , 3)
		Pg = round( Ia1 * VGv , 3)
		Ps = round( Ia2 * VSv , 3)

		#self.Parent.Viewport.update()

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
		self.t1 = 0
		self.t2 = 0
		self.Particle1 = QPoint(182,136)
		self.Particle2 = QPoint(676,136)

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
		if P1 > R1p * Pg: painter.setPen(QPen(Qt.GlobalColor.red, 2))
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 350, self.mapFromScene(0,0).y() + 100),
			f"{R1r}  Ω"
		)
		if P1 > R1p * Pg: painter.setPen(QPen(Qt.GlobalColor.black, 2))
		if P2 > R2p * (Pg - Ps): painter.setPen(QPen(Qt.GlobalColor.red, 2))
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 750, self.mapFromScene(0,0).y() + 450),
			f"{R2r}  Ω"
		)
		if P2 > R2p * (Pg - Ps): painter.setPen(QPen(Qt.GlobalColor.black, 2))
		if P3 > R3p * Ps : painter.setPen(QPen(Qt.GlobalColor.red, 2))
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 880, self.mapFromScene(0,0).y() + 100),
			f"{R3r}  Ω"
		)
		if P3 > R3p * Ps: painter.setPen(QPen(Qt.GlobalColor.black, 2))
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
		# painter.drawText(QPointF(self.mapFromScene(0,0).x() + 250, self.mapFromScene(0,0).y() + 420),
		# 	f"{VGr}  Ω"
		# )
		# painter.drawText(QPointF(self.mapFromScene(0,0).x() + 1200, self.mapFromScene(0,0).y() + 420),
		# 	f"{VSr}  Ω"
		# )

		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 350, self.mapFromScene(0,0).y() + 50),
			f"{R1a}  A"
		)
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 750, self.mapFromScene(0,0).y() + 400),
			f"{R2a}  A"
		)
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 880, self.mapFromScene(0,0).y() + 50),
			f"{R3a}  A"
		)

		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 350, self.mapFromScene(0,0).y() + 30),
			f"Disipa: {P1}  W  -  Max: {round( R1p * Pg , 3)}"
		)
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 750, self.mapFromScene(0,0).y() + 380),
			f"Disipa: {P2}  W  -  Max: {round( R2p * (Pg - Ps) , 3)}"
		)
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 880, self.mapFromScene(0,0).y() + 30),
			f"Disipa: {P3}  W  -  Max: {round( R3p * Ps , 3)}"
		)
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 250, self.mapFromScene(0,0).y() + 420),
			f"Aporta: {Pg}  W"
		)
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 1200, self.mapFromScene(0,0).y() + 420),
			f"Aporta: {Ps}  W"
		)


		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 145, self.mapFromScene(0,0).y() + 580),
			"R1"
		)
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 345, self.mapFromScene(0,0).y() + 580),
			"R2"
		)
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 545, self.mapFromScene(0,0).y() + 580),
			"R3"
		)

		colors = resistance_to_colors(R1r)
		painter.setBrush(QBrush(colors[0]))
		painter.drawRect(QRect(self.mapFromScene(0,0).x() + 100, self.mapFromScene(0,0).y() + 600, 20, 60))
		painter.setBrush(QBrush(colors[1]))
		painter.drawRect(QRect(self.mapFromScene(0,0).x() + 130, self.mapFromScene(0,0).y() + 600, 20, 60))
		painter.setBrush(QBrush(colors[2]))
		painter.drawRect(QRect(self.mapFromScene(0,0).x() + 160, self.mapFromScene(0,0).y() + 600, 20, 60))
		painter.setBrush(QBrush(colors[3]))
		painter.drawRect(QRect(self.mapFromScene(0,0).x() + 190, self.mapFromScene(0,0).y() + 600, 20, 60))
		
		colors = resistance_to_colors(R2r)
		painter.setBrush(QBrush(colors[0]))
		painter.drawRect(QRect(self.mapFromScene(0,0).x() + 300, self.mapFromScene(0,0).y() + 600, 20, 60))
		painter.setBrush(QBrush(colors[1]))
		painter.drawRect(QRect(self.mapFromScene(0,0).x() + 330, self.mapFromScene(0,0).y() + 600, 20, 60))
		painter.setBrush(QBrush(colors[2]))
		painter.drawRect(QRect(self.mapFromScene(0,0).x() + 360, self.mapFromScene(0,0).y() + 600, 20, 60))
		painter.setBrush(QBrush(colors[3]))
		painter.drawRect(QRect(self.mapFromScene(0,0).x() + 390, self.mapFromScene(0,0).y() + 600, 20, 60))
		
		colors = resistance_to_colors(R3r)
		painter.setBrush(QBrush(colors[0]))
		painter.drawRect(QRect(self.mapFromScene(0,0).x() + 500, self.mapFromScene(0,0).y() + 600, 20, 60))
		painter.setBrush(QBrush(colors[1]))
		painter.drawRect(QRect(self.mapFromScene(0,0).x() + 530, self.mapFromScene(0,0).y() + 600, 20, 60))
		painter.setBrush(QBrush(colors[2]))
		painter.drawRect(QRect(self.mapFromScene(0,0).x() + 560, self.mapFromScene(0,0).y() + 600, 20, 60))
		painter.setBrush(QBrush(colors[3]))
		painter.drawRect(QRect(self.mapFromScene(0,0).x() + 590, self.mapFromScene(0,0).y() + 600, 20, 60))


		t = self.t1 % 4
		if   t < 1: 
			self.Particle1.setX(map_in_range(t, 0, 1, 182, 676))
			self.Particle1.setY(136)
		elif t < 2: 
			self.Particle1.setY(map_in_range(t, 1, 2, 136, 518))
			self.Particle1.setX(676)
		elif t < 3: 
			self.Particle1.setX(map_in_range(t, 2, 3, 676, 182))
			self.Particle1.setY(518)
		else:       
			self.Particle1.setY(map_in_range(t, 3, 4, 518, 136))
			self.Particle1.setX(182)
		t = self.t2 % 4
		if   t < 1: 
			self.Particle2.setX(map_in_range(t, 0, 1, 1156 , 676))
			self.Particle2.setY(136)
		elif t < 2: 
			self.Particle2.setY(map_in_range(t, 1, 2, 136 , 518 ))
			self.Particle2.setX(676)
		elif t < 3: 
			self.Particle2.setX(map_in_range(t, 2, 3, 676, 1156 ))
			self.Particle2.setY(518)
		else:       
			self.Particle2.setY(map_in_range(t, 3, 4, 518 , 136 ))
			self.Particle2.setX(1156)

		painter.setBrush(QBrush(Qt.GlobalColor.blue))
		painter.drawEllipse(self.Particle1, 5, 5)
		painter.setBrush(QBrush(Qt.GlobalColor.red))
		painter.drawEllipse(self.Particle2, 5, 5)

		super().paint(painter, option, widget)