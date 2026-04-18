import os
import re
import glob

# Path to the games folder
games_dir = "/Users/aidenmathew/Desktop/antigravity/gclass/games"
html_files = glob.glob(os.path.join(games_dir, "*.html"))

template = """<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
  <title>{title}</title>
  <style>
    body, html {{ 
      margin: 0; 
      padding: 0; 
      width: 100%; 
      height: 100%; 
      overflow: hidden; 
      background-color: #000; 
    }}
    iframe {{ 
      width: 100%; 
      height: 100%; 
      border: none; 
    }}
  </style>
</head>
<body>
  <iframe src="{src}" scrolling="none" frameborder="0" allowfullscreen></iframe>
</body>
</html>
"""

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract title
    title_match = re.search(r'<title>(.*?)</title>', content)
    title = title_match.group(1) if title_match else "Game"

    # Extract iframe src
    iframe_match = re.search(r'<iframe[^>]*id="game-area"[^>]*src="([^"]+)"', content)
    if not iframe_match:
        iframe_match = re.search(r'<iframe[^>]*class="game-iframe"[^>]*src="([^"]+)"', content)
        
    if not iframe_match:
        print(f"Skipping (no game iframe found): {os.path.basename(filepath)}")
        return False
        
    src = iframe_match.group(1)
    
    # Generate new HTML content
    new_content = template.format(title=title, src=src)
    
    # Write the clean template back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    return True

success_count = 0
for filepath in html_files:
    if process_file(filepath):
        success_count += 1

print(f"Processed {success_count} out of {len(html_files)} files successfully.")
