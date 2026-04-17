# AI Prompt: Build a Pokémon Team Viewer Web App

You are an expert web developer tasked with creating a "Pokémon Team Viewer" application. Your goal is to build a web-based tool that allows users to search for players and view their 6-Pokémon teams exactly as they would appear in the PvPoke battle simulator. 

## Technical Stack
- Vanilla HTML, CSS, and JavaScript.
- No heavy frameworks (like React or Angular) are necessary; keep it lightweight and fast.
- You will be working with four main files: `index.html`, `style.css`, `app.js`, and a `data.json` file which contains the dataset.

## Core Features and Requirements

1. **Player Search Functionality**:
   - The user interface must include a search bar where users can look up a specific player by name.
   - The app should parse the `data.json` dataset to find matching players and their respective teams.

2. **6-Pokémon Team Display**:
   - Display the player's 6-Pokémon team when selected.
   - The team layout and visual representation must closely mimic the format used by the open-source **PvPoke battle simulator** (including species names, stats, moves, CP, and typical Pokemon sprites).

3. **PvPoke Export "Copy" Feature**:
   - Include a prominently featured "Copy" button for the team.
   - When clicked, this button should generate and copy to the user's clipboard a **standard PvPoke-compatible team export string**.
   - This ensures seamless integration, allowing users to paste the copied string directly into the PvPoke engine.

4. **Modern, Glassmorphic UI**:
   - Design the application using modern aesthetic principles. 
   - Feature a **glassmorphism** design scheme: translucent backgrounds, subtle frosted glass effects, layered UI, vibrant yet harmonious gradients in the background, readable modern typography (like Inter or Roboto).
   - Use dynamic hover effects and micro-animations to make the interface feel responsive and alive. Ensure it feels like a premium app.

5. **Responsiveness**:
   - Ensure the layout is fully responsive and looks stunning on both desktop and mobile devices. 
   - The 6-Pokémon team grid should gracefully wrap or collapse depending on screen width.

## Step-by-Step Implementation Approach

1. **Setup Core HTML (`index.html`)**: Build the semantic skeleton, including the search container, the display area for the 6 Pokémon, and the copy button. Include references to `style.css` and `app.js`.
2. **Implement Glassmorphic Styling (`style.css`)**: Add your CSS variables, the dynamic gradient backgrounds, the frosted glass UI component styles (`backdrop-filter: blur()`), and responsive flex/grid layouts.
3. **Data Loading and Logic (`app.js`)**: 
   - Fetch the player data from `data.json`.
   - Implement the search filtering logic.
   - Dynamically render the team interface into the DOM based on search results.
   - Implement the export string generation logic and copy-to-clipboard functionality.

Please generate the complete, ready-to-run code for `index.html`, `style.css`, and `app.js` based on these specifications.
