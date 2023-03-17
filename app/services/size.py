from .BaseBlueprint import BaseBlueprint
from ..controllers import SizeController

size = BaseBlueprint('size', __name__, SizeController)
