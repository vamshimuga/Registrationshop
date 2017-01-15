"""
VolumeVisualizationSimpleDeformation

:Authors:
	Berend Klein Haneveld
"""
from VolumeVisualization import VolumeVisualization
from VolumeVisualization import VisualizationTypeSimpleDeformation
from vtk import vtkVolumeProperty
from vtk import vtkColorTransferFunction
from vtk import vtkPiecewiseFunction
from ui.widgets.SliderFloatWidget import SliderFloatWidget
from ui.widgets.ColorWidget import ColorChoiceWidget
from core.decorators import overrides
from PySide.QtGui import QWidget
from PySide.QtGui import QGridLayout
from PySide.QtGui import QGroupBox
from PySide.QtCore import Qt


class VolumeVisualizationSimpleDeformation(VolumeVisualization):
	"""
	VolumeVisualization subclass for a simple visualization.
	"""
	def __init__(self):
		super(VolumeVisualizationSimpleDeformation, self).__init__()

		self.visualizationType = VisualizationTypeSimpleDeformation

		# Create the volume property
		self.volProp = vtkVolumeProperty()
		self.volProp.SetIndependentComponents(True)
		self.volProp.SetInterpolationTypeToLinear()
		self.volProp.ShadeOn()
		self.volProp.SetAmbient(0.3)
		self.volProp.SetDiffuse(0.8)
		self.volProp.SetSpecular(0.2)
		self.volProp.SetSpecularPower(10.0)
		self.volProp.SetScalarOpacityUnitDistance(0.8919)

		self.minimum = 0
		self.maximum = 1
		self.lowerBound = 0
		self.upperBound = 1
		colors = [[255, 139, 0], [0, 147, 255], [0, 255, 147], [213, 100, 255], [255, 75, 75]]
		self.colors = map(lambda x: [x[0] / 255.0, x[1] / 255.0, x[2] / 255.0], colors)
		self.color = self.colors[0]
		self.opacity = 1.0
		self.colorFunction = None
		self.opacityFunction = None

	@overrides(VolumeVisualization)
	def getParameterWidget(self):
		"""
		Returns a widget with sliders / fields with which properties of this
		volume property can be adjusted.
		:rtype: QWidget
		"""
		self.lowerBoundSlider = SliderFloatWidget()
		self.lowerBoundSlider.setName("Lower:")
		self.lowerBoundSlider.setRange([self.minimum, self.maximum])
		self.lowerBoundSlider.setValue(self.lowerBound)
		self.lowerBoundSlider.label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
		self.lowerBoundSlider.valueChanged.connect(self.valueChanged)

		self.upperBoundSlider = SliderFloatWidget()
		self.upperBoundSlider.setName("Upper:")
		self.upperBoundSlider.setRange([self.minimum, self.maximum])
		self.upperBoundSlider.setValue(self.upperBound)
		self.upperBoundSlider.label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
		self.upperBoundSlider.valueChanged.connect(self.valueChanged)

		layoutGroup = QGridLayout()
		layoutGroup.setAlignment(Qt.AlignTop)
		layoutGroup.setContentsMargins(5, 0, 0, 0)
		layoutGroup.setSpacing(0)
		layoutGroup.addWidget(self.lowerBoundSlider)
		layoutGroup.addWidget(self.upperBoundSlider)

		groupbox = QGroupBox("Thresholds:")
		groupbox.setLayout(layoutGroup)

		self.opacitySlider = SliderFloatWidget()
		self.opacitySlider.setName("Opacity:")
		self.opacitySlider.setRange([0.0, 1.0])
		self.opacitySlider.setValue(self.opacity)
		self.opacitySlider.label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
		self.opacitySlider.valueChanged.connect(self.valueChanged)

		self.colorChooser = ColorChoiceWidget()
		self.colorChooser.setName("Color:")
		self.colorChooser.setColors(self.colors)
		self.colorChooser.setColor(self.color)
		self.colorChooser.setMinimumHeight(self.upperBoundSlider.sizeHint().height())
		self.colorChooser.label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
		self.colorChooser.valueChanged.connect(self.valueChanged)

		otherLayoutGroup = QGridLayout()
		otherLayoutGroup.setAlignment(Qt.AlignTop)
		otherLayoutGroup.setContentsMargins(5, 0, 0, 0)
		otherLayoutGroup.setSpacing(0)
		otherLayoutGroup.addWidget(self.opacitySlider)
		# otherLayoutGroup.addWidget(self.colorChooser)

		# otherBox = QGroupBox("Color and opacity:")
		otherBox = QGroupBox()
		otherBox.setLayout(otherLayoutGroup)

		layout = QGridLayout()
		layout.setAlignment(Qt.AlignTop)
		layout.setContentsMargins(0, 0, 0, 0)
		layout.setHorizontalSpacing(0)
		layout.addWidget(groupbox)
		layout.addWidget(otherBox)

		widget = QWidget()
		widget.setLayout(layout)

		try:
			from ColumnResizer import ColumnResizer
			self.columnResizer = ColumnResizer()
			self.columnResizer.addWidgetsFromLayout(self.lowerBoundSlider.layout(), 0)
			self.columnResizer.addWidgetsFromLayout(self.upperBoundSlider.layout(), 0)
			self.columnResizer.addWidgetsFromLayout(self.colorChooser.layout(), 0)
			self.columnResizer.addWidgetsFromLayout(self.opacitySlider.layout(), 0)

			self.otherColRes = ColumnResizer()
			self.otherColRes.addWidgetsFromLayout(self.lowerBoundSlider.layout(), 2)
			self.otherColRes.addWidgetsFromLayout(self.upperBoundSlider.layout(), 2)
			self.otherColRes.addWidgetsFromLayout(self.opacitySlider.layout(), 2)
		except Exception, e:
			print e

		return widget

	@overrides(VolumeVisualization)
	def setImageData(self, imageData):
		if imageData is None:
			self.minimum = 0.0
			self.maximum = 1.0
			self.lowerBound = self.minimum
			self.upperBound = self.maximum
			self.opacity = 1.0
			return
		print("Set image data called from mag")
		self.minimum, self.maximum = imageData.GetScalarRange()
		self.lowerBound = self.minimum
		self.upperBound = self.maximum
		self.opacity = 1.0

	@overrides(VolumeVisualization)
	def setMapper(self, mapper):
		pass

	@overrides(VolumeVisualization)
	def shaderType(self):
		return 0

	@overrides(VolumeVisualization)
	def updateTransferFunction(self):
		r, g, b = self.color

		# Transfer functions and properties
		if not self.colorFunction:
			self.colorFunction = vtkColorTransferFunction()
		else:
			self.colorFunction.RemoveAllPoints()
		#self.colorFunction.AddRGBPoint(self.minimum, 0, 0, 1)
		#self.colorFunction.AddRGBPoint(0,0,1,0)
		#self.colorFunction.AddRGBPoint(self.maximum, 1, 0, 0)

		self.colorFunction.AddRGBPoint(self.upperBound, 10 / 255, 0, 0)
		self.colorFunction.AddRGBPoint(self.maximum, 10 / 255, 0, 0)
		self.colorFunction.AddRGBPoint(self.minimum + (self.maximum - self.minimum) / 3,59 / 255, 100 / 255,100 / 255)
		self.colorFunction.AddRGBPoint(self.minimum + 2 * (self.maximum - self.minimum) / 3, 1, 0, 1 / 255)
		self.colorFunction.AddRGBPoint(self.minimum, 1, 1, 1)
		self.colorFunction.AddRGBPoint(self.lowerBound, 1, 1, 1)

		if not self.opacityFunction:
			self.opacityFunction = vtkPiecewiseFunction()
		else:
			self.opacityFunction.RemoveAllPoints()
		'''self.opacityFunction.AddPoint(self.minimum, 0)
		self.opacityFunction.AddPoint(self.lowerBound, 0)
		self.opacityFunction.AddPoint(self.lowerBound+0.0001, self.opacity)
		self.opacityFunction.AddPoint(self.upperBound-0.0001, self.opacity)
		#self.opacityFunction.AddPoint((self.lowerBound+self.upperBound)/2,1) #point added
		self.opacityFunction.AddPoint(self.upperBound, 0)
		self.opacityFunction.AddPoint(self.maximum, 0)'''

		self.opacityFunction.AddPoint(self.lowerBound, 0)
		self.opacityFunction.AddPoint(self.minimum, 0)
		self.opacityFunction.AddPoint(self.maximum, self.opacity)
		self.opacityFunction.AddPoint(self.upperBound, self.opacity)

		self.volProp.SetColor(self.colorFunction)
		self.volProp.SetScalarOpacity(self.opacityFunction)

		self.updatedTransferFunction.emit()

	@overrides(VolumeVisualization)
	def valueChanged(self, value):
		"""
		This method is called when the value of one of the sliders / fields is
		adjusted. Argument value is unused. It is just there so that it can be
		connected to the signals of the interface elements.

		:type value: int
		"""
		self.lowerBound = min(self.lowerBoundSlider.value(), self.upperBoundSlider.value())
		self.upperBound = max(self.lowerBoundSlider.value(), self.upperBoundSlider.value())
		self.color = self.colorChooser.color
		self.opacity = self.opacitySlider.value()
		self.updateTransferFunction()
