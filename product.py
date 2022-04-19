class Product:
    def __init__(self, name, stock, links):
        self.name = name
        self.stock = stock
        self.links = links

    def isStocked(self):
        return self.stock > 0


