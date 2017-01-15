"""
VolumeVisualizationFactory

:Authors:
	Berend Klein Haneveld
"""
from VolumeVisualization import VisualizationTypeSimple
from VolumeVisualization import VisualizationTypeCT
from VolumeVisualization import VisualizationTypeMIP
from VolumeVisualization import VisualizationTypeMIDA
from VolumeVisualization import VisualizationTypeRamp
from VolumeVisualization import VisualizationTypeTransferFunction
from VolumeVisualization import VisualizationTypeSimpleDeformation
from VolumeVisualization import VisualizationTypeSimpleDeformationJ
from VolumeVisualization import VisualizationTypeSimpleDeformationB
from VolumeVisualizationSimple import VolumeVisualizationSimple
from VolumeVisualizationSimpleDeformation import VolumeVisualizationSimpleDeformation
from VolumeVisualizationSimpleDeformationJ import VolumeVisualizationSimpleDeformationJ
from VolumeVisualizationSimpleDeformationB import VolumeVisualizationSimpleDeformationB
from VolumeVisualizationCT import VolumeVisualizationCT
from VolumeVisualizationMIP import VolumeVisualizationMIP
from VolumeVisualizationMIDA import VolumeVisualizationMIDA
from VolumeVisualizationRamp import VolumeVisualizationRamp
from VolumeVisualizationTransferFunction import VolumeVisualizationTransferFunction


# Factory
class VolumeVisualizationFactory(object):
	"""
	VolumeVisualizationFactory makes and creates proper VolumeVisualization objects.
	"""

	@classmethod
	def CreateProperty(cls, visualizationType):
		if visualizationType == VisualizationTypeSimple:
			print("Viz simple is used")
			return VolumeVisualizationSimple()
		elif visualizationType == VisualizationTypeSimpleDeformation:
			print("Viz simple magnitude is used")
			return VolumeVisualizationSimpleDeformation()
		elif visualizationType == VisualizationTypeSimpleDeformationJ:
			print("Viz simple J is used")
			return VolumeVisualizationSimpleDeformationJ()
		elif visualizationType == VisualizationTypeSimpleDeformationB:
			print("Viz simple B is used")
			return VolumeVisualizationSimpleDeformationB()
		elif visualizationType == VisualizationTypeCT:
			print("Viz CT is used")
			return VolumeVisualizationCT()
		elif visualizationType == VisualizationTypeMIP:
			print("Viz MIP is used")
			return VolumeVisualizationMIP()
		elif visualizationType == VisualizationTypeRamp:
			print("Viz ramp is used")
			return VolumeVisualizationRamp()
		elif visualizationType == VisualizationTypeMIDA:
			print("Viz MIDA is used")
			return VolumeVisualizationMIDA()
		elif visualizationType == VisualizationTypeTransferFunction:
			print("Viz type transfer is used")
			return VolumeVisualizationTransferFunction()
		else:
			print visualizationType
			assert False
