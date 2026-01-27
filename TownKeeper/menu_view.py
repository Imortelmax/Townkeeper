import arcade
import arcade.gui
import settings
from game_view import GameView

class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        
        # --- 1. Chargement IDENTIQUE à GameView ---
        # On utilise load_texture car on sait que ça marche chez vous
        try:
            self.background = arcade.load_texture(settings.ASSETS_PATH / "pictures" / "menu.png")
        except Exception as e:
            print(f"Erreur chargement: {e}")
            self.background = None

        self.setup()

    def setup(self):
        self.manager.clear()
        
        self.anchor = arcade.gui.UIAnchorLayout()
        self.v_box = arcade.gui.UIBoxLayout(space_between=20)

        # --- Titre ---
        title_label = arcade.gui.UILabel(
            text=settings.SCREEN_TITLE,
            font_size=40,
            font_name="Kenney Future",
            text_color=arcade.color.APPLE_GREEN,
        )
        self.v_box.add(title_label)

        # --- Style des boutons ---
        default_style = {
            "normal": {
                "font_name": settings.START_FONT_NAME,
                "font_size": 15,
                "font_color": arcade.color.WHITE,
                "bg_color": (50, 50, 50),
                "border_width": 2,
                "border_color": arcade.color.BLACK,
            },
            "hover": {
                "font_name": settings.START_FONT_NAME,
                "font_size": 15,
                "font_color": arcade.color.WHITE,
                "bg_color": (100, 100, 100),
                "border_width": 2,
                "border_color": arcade.color.WHITE,
            },
            "press": {
                "font_name": settings.START_FONT_NAME,
                "font_size": 15,
                "font_color": arcade.color.GRAY,
                "bg_color": (20, 20, 20),
                "border_width": 2,
                "border_color": arcade.color.BLACK,
            },
        }

        # --- Boutons ---
        play_btn = arcade.gui.UIFlatButton(text="JOUER", width=250, style=default_style)
        play_btn.on_click = self.on_click_play
        self.v_box.add(play_btn)

        options_btn = arcade.gui.UIFlatButton(text="OPTIONS", width=250, style=default_style)
        options_btn.on_click = self.on_click_options
        self.v_box.add(options_btn)

        quit_btn = arcade.gui.UIFlatButton(text="QUITTER", width=250, style=default_style)
        quit_btn.on_click = self.on_click_quit
        self.v_box.add(quit_btn)

        self.anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=self.v_box
        )
        self.manager.add(self.anchor)

    def on_resize(self, width, height):
        """Indispensable pour Linux/Arcade 3.0"""
        super().on_resize(width, height)
        self.manager.trigger_render()

    def on_click_play(self, event):
        game_view = GameView()
        self.window.show_view(game_view)

    def on_click_options(self, event):
        print("Options: À implémenter")

    def on_click_quit(self, event):
        arcade.exit()

    def on_show_view(self):
        self.manager.enable()
        self.window.background_color = arcade.color.ALMOND 

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        
        if self.background:
            arcade.draw_texture_rect(
                texture=self.background,
                rect=arcade.Rect(
                    left=0,
                    right=settings.SCREEN_WIDTH,
                    bottom=0,
                    top=settings.SCREEN_HEIGHT,
                    width=settings.SCREEN_WIDTH,
                    height=settings.SCREEN_HEIGHT,
                    x=settings.SCREEN_WIDTH / 2,
                    y=settings.SCREEN_HEIGHT / 2, 
                )
            )
        
        self.manager.draw()