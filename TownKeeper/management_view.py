import arcade
import arcade.gui
import settings
import random

class ManagementView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.manager = arcade.gui.UIManager()

        # Calcul du revenu
        performance = self.game_view.daily_correct_decisions / settings.VISITORS_PER_DAY
        self.income = int(performance * 20)
        self.game_view.gold += self.income

        self.setup_ui()

    def setup_ui(self):
        self.v_box = arcade.gui.UIBoxLayout()

        # Bouton pour payer le loyer + Nourriture
        rent_btn = arcade.gui.UIFlatButton(text=f"Payer Loyer (-{settings.DAILY_RENT} or)", width=300)
        rent_btn.on_click = self.pay_rent
        food_btn = arcade.gui.UIFlatButton(text=f"Payer Nourriture (-{settings.DAILY_FOOD} or)", width=300)
        food_btn.on_click = self.pay_food

        # Bouton jour suivant
        next_btn = arcade.gui.UIFlatButton(text="Jour Suivant", width=300)
        next_btn.on_click = self.next_day

        self.v_box.add(rent_btn.with_space_around(bottom=10))
        self.v_box.add(food_btn.with_space_around(bottom=20))
        self.v_box.add(next_btn)

        self.manager.add(arcade.gui.UIAnchorWidget(child=self.v_box))

    def pay_rent(self, event):
        if self.game_view.gold >= settings.DAILY_RENT:
            self.game_view.gold -= settings.DAILY_RENT
            print("Loyer payé !")

    def pay_food(self, event):
        if self.game_view.gold >= settings.DAILY_FOOD:
            self.game_view.gold -= settings.DAILY_FOOD
            print("Nourriture payé !")
    
    def next_day(self, event):
        self.game_view.day += 1
        self.game_view.visitors_seen = 0
        self.game_view.daily_correct_decisions = 0

        from rules import DAILY_RULES
        self.game_view.current_rule = random.choice(DAILY_RULES)
        self.game_view.spawn_visitor()
        self.window.show_view(self.game_view)

    def on_show_view(self):
        self.manager.enable()

    def on_draw(self):
        self.clear()
        arcade.draw_text("Rapport de Journée", settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT - 100,
                         arcade.color.BLACK, 30, anchor_x="center", font_name=settings.MAIN_FONT_NAME)
        arcade.draw_text(f"Revenu: +{self.income} or", settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT - 200,
                         arcade.color.BLACK, 20,anchor_x="center", font_name=settings.MAIN_FONT_NAME)
        self.manager.draw()