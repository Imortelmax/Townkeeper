import arcade
import arcade.gui
import random
import settings
from visitor import Visitor
from rules import DAILY_RULES
# Nécessaire pour le découpage manuel de l'image
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
        
        self.current_rule = random.choice(DAILY_RULES)
        self.current_visitor = None
        self.visitor_list = arcade.SpriteList()

        # --- CORRECTION FINALE : DECOUPAGE PROPORTIONNEL DU BUREAU ---
        bg_path = settings.ASSETS_PATH / "pictures" / "background.png"
        
        # 1. On charge la texture de fond normale (Arcade s'occupe de la redimensionner)
        self.background = arcade.load_texture(bg_path)
        
        # 2. On charge l'image brute pour créer le "pansement" (le bureau devant)
        full_image = arcade.load_image(bg_path)
        
        # CALCUL DU RATIO :
        # On regarde quel pourcentage de l'écran est occupé par le bureau.
        # Exemple : Si l'écran fait 850px de haut et le bureau 240px, le ratio est ~0.28 (28%)
        ratio_hauteur = settings.DESK_HEIGHT / settings.SCREEN_HEIGHT
        
        # On applique ce ratio à la VRAIE hauteur de votre image (qui peut être 1080px, 4000px, etc.)
        hauteur_coupe_pixels = int(full_image.height * ratio_hauteur)
        
        # On calcule le point de départ Y (Coordonnée 0 = Haut de l'image en PIL)
        # On veut couper tout en bas, donc : HauteurTotale - HauteurAcouper
        y_start = full_image.height - hauteur_coupe_pixels
        
        # On définit la zone de coupe : (Gauche, Haut, Droite, Bas)
        crop_area = (0, y_start, full_image.width, full_image.height)
        
        # On découpe et on transforme en texture utilisable par Arcade
        desk_image = full_image.crop(crop_area)
        self.desk_texture = Texture(ImageData(desk_image))
        
        self.setup_ui()
        self.spawn_visitor()

    def setup_ui(self):
        self.manager.clear()
        self.v_box = arcade.gui.UIBoxLayout(vertical=False, space_between=20)
        
        acc_btn = arcade.gui.UIFlatButton(text="ACCEPTER", width=200)
        rej_btn = arcade.gui.UIFlatButton(text="REFUSER", width=200)

        acc_btn.on_click = self.on_accept
        rej_btn.on_click = self.on_reject

        self.v_box.add(acc_btn)
        self.v_box.add(rej_btn)

        self.manager.add(arcade.gui.UIAnchorLayout(child=self.v_box, anchor_y="bottom", align_y=50))
        
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
        if self.current_visitor and self.current_visitor.arrived:
            self.judge(True)

    def on_reject(self, event):
        if self.current_visitor and self.current_visitor.arrived:
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
            from management_view import ManagementView
            self.window.show_view(ManagementView(self))
        else:
            self.spawn_visitor()

    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(settings.COLOR_BACKGROUND)
    
    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        
        # 1. DESSINER LE FOND COMPLET
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
            # 2. DESSINER LE VISITEUR (Ses jambes dépassent sur le bureau)
            self.visitor_list.draw()
            
            # 3. DESSINER LE "PANSEMENT" (Le bureau redessiné par dessus)
            # Cela cache parfaitement les jambes car la texture correspond exactement au bas de l'écran
            arcade.draw_texture_rect(
                texture=self.desk_texture,
                rect=arcade.Rect(
                    left=0, right=settings.SCREEN_WIDTH,
                    bottom=0, top=settings.DESK_HEIGHT,
                    width=settings.SCREEN_WIDTH, height=settings.DESK_HEIGHT,
                    x=settings.SCREEN_WIDTH / 2, y=settings.DESK_HEIGHT / 2
                )
            )
            
            # 4. PASSEPORT (Par dessus le bureau)
            self.current_visitor.draw_passeport()

        arcade.draw_text(f"Jour {self.day} - Or: {self.gold}", 50, settings.SCREEN_HEIGHT - 50, arcade.color.BLACK, 20)
        arcade.draw_text(f"Règle {self.current_rule['text']}",  50, settings.SCREEN_HEIGHT - 80, arcade.color.DARK_RED, 18)
        
        self.manager.draw()

    def on_update(self, delta_time):
        if self.current_visitor:
            self.current_visitor.update()