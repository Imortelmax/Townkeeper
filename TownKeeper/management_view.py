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

        self.is_food_paid = False
        self.is_rent_paid = False

        self.setup_ui()

    def setup_ui(self):
        self.manager.clear()

        anchor_layout= arcade.gui.UIAnchorLayout()
        self.v_box = arcade.gui.UIBoxLayout(space_between=20)

        # Bouton pour payer le loyer + Nourriture
        self.rent_btn = arcade.gui.UIFlatButton(text=f"Payer Loyer (-{settings.DAILY_RENT} or)", width=300)
        self.rent_btn.on_click = self.pay_rent
        self.food_btn = arcade.gui.UIFlatButton(text=f"Payer Nourriture (-{settings.DAILY_FOOD} or)", width=300)
        self.food_btn.on_click = self.pay_food

        # Bouton jour suivant
        next_btn = arcade.gui.UIFlatButton(text="Jour Suivant", width=300)
        next_btn.on_click = self.next_day

        self.v_box.add(self.rent_btn)
        self.v_box.add(self.food_btn)
        self.v_box.add(next_btn)

        anchor_layout.add(
            child=self.v_box,
            anchor_x="center_x",
            anchor_y="center_y",
        )
        self.manager.add(anchor_layout)

    def pay_rent(self, event):
        if self.game_view.gold >= settings.DAILY_RENT and not self.is_rent_paid:
            self.game_view.gold -= settings.DAILY_RENT
            
            self.is_rent_paid = True
            self.rent_btn.text = "Loyer payé"
            print("Loyer payé !")

    def pay_food(self, event):
        if self.game_view.gold >= settings.DAILY_FOOD and not self.is_food_paid:
            self.game_view.gold -= settings.DAILY_FOOD

            self.is_food_paid = True
            self.food_btn.text = "Nourriture payée"
            print("Nourriture payé !")
    
    def next_day(self, event):
        # Incrementation du jour
        self.game_view.day += 1

        # Reset 
        self.game_view.visitors_seen = 0
        self.game_view.daily_correct_decisions = 0
        self.game_view.visitor_list.clear()

        # Remet le jour
        self.game_view.is_day_over = False
        self.game_view.end_day_timer = 0
        self.game_view.manager.enable()

        from rules import DAILY_RULES
        self.game_view.current_rule = random.choice(DAILY_RULES)
        self.game_view.spawn_visitor()

        self.window.show_view(self.game_view)

    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(settings.COLOR_BACKGROUND)

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()

        # Ttre
        arcade.draw_text("Rapport de Journée", settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT - 100,
                         settings.COLOR_FONT_END_DAY, 30, anchor_x="center", font_name=settings.MAIN_FONT_NAME)

        # Revenu
        arcade.draw_text(f"Revenu: +{self.income} or", settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT - 150,
                         settings.COLOR_FONT_END_DAY, 20, anchor_x="center", font_name=settings.MAIN_FONT_NAME)

        # Or actuel
        arcade.draw_text(f"Or en poche: {self.game_view.gold}", settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT - 180,
                         settings.COLOR_FONT_GOLD, 20, anchor_x="center", font_name=settings.MAIN_FONT_NAME)

        self.manager.draw()