import struct
from pathlib import Path
import settings  # On importe vos réglages pour avoir le chemin EXACT

def get_font_name(font_path):
    """Lit le nom de famille interne d'un fichier TTF."""
    path = Path(font_path)
    if not path.exists():
        return f"ERREUR: Fichier introuvable au chemin -> {path}"

    with open(path, 'rb') as f:
        data = f.read()

    # Lecture de l'en-tête TTF pour trouver la table 'name'
    try:
        num_tables = struct.unpack('>H', data[4:6])[0]
        name_offset = None
        
        for i in range(num_tables):
            off = 12 + i * 16
            tag = data[off:off+4]
            if tag == b'name':
                name_offset = struct.unpack('>I', data[off+8:off+12])[0]
                break
        
        if not name_offset: 
            return "Table 'name' introuvable."
        
        # Lecture de la table 'name'
        count, string_offset = struct.unpack('>HH', data[name_offset+2:name_offset+6])
        string_data_start = name_offset + string_offset
        
        names = set()
        for i in range(count):
            off = name_offset + 6 + i * 12
            pid, eid, lid, nid, length, string_off = struct.unpack('>HHHHHH', data[off:off+12])
            
            # NameID 1 = Famille
            if nid == 1: 
                str_bytes = data[string_data_start + string_off : string_data_start + string_off + length]
                try:
                    # Décodage (souvent UTF-16BE pour les TTF)
                    decoded = str_bytes.decode('utf-16-be' if pid == 3 else 'latin-1')
                    decoded = decoded.replace('\x00', '')
                    names.add(decoded)
                except:
                    pass
        
        return list(names)

    except Exception as e:
        return f"Erreur de lecture : {e}"

# --- Test des fichiers avec le chemin ABSOLU de settings.py ---
print("--- ANALYSE DES POLICES ---")

# On construit le chemin grâce à settings.ASSETS_PATH
path_deutsch = settings.ASSETS_PATH / "fonts" / "Deutsch.ttf"
path_ruritania = settings.ASSETS_PATH / "fonts" / "Ruritania.ttf"

print(f"Dossier Assets détecté : {settings.ASSETS_PATH}")
print("Deutsch   :", get_font_name(path_deutsch))
print("Ruritania :", get_font_name(path_ruritania))
print("---------------------------")