"""Module contains the class Menu"""

class Menu:
    """
    Initialize a Menu instance with an empty collection of menu items.
    """

    def __init__(self) -> None:
        
        self.menu_items:  dict['Item']  ={}

    def add_menu (self, dic_items: dict['Item']) -> None:
        """
        Add a dictionary of items to the menu. If the category already exists,
        it updates the category with new items; otherwise, it adds a new category.

        Parameters:
        dic_items: dict - A dictionary where keys are categories (str) and values are
                          dictionaries of items (str) and their prices (float).
        """

        for category,item in dic_items.items():
            if category in self.menu_items:
                self.menu_items[category].update(item)
            else:
                self.menu_items[category]=item
