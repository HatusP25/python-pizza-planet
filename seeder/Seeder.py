from app.controllers import OrderController
from app.repositories.managers import OrderManager, BeverageManager, IngredientManager, SizeManager
from seeder.utils.data import ingredients, sizes, beverages, clients
from seeder.utils.functions import get_random_price, pick_random_list, pick_random_dict, pick_many_random_list, \
    get_random_date


class DatabaseSeeder:
    def __init__(self):
        self.orders = []
        self.ingredients = []
        self.sizes = []
        self.beverages = []
        self.clients = []
        self.orderController = OrderController()
        self.orderManager = OrderManager()
        self.beverageManager = BeverageManager()
        self.ingredientManager = IngredientManager()
        self.sizeManager = SizeManager()

    def seed(self):
        self.seed_beverages()
        self.seed_sizes()
        self.seed_ingredients()
        self.seed_orders()

    def seed_orders(self):
        for _ in range(100):
            client = pick_random_list(clients)
            size = pick_random_list(self.sizes)
            order_ingredients = pick_many_random_list(self.ingredients)
            order_beverages = pick_many_random_list(self.beverages)
            self.orders.append(self.orderController.create({
                'client_name': client['client_name'],
                'client_dni': client['client_dni'],
                'client_phone': client['client_phone'],
                'client_address': client['client_address'],
                'date': get_random_date(),
                'size_id': str(size),
                'ingredients': order_ingredients,
                'beverages': order_beverages
            }))

    def seed_ingredients(self):
        for ingredient in ingredients:
            self.ingredients.append(
                self.ingredientManager.create({"name": ingredient, 'price': get_random_price()})["_id"])

    def seed_sizes(self):
        for size in sizes:
            self.sizes.append(self.sizeManager.create(size)["_id"])

    def seed_beverages(self):
        for beverage in beverages:
            self.beverages.append(self.beverageManager.create({"name": beverage, 'price': get_random_price()})["_id"])

    def drop_tables(self):
        self.beverageManager.drop_table()
        self.ingredientManager.drop_table()
        self.sizeManager.drop_table()
        self.orderManager.drop_table()


Seeder = DatabaseSeeder()
