import json
import re
import os

def clean_name(name):
    # Usually we just lowercase and replace spaces with nothing or hyphen? PvPoke uses hyphens for names? No, mostly just the word or specific mapping.
    # Example: "Clefable" -> "clefable", "Ho-Oh" -> "ho_oh_shadow" (depends, but export string accepts "Clefable")
    # For export strings in PvPoke CSV, it's very forgiving! "Clefable", "Alolan Ninetales (Shadow)" works too!
    # But let's build the optimal string format.
    return name.strip()

def extract_en(val):
    # e.g., "불새 / Sky Attack" -> "Sky Attack"
    parts = val.split('/')
    return parts[-1].strip()

def extract_ko(val):
    parts = val.split('/')
    return parts[0].strip()

def make_pvpoke_move(move):
    if move in ["-", "", "None"]: return ""
    return extract_en(move).upper().replace(" ", "_")

def parse_pvpoke_data():
    with open('processed_info.md', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    players = {}
    current_player = None
    
    for line in lines:
        line = line.strip()
        if not line: continue
        parts = line.split('\t')
        
        # Player line length is 5
        if len(parts) == 5:
            if "GamerTag" in parts[1]:
                continue
            current_player = {
                "gamertag": parts[1].strip('"'),
                "discord_id": parts[2].strip('"'),
                "trainer_name": parts[3].strip('"'),
                "trainer_code": parts[4].strip('"'),
                "pokemon": []
            }
            # Key to uniquely identify (user requested search by player name)
            search_key = current_player['trainer_name'] if current_player['trainer_name'] else current_player['gamertag']
            players[search_key] = current_player
            
        elif len(parts) == 9 and current_player is not None:
            if "Name" in parts[1]:
                continue
            
            raw_name = parts[1].strip('"')
            raw_form = parts[2].strip('"')
            raw_app = parts[3].strip('"')
            
            eng_name = extract_en(raw_name)
            eng_form = extract_en(raw_form)
            eng_app = extract_en(raw_app)
            
            # Moves
            fast = make_pvpoke_move(parts[6].strip('"'))
            charge1 = make_pvpoke_move(parts[7].strip('"'))
            charge2 = make_pvpoke_move(parts[8].strip('"'))
            cp = parts[4].strip('"')
            
            # Construct PvPoke Name for the Export String
            # PvPoke handles "Malamar" or "Ninetales (Alolan)" and "Malamar (Shadow)"
            pvpoke_name = eng_name
            is_shadow = "Shadow" in eng_app
            is_alolan = "Alolan" in eng_form or "Alola" in eng_form or "Alola" in eng_name
            is_galarian = "Galarian" in eng_form or "Galar" in eng_form or "Galar" in eng_name
            is_hisuian = "Hisuian" in eng_form or "Hisui" in eng_form or "Hisui" in eng_name
            
            # Append forms correctly for standard string format
            if is_alolan: pvpoke_name = f"Alolan {pvpoke_name}"
            if is_galarian: pvpoke_name = f"Galarian {pvpoke_name}"
            if is_hisuian: pvpoke_name = f"Hisuian {pvpoke_name}"
            if is_shadow: pvpoke_name = f"{pvpoke_name} (Shadow)"
            
            # Build the custom CSV string line
            # Format: Name,FAST,CHARGE1,CHARGE2
            moves = [m for m in [fast, charge1, charge2] if m]
            export_str = f"{pvpoke_name},{','.join(moves)}"
            
            current_player['pokemon'].append({
                "raw_name": raw_name,
                "eng_name": eng_name,
                "pvpoke_name": pvpoke_name,
                "fast_move": fast,
                "charge1": charge1,
                "charge2": charge2,
                "cp": cp,
                "export_str": export_str
            })

    os.makedirs('pvpoke-viewer', exist_ok=True)
    with open('pvpoke-viewer/data.json', 'w', encoding='utf-8') as f:
        json.dump(list(players.values()), f, ensure_ascii=False, indent=2)
        
    print(f"Successfully exported {len(players)} players to pvpoke-viewer/data.json")

if __name__ == "__main__":
    parse_pvpoke_data()
