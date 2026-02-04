import arcade
from pathlib import Path

# Localiser le fichier TownKeeper/
BASE_DIR = Path(__file__).resolve().parent

# Localise la racine du projet
PROJECT_ROOT = BASE_DIR.parent

# Chemin aboslu vers le dossier assets
ASSETS_PATH = PROJECT_ROOT / "assets"

# --- Fenêtre et Titre ---
SCREEN_WIDTH = 1400
SCREEN_HEIGHT =  850
SCREEN_TITLE = "The Townkeeper"

# --- Couleurs Thématiques ---
COLOR_BACKGROUND = arcade.color.APPLE_GREEN
COLOR_TEXT_DARK = arcade.color.DARK_LIVER
COLOR_STAMP_RED = arcade.color.BARN_RED
COLOR_GOLD = arcade.color.GOLDEN_POPPY
COLOR_FONT = arcade.color.BLACK
COLOR_FONT_RULE = arcade.color.DARK_RED
COLOR_FONT_END_DAY = arcade.color.DARK_LIVER
COLOR_FONT_GOLD = arcade.color.GOLDENROD

# --- Equilibage du Gameplay (Game Design) ---
STARTING_GOLD = 20
DAILY_RENT = 10
UNPAID_RENT = 0 # Pour te faire virer de ton logement
DAILY_FOOD = 5
UNPAID_FOOD = 0 # Jour avant la mort de faim de ta famille
MAX_TRUST = 100
MIN_TRUST = 0
FORGERY_CHANCE = 0.3 # Chance que le document soit faux
VISITORS_PER_DAY = 2

# --- Positions UI (A partir de en bas a gauche) ---
UI_SCORE_POS = (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 50)
UI_PASSPORT_POS = (400,250)
UI_DECREE_POS = (50, SCREEN_HEIGHT - 100)

# --- Couleurs Boutons ---
COLOR_BTN_ACCEPT = arcade.color.APPLE_GREEN
COLOR_BTN_REJECT = arcade.color.BARN_RED
COLOR_BTN_TEXT =arcade.color.WHITE

# --- Dimensions ---
BTN_WIDTH = 250
BTN_HEIGHT = 60
DESK_HEIGHT = 465

# --- Police d'écriture ---
START_FONT_NAME = "Deutsch Gothic" 
MAIN_FONT_NAME = "Deutsch Gothic"
MENU_FONT_NAME = "Kenney Future"

# --- Données des personnages ---
NAMES = [
    "Ivan", 
    "Marta", 
    "Sergei", 
    "Anna"
]
ROLES = [
    "Marchand",
    "Pèlerin", 
    "Artisan", 
    "Barde",
    "Mage",
    "Chevalier",
    "Paysan",
]
COUNTRIES = [
    "Franc", 
    "Saint-Empire", 
    "Saxon",
    "Rus de Kiev"
]
STORIES = [
    "Je voyage pour affaire",
]
COUNTRY_SIGNS = {
    "Gaule" :"Soleil",
    "Saint-Empire": "Aigle",
    "Italie": "Couronnre",
}
