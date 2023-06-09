from telebot import types


def create_main_menu_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(types.KeyboardButton("Про мене"))
    keyboard.add(types.KeyboardButton("Рецепти"))
    return keyboard


def create_gender_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(types.KeyboardButton("Чоловік"))
    keyboard.add(types.KeyboardButton("Жінка"))
    return keyboard


def create_recipes_keyboard(self):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    recipes = self.get_recipe_list()
    if recipes:
        for recipe in recipes:
            keyboard.add(types.KeyboardButton(recipe.name))
        keyboard.add(types.KeyboardButton("Головне меню"))
        return keyboard
    else:
        return None
