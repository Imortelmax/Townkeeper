import arcade 
import settings
from menu_view import MenuView

def main():
    window = arcade.Window(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, settings.SCREEN_TITLE)
    
    arcade.load_font(settings.ASSETS_PATH / "fonts" / "Deutsch.ttf")
    arcade.load_font(settings.ASSETS_PATH / "fonts" / "Ruritania.ttf")

    start_view = MenuView()
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()