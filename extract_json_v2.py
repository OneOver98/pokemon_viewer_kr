import json
import os

def extract_en(val):
    parts = val.split('/')
    return parts[-1].strip()

def make_pvpoke_move(move):
    if move in ["-", "", "None"]: return ""
    return extract_en(move).upper().replace(" ", "_")

def load_gamemaster():
    gamemaster_path = r"c:\Users\jake\ai_1o\pvpoke\src\data\gamemaster.json"
    poke_types = {}
    move_types = {}
    
    with open(gamemaster_path, 'r', encoding='utf-8') as f:
        gm = json.load(f)
        
    for p in gm.get('pokemon', []):
        poke_types[p.get('speciesId')] = p.get('types', [])
        poke_types[p.get('speciesName', '').lower()] = p.get('types', [])
        
    for m in gm.get('moves', []):
        move_types[m.get('moveId')] = m.get('type', 'none')
        
    return poke_types, move_types

def get_pvpoke_id(eng_name, raw_name, raw_form, raw_app):
    pvpoke_id = eng_name.lower().replace(" ", "")
    is_shadow = "Shadow" in raw_app
    is_alolan = "Alola" in raw_form or "Alola" in raw_name
    is_galarian = "Galar" in raw_form or "Galar" in raw_name
    is_hisuian = "Hisui" in raw_form or "Hisui" in raw_name
    
    if is_alolan: pvpoke_id += "_alolan"
    if is_galarian: pvpoke_id += "_galarian"
    if is_hisuian: pvpoke_id += "_hisuian"
    if is_shadow: pvpoke_id += "_shadow"
    
    return pvpoke_id

def parse_pvpoke_data():
    poke_types_map, move_types_map = load_gamemaster()
    
    with open('processed_info.md', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    players = {}
    current_player = None
    
    for line in lines:
        line = line.strip()
        if not line: continue
        parts = line.split('\t')
        
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
            
            fast = make_pvpoke_move(parts[6].strip('"'))
            charge1 = make_pvpoke_move(parts[7].strip('"'))
            charge2 = make_pvpoke_move(parts[8].strip('"'))
            cp = parts[4].strip('"')
            hp = parts[5].strip('"')
            
            pvpoke_id = get_pvpoke_id(eng_name, raw_name, raw_form, raw_app)
            
            # Lookup Types
            types = poke_types_map.get(pvpoke_id, poke_types_map.get(eng_name.lower(), ["none", "none"]))
            if len(types) == 1: types.append("none")
            
            fast_type = move_types_map.get(fast, "none")
            c1_type = move_types_map.get(charge1, "none")
            if charge1 == "HIDDEN_POWER_BUG": c1_type = "bug"
            elif charge1.startswith("HIDDEN_POWER"): c1_type = charge1.split("_")[-1].lower()
            
            c2_type = move_types_map.get(charge2, "none")
            if charge2.startswith("HIDDEN_POWER"): c2_type = charge2.split("_")[-1].lower()
            
            is_shadow = "Shadow" in raw_app
            is_alolan = "Alola" in raw_form or "Alola" in raw_name
            is_galarian = "Galar" in raw_form or "Galar" in raw_name
            is_hisuian = "Hisui" in raw_form or "Hisui" in raw_name
            
            pvpoke_name = eng_name
            if is_alolan: pvpoke_name = f"Alolan {pvpoke_name}"
            if is_galarian: pvpoke_name = f"Galarian {pvpoke_name}"
            if is_hisuian: pvpoke_name = f"Hisuian {pvpoke_name}"
            if is_shadow: pvpoke_name = f"{pvpoke_name} (Shadow)"
            
            moves = [m for m in [fast, charge1, charge2] if m]
            export_str = f"{pvpoke_name},{','.join(moves)}"
            
            current_player['pokemon'].append({
                "raw_name": raw_name,
                "eng_name": eng_name,
                "pvpoke_name": pvpoke_name,
                "fast_move": fast,
                "fast_type": fast_type,
                "charge1": charge1,
                "charge1_type": c1_type,
                "charge2": charge2,
                "charge2_type": c2_type,
                "cp": cp,
                "hp": hp,
                "is_shadow": is_shadow,
                "types": types,
                "export_str": export_str
            })

    os.makedirs('pvpoke-viewer_v2', exist_ok=True)
    with open('pvpoke-viewer_v2/data.json', 'w', encoding='utf-8') as f:
        json.dump(list(players.values()), f, ensure_ascii=False, indent=2)
        
    print(f"Successfully exported {len(players)} players to pvpoke-viewer_v2/data.json")

if __name__ == "__main__":
    parse_pvpoke_data()
