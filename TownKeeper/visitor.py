import arcade 
import random
from document import Document
import settings

class Visitor(arcade.Sprite):
    def __init__(self, name, role, story, country, is_sick=False):
        char_name = role.strip() + str(random.randint(1, 2))
        image_path = settings.ASSETS_PATH / "visitors" / f"{char_name}.png"
        try:
            super().__init__(str(image_path), scale=0.2)
        except:
            super().__init__(arcade.make_soft_circle_texture(60, arcade.color.WHITE))
        
        self.name, self.role, self.story = name, role, story
        self.country, self.is_sick = country, is_sick
        self.document_signs = [settings.COUNTRY_SIGNS.get(self.country, 'Inconnu')]

        # Paramètres d'animation
        self.start_scale = 0.9
        self.target_scale = 3

        self.center_x = settings.SCREEN_WIDTH // 2
        self.center_y = settings.SCREEN_HEIGHT - 260
        self.target_x = 560
        self.target_y = 500

        self.arrived = False
        self.document = self.generate_document()

    def generate_document(self):
        seal = settings.COUNTRY_SIGNS.get(self.country, "Sceau")
        doc = Document(self.name, self.country, self.role, seal, random.randint(5, 15))

        if random.random() < settings.FORGERY_CHANCE:
            doc.create_forgery()
        return doc
    
    def update(self):
        """Animation fluide"""
        if not self.arrived:
            # Plus le chiffre est petit plus l'anime est lente
            ease_speed = 0.02

            # On rapproche progressivement la position Y de la cible
            self.center_y += (self.target_y - self.center_y) * ease_speed
            self.center_x += (self.target_x - self.center_x) * ease_speed

            current_scale = self.scale[0]

            # On rapproche progressivement la taille
            new_scale = current_scale + (self.target_scale - current_scale) * ease_speed
            self.scale = new_scale

            if abs(self.center_y - self.target_y) < 1 and abs(self.center_x - self.target_x) < 1:
                self.center_y = self.target_y
                self.center_x = self.target_x
                self.scale = self.target_scale
                self.arrived = True

    def draw_passeport(self):
        """Rendu du texte sur le document"""
        if self.arrived:
            start_y = 370
            arcade.draw_text(f"Nom: {self.document.owner_name}", 390, start_y, arcade.color.BLACK, 25, font_name=settings.MAIN_FONT_NAME)
            arcade.draw_text(f"Métier: {self.document.role}", 380, start_y - 45, arcade.color.BLACK, 25, font_name=settings.MAIN_FONT_NAME)
            arcade.draw_text(f"Pays: {self.document.country}", 370, start_y - 90, arcade.color.BLACK, 25, font_name=settings.MAIN_FONT_NAME)