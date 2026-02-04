import arcade
import arcade.gui
import random
import settings
from visitor import Visitor
from rules import DAILY_RULES
from arcade.texture import Texture, ImageData 

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()

        # Etat du jeu
        self.gold = settings.STARTING_GOLD
        self.day = 1
        self.visitors_seen = 0
        self.daily_correct_decisions = 0
        self.lord_trust = 75
        
        self.end_day_timer = 0
        self.is_day_over = False

        self.current_rule = random.choice(DAILY_RULES)
        self.current_visitor = None
        self.visitor_list = arcade.SpriteList()

        bg_path = settings.ASSETS_PATH / "pictures" / "background.png"
        self.background = arcade.load_texture(bg_path)
        
        full_image = arcade.load_image(bg_path)
        ratio_hauteur = settings.DESK_HEIGHT / settings.SCREEN_HEIGHT
        hauteur_coupe_pixels = int(full_image.height * ratio_hauteur)
        y_start = full_image.height - hauteur_coupe_pixels
        crop_area = (0, y_start, full_image.width, full_image.height)
        desk_image = full_image.crop(crop_area)
        self.desk_texture = Texture(ImageData(desk_image))
        
        self.setup_ui()
        self.spawn_visitor()

    def setup_ui(self):
        self.manager.clear()

        anchor_layout = arcade.gui.UIAnchorLayout()
        self.v_box = arcade.gui.UIBoxLayout(vertical=False, space_between=50)
        
        style_accept = {
            "normal": {
                "font_name": settings.MAIN_FONT_NAME,
                "font_size": 20,
                "font_color": arcade.color.WHITE,
                "bg_color": settings.COLOR_BTN_ACCEPT,
                "border_color": arcade.color.DARK_GREEN,
                "border_width": 2,
            },
            "hover": {
                "font_name": settings.MAIN_FONT_NAME,
                "font_size": 21,
                "font_color": arcade.color.WHITE,
                "bg_color": arcade.color.FOREST_GREEN,
                "border_color": arcade.color.WHITE,
            },
            "press": {
                "font_name": settings.MAIN_FONT_NAME,
                "font_size": 20,
                "font_color": arcade.color.BLACK,
                "bg_color": settings.COLOR_BTN_ACCEPT
            }
        }

        style_reject = {
            "normal": {
                "font_name": settings.MAIN_FONT_NAME,
                "font_size": 20,
                "font_color": arcade.color.WHITE,
                "bg_color": settings.COLOR_BTN_REJECT,
                "border_color": arcade.color.DARK_RED,
                "border_width": 2,
            },
            "hover": {
                "font_name": settings.MAIN_FONT_NAME,
                "font_size": 21,
                "font_color": arcade.color.WHITE,
                "bg_color": arcade.color.RED_DEVIL,
                "border_color": arcade.color.WHITE,
            },
            "press": {
                "font_name": settings.MAIN_FONT_NAME,
                "font_size": 20,
                "font_color": arcade.color.BLACK,
                "bg_color": settings.COLOR_BTN_REJECT
            }
        }

        acc_btn = arcade.gui.UIFlatButton(text="ACCEPTER", width=220, height=60, style=style_accept)
        rej_btn = arcade.gui.UIFlatButton(text="REFUSER", width=220, height=60, style=style_reject)

        acc_btn.on_click = self.on_accept
        rej_btn.on_click = self.on_reject

        self.v_box.add(rej_btn)
        self.v_box.add(acc_btn)

        anchor_layout.add(
            child=self.v_box,
            anchor_x="center_x",
            anchor_y="bottom",
            align_y=30
        )

        #Place des boutons
        self.manager.add(anchor_layout)
        
    def spawn_visitor(self):
        self.current_visitor = Visitor(
            name = random.choice(settings.NAMES),
            role = random.choice(settings.ROLES),
            story = random.choice(settings.STORIES),
            country = random.choice(settings.COUNTRIES)
        )

        self.visitor_list.clear()
        self.visitor_list.append(self.current_visitor)
  
    def on_accept(self, event):
        if self.current_visitor and self.current_visitor.arrived and not self.is_day_over:
            self.judge(True)

    def on_reject(self, event):
        if self.current_visitor and self.current_visitor.arrived and not self.is_day_over:
            self.judge(False)

    def judge(self, player_choice):
        v = self.current_visitor
        d = v.document
        doc_valid = (v.name == d.owner_name and v.role == d.role and v.country == d.country and not d.is_forgery)
        is_violating_rule = self.current_rule["condition"](v)
        should_accept = doc_valid and not is_violating_rule

        if player_choice == should_accept:
            self.daily_correct_decisions += 1
            self.lord_trust = min(100, self.lord_trust + 5)
        else:
            self.lord_trust = max(0, self.lord_trust - 10)

        self.visitors_seen +=1

        if self.visitors_seen >= settings.VISITORS_PER_DAY:
            print(f"Fin de la journée ! Attente de {self.end_day_timer} secondes...")
            self.is_day_over = True
            self.end_day_timer = 2
            self.manager.disable()
        else:
            self.spawn_visitor()

    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(settings.COLOR_BACKGROUND)
    
    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        
        arcade.draw_texture_rect(
            texture=self.background,
            rect=arcade.Rect(
                left=0, right=settings.SCREEN_WIDTH,
                bottom=0, top=settings.SCREEN_HEIGHT,
                width=settings.SCREEN_WIDTH, height=settings.SCREEN_HEIGHT,
                x=settings.SCREEN_WIDTH / 2, y=settings.SCREEN_HEIGHT / 2
            )
        )

        if self.current_visitor:
            self.visitor_list.draw()
            
            arcade.draw_texture_rect(
                texture=self.desk_texture,
                rect=arcade.Rect(
                    left=0, right=settings.SCREEN_WIDTH,
                    bottom=0, top=settings.DESK_HEIGHT,
                    width=settings.SCREEN_WIDTH, height=settings.DESK_HEIGHT,
                    x=settings.SCREEN_WIDTH / 2, y=settings.DESK_HEIGHT / 2
                )
            )
            
            self.current_visitor.draw_passeport()

        arcade.draw_text(f"Jour {self.day} - Or: {self.gold}", 50, settings.SCREEN_HEIGHT - 50, settings.COLOR_FONT, 20, font_name=settings.MAIN_FONT_NAME)
        arcade.draw_text(f"Règle {self.current_rule['text']}",  50, settings.SCREEN_HEIGHT - 80, settings.COLOR_FONT_RULE, 18, font_name=settings.MAIN_FONT_NAME)
        
        self.manager.draw()

    def on_update(self, delta_time):
        if self.current_visitor:
            self.current_visitor.update()

        if self.is_day_over:
            self.end_day_timer -= delta_time
            if self.end_day_timer <= 0:
                from management_view import ManagementView
                self.window.show_view(ManagementView(self))