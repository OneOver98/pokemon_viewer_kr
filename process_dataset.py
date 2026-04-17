import sys

def process_file(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    out_lines = []
    counter = 1

    for line in lines:
        line = line.rstrip('\n')
        if not line:
            # Skip genuinely empty lines (e.g. EOF)
            continue
            
        parts = line.split('\t')
        
        # Player+Pokemon combined line
        if len(parts) >= 13:
            # First 5 are: Index, GamerTag, Discord ID, Trainer Name, Trainer Code
            line_a = [f'"{counter}"'] + parts[1:5]
            out_lines.append('\t'.join(line_a))
            counter += 1
            
            # Remaining parts are Pokemon Info
            line_b = [f'"{counter}"'] + parts[5:]
            out_lines.append('\t'.join(line_b))
            counter += 1
        else:
            # Normal single line (just Pokemon, or special header like "Player" "Pokemon")
            line_a = [f'"{counter}"'] + parts[1:]
            out_lines.append('\t'.join(line_a))
            counter += 1

    with open(output_path, "w", encoding="utf-8") as f:
        for o in out_lines:
            f.write(o + '\n')
            
    print("Processed successfully!")
    for i in range(min(15, len(out_lines))):
        print(out_lines[i])

if __name__ == "__main__":
    process_file("raw_info.md", "processed_info.md")
