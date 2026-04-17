import os
import re
import random

root_dir = '.'
html_files = [f for f in os.listdir(root_dir) if f.endswith('.html') and f not in ('index.html', 'soccer.html', 'tag.html', 'basketrandom.html')]
html_files.sort()

# Read current index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# We will format the new games into a string
new_games_html = ""
for f in html_files:
    # get a title
    with open(f, 'r', encoding='utf-8') as file:
        f_content = file.read()
    title_match = re.search(r'<title>([^<]+)</title>', f_content, re.IGNORECASE)
    title = title_match.group(1).strip() if title_match else f.replace('.html', '').replace('-', ' ').title()
    
    game_id = f.replace('.html', '')
    
    # generate random gradient colors
    h = random.randint(0, 360)
    bg = f"background: linear-gradient(135deg, hsl({h}, 80%, 60%), hsl({(h+40)%360}, 80%, 50%))"
    emoji = "🎮"
    
    new_games_html += f'''
        <a href="{f}" class="drawer-app" data-game="{game_id}">
          <div class="drawer-app-icon" style="{bg}">{emoji}</div>
          <div class="drawer-app-name">{title}</div>
        </a>
'''

# Find the insertion point: immediately before the coming soon disabled apps
# Let's insert after <div class="drawer-grid" id="drawerGrid"> 
# and existing soccer/tag basketrandom games

# Find <div class="drawer-app disabled" data-game="coming" id="appComing1">
insert_marker = '<div class="drawer-app disabled" data-game="coming" id="appComing1">'

if insert_marker in content:
    parts = content.split(insert_marker)
    new_content = parts[0] + new_games_html + insert_marker + parts[1]
    
    # Also update the footer text to reflect total games
    total_games = 3 + len(html_files)
    new_content = re.sub(r'(\d+)\s+games\s+available', f'{total_games} games available', new_content)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Added {len(html_files)} games. Total games: {total_games}")
else:
    print("Could not find insertion point!")
