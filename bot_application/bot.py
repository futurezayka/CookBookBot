import os
import django
import telebot
from decouple import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_task.settings')
django.setup()

from keyboards import create_main_menu_keyboard, create_gender_keyboard
from custom_adminka.models import CurrentUser, Recipe
from fsm import BotFSM, State


class RecipeBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.fsm = BotFSM(self)

        self.bot.message_handler(commands=['start'])(self.handle_start)
        self.bot.message_handler(
            func=lambda message: CurrentUser.objects.get(id=message.chat.id).state == 'waiting_for_name')(
            self.handle_name)
        self.bot.message_handler(
            func=lambda message: CurrentUser.objects.get(id=message.chat.id).state == 'waiting_for_gender')(
            self.handle_gender)
        self.bot.message_handler(func=lambda message: message.text == "Про мене")(self.fsm.handle_about_me)
        self.bot.message_handler(func=lambda message: message.text == "Рецепти")(self.fsm.handle_recipes)
        self.bot.message_handler(func=lambda message: self.is_recipe_button(message.text))(
            self.fsm.handle_recipe_selection)
        self.bot.message_handler(func=lambda message: message.text == "Головне меню")(
            lambda message: self.show_main_menu(message.chat.id))

    def run(self):
        self.bot.infinity_polling()

    def handle_start(self, message):
        if not CurrentUser.objects.filter(id=message.chat.id).exists():
            self.bot.send_message(message.chat.id, "Вітаю, введіть ваше ім'я:")
            CurrentUser.objects.create(id=message.chat.id,
                                       username=f'@{message.from_user.username}',
                                       first_name=message.from_user.first_name, last_name=message.from_user.last_name)
            self.fsm.set_state(message.chat.id, State.WAITING_FOR_NAME.value)
        else:
            self.show_main_menu(message.chat.id)

    def handle_name(self, message):
        user = CurrentUser.objects.get(id=message.chat.id)
        user.name = message.text
        user.state = 'waiting_for_gender'
        user.save()
        self.fsm.set_state(message.chat.id, State.WAITING_FOR_GENDER.value)
        self.bot.send_message(message.chat.id, "Вкажіть Вашу стать:", reply_markup=create_gender_keyboard())

    def handle_gender(self, message):
        user = CurrentUser.objects.get(id=message.chat.id)
        user.gender = message.text
        user.save()
        self.fsm.set_state(message.chat.id, State.MAIN_MENU.value)
        self.show_main_menu(message.chat.id)

    def show_main_menu(self, chat_id):
        keyboard = create_main_menu_keyboard()
        self.fsm.set_state(chat_id, State.MAIN_MENU.value)
        self.bot.send_message(chat_id, "Головне меню:", reply_markup=keyboard)

    def get_recipe_list(self):
        return Recipe.objects.all()

    def get_recipe_by_name(self, name):
        return Recipe.objects.get(name=name)

    def is_recipe_button(self, text):
        recipes = self.get_recipe_list()
        recipe_names = [recipe.name for recipe in recipes]
        return text in recipe_names


if __name__ == "__main__":
    bot = RecipeBot(config('TOKEN'))
    bot.run()
