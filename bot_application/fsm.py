from enum import Enum

from django.core.exceptions import ObjectDoesNotExist
from bot_application.keyboards import create_recipes_keyboard
from custom_adminka.models import CurrentUser


class State(Enum):
    WAITING_FOR_NAME = 'waiting_for_name'
    WAITING_FOR_GENDER = 'waiting_for_gender'
    MAIN_MENU = 'main_menu'
    RECIPE_SELECTION = 'recipe_selection'


class BotFSM:
    def __init__(self, bot):
        self.bot = bot

    def get_state(self, user_id):
        try:
            user = CurrentUser.objects.get(id=user_id)
            if user.state:
                return user.state
        except CurrentUser.DoesNotExist:
            return None

    def set_state(self, user_id, state):
        try:
            user = CurrentUser.objects.get(id=user_id)
            user.state = state
            user.save()
        except CurrentUser.DoesNotExist:
            user = CurrentUser.objects.create(id=user_id, state=state)

    def get_user_profile(self, user_id):
        try:
            user_profile = CurrentUser.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return None
        return user_profile

    def handle_about_me(self, message):
        user_id = message.chat.id
        state = self.get_state(user_id)
        if state == State.MAIN_MENU.value:
            user_profile = self.get_user_profile(user_id)
            if user_profile:
                response = f"Ім'я: {user_profile.name}\nСтать: {user_profile.gender}"
                self.bot.bot.send_message(user_id, response)
            else:
                self.bot.bot.send_message(user_id, "Заповніть анкету")

    def handle_recipes(self, message):
        user_id = message.chat.id
        state = self.get_state(user_id)
        if state == State.MAIN_MENU.value:
            recipe_list = self.bot.get_recipe_list()
            if len(recipe_list) > 0:
                keyboard = create_recipes_keyboard(self.bot)
                self.set_state(user_id, State.RECIPE_SELECTION.value)
                self.bot.bot.send_message(user_id, "Оберіть рецепт", reply_markup=keyboard)
            else:
                self.bot.bot.send_message(user_id, "Нема доступних рецептів")

    def handle_recipe_selection(self, message):
        user_id = message.chat.id
        state = self.get_state(user_id)
        if state == State.RECIPE_SELECTION.value:
            recipe_name = message.text
            recipe = self.bot.get_recipe_by_name(recipe_name)
            if recipe:
                self.bot.bot.send_photo(user_id, photo=recipe.photo, caption=recipe.description)
            else:
                self.bot.bot.send_message(user_id, "Рецепт не знайдено")
