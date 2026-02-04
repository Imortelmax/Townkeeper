import arcade
import arcade.gui
import settings

class PauseView(arcade.View):
    def __init__(self):
        super().__init__()
        self.game_view = game_view
        self.manager = arcade.gui.UIManager()
        self.setup_ui()

    def setup_ui(self):
        self.manager.clear()
        anchor = arcade.gui.UIAnchorLayout()
        v_box = arcade.gui.UIBoxLayout(space_between=20)

        # Title
        title = arcade.gui.UILabel(
            text="Pause", 
            font_size=40, 
            font_name=settings.MAIN_FONT_NAME, 
            text_color=settings.COLOR_FONT
        )
        v_box.add(title)

        # Style des boutons
        btn_style = {
            "normal": {
                "font_name": settings.MAIN_FONT_NAME,
                "font_color": settings.COLOR_FONT,
                "font_size": 20,
                "bg_color": settings.COLOR_BACKGROUND,
                "border_width": 2,
                "border_color": settings.COLOR_FONT,
            },
            "hover": {
                "font_name": settings.MAIN_FONT_NAME,
                "font_color": settings.COLOR_FONT,
                "font_size": 21,
                "bg_color": settings.COLOR_BACKGROUND,
                "border_color": settings.COLOR_FONT,
            },
            "press": {
                "font_name": settings.MAIN_FONT_NAME,
                "font_color": settings.COLOR_FONT,
                "font_size": 20,
                "bg_color": settings.COLOR_BACKGROUND,
            },
        }

        resume_btn = arcade.gui.UIFlatButton(text="Reprendre", width=200, style=btn_style)
        resume_btn.on_click = self.on_resume
        options_btn = arcade.gui.UIFlatButton(text="Options", width=200, style=btn_style)
        menu_btn = arcade.gui.UIFlatButton(text="Retour au menu", width=200, style=btn_style)
        menu_btn.on_click = self.on_menu
        quit_btn = arcade.gui.UIFlatButton(text="Quitter le jeu", width=200, style=btn_style)
        quit_btn.on_click = self.on_quit

        v_box.add(resume_btn)
        v_box.add(options_btn)
        v_box.add(menu_btn)
        v_box.add(quit_btn)

        anchor.add(
            child=v_box,
            anchor_x="center_x",
            anchor_y="center_y",
        )
        self.manager.add(anchor)

    def on_resume(self, event):
        self.window.show_view(self.game_view)
    
    def on_menu(self, event):
        from menu_view import MenuView
        self.window.show_view(MenuView())
    
    def on_quit(self, event):
        arcade.exit()

    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(settings.COLOR_BACKGROUND)

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()