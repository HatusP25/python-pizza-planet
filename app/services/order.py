from .BaseBlueprint import BaseBlueprint
from ..controllers import OrderController

order = BaseBlueprint('order', __name__, OrderController)


