from .BaseBlueprint import BaseBlueprint
from ..controllers import BeverageController

beverage = BaseBlueprint('beverage', __name__, BeverageController)
