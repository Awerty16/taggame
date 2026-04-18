import os
import glob
import re

html_file = "/Users/aidenmathew/Desktop/antigravity/gclass/index.html"
games_dir = "/Users/aidenmathew/Desktop/antigravity/gclass/games"

games = glob.glob(os.path.join(games_dir, "*.html"))

three_kept = """
        <a href="soccer.html" class="drawer-app" data-game="soccer" id="appSoccer">
          <div class="drawer-app-icon icon-soccer">⚽</div>
          <div class="drawer-app-name">Soccer</div>
        </a>

        <a href="tag.html" class="drawer-app" data-game="tag" id="appTag">
          <div class="drawer-app-icon icon-tag">🏃</div>
          <div class="drawer-app-name">Tag</div>
        </a>

        <a href="basketrandom.html" class="drawer-app" data-game="basketball" id="appBasketball">
          <div class="drawer-app-icon icon-basketball">🏀</div>
          <div class="drawer-app-name">Basket Random</div>
        </a>
"""

coming_soon = """
        <div class="drawer-app disabled" data-game="coming" id="appComing1">
          <div class="drawer-app-icon icon-coming">🧩</div>
          <div class="drawer-app-name">Puzzle</div>
          <div class="drawer-app-badge">Soon</div>
        </div>

        <div class="drawer-app disabled" data-game="coming" id="appComing2">
          <div class="drawer-app-icon icon-coming">🏎️</div>
          <div class="drawer-app-name">Racing</div>
          <div class="drawer-app-badge">Soon</div>
        </div>

        <div class="drawer-app disabled" data-game="coming" id="appComing3">
          <div class="drawer-app-icon icon-coming">🎯</div>
          <div class="drawer-app-name">Archery</div>
          <div class="drawer-app-badge">Soon</div>
        </div>

        <div class="drawer-app disabled" data-game="coming" id="appComing4">
          <div class="drawer-app-icon icon-coming">🪐</div>
          <div class="drawer-app-name">Space Run</div>
          <div class="drawer-app-badge">Soon</div>
        </div>
"""

generated_games = []
# Ensure alphabetical sorting nicely
games.sort(key=lambda x: os.path.basename(x).lower())

for filepath in games:
    filename = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    title_match = re.search(r'<title>(.*?)</title>', content)
    if title_match:
        name = title_match.group(1).replace('- gswitch3.github.io', '').strip()
    else:
        name = filename.replace('.html', '').replace('-', ' ').title()
        
    game_id = filename.replace('.html', '')
    
    # generate a consistent hsl color for the icon background based on filename
    h1 = (hash(filename) % 360)
    h2 = (h1 + 40) % 360
    
    icon_content = "🎮"
    
    item = f'''
        <a href="games/{filename}" class="drawer-app" data-game="{game_id}">
          <div class="drawer-app-icon" style="background: linear-gradient(135deg, hsl({h1}, 80%, 60%), hsl({h2}, 80%, 50%))">{icon_content}</div>
          <div class="drawer-app-name">{name}</div>
        </a>'''
    generated_games.append(item)

all_items = three_kept + "".join(generated_games) + coming_soon

with open(html_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1

# Find boundaries
for i, line in enumerate(lines):
    if '<div class="drawer-grid" id="drawerGrid">' in line:
        start_idx = i + 1
    if start_idx != -1 and i > start_idx:
        # Looking for the closing tag of drawer-grid
        if '      </div>' in line and '<!-- Footer -->' in "".join(lines[i:i+5]):
            end_idx = i
            break

if start_idx != -1 and end_idx != -1:
    new_lines = lines[:start_idx] + [all_items + "\n"] + lines[end_idx:]
    
    # Update count
    total_games = len(generated_games) + 3
    for i, line in enumerate(new_lines):
        if 'games available' in line and 'drawer-footer-text' not in line:
            # Find the span dot inside the footer to keep structure, or just replace the text node
            new_lines[i] = f"        {total_games} games available\n"

    with open(html_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print(f"Successfully integrated {len(generated_games)} games from games/ into index.html")
    print(f"Total count is now {total_games}")
else:
    print(f"Error: Could not find boundaries. start_idx={start_idx}, end_idx={end_idx}")
