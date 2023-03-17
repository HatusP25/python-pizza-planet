from .BaseBlueprint import BaseBlueprint
from ..controllers import IngredientController


ingredient = BaseBlueprint('ingredient', __name__, IngredientController)
