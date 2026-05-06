import os, json, urllib.parse, re

base = r'c:\Users\misam\OneDrive\デスクトップ\AI関係資料\記憶の保管庫\WEB制作\神谷じんいちろう_Portfolio\assets\images\portfolio'
script_path = r'c:\Users\misam\OneDrive\デスクトップ\AI関係資料\記憶の保管庫\WEB制作\神谷じんいちろう_Portfolio\assets\js\script.js'

folders = sorted([d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d))])

color_keywords = ['カラー', 'ゆるキャラ', 'アニメ', '水彩', 'LP']
mono_keywords = ['モノクロ', '墨']
other_keywords = ['ミステリアス']

def get_category(name):
    for kw in other_keywords:
        if kw in name:
            return 'other'
    for kw in mono_keywords:
        if kw in name:
            return 'mono-manga'
    for kw in color_keywords:
        if kw in name:
            return 'color-manga'
    return 'color-manga'

def sort_key(f):
    nums = re.findall(r'(\d+)', f)
    return int(nums[0]) if nums else f

data = []
for i, folder in enumerate(folders, 1):
    folder_path = os.path.join(base, folder)
    files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif'))]
    files.sort(key=sort_key)
    if not files:
        continue
    encoded_folder = urllib.parse.quote(folder)
    pages = []
    for f in files:
        encoded_file = urllib.parse.quote(f)
        pages.append("assets/images/portfolio/" + encoded_folder + "/" + encoded_file)
    tag = folder
    title = folder.split('(')[0].strip()
    category = get_category(folder)
    data.append({
        'id': 'manga' + str(i),
        'category': category,
        'tag': tag,
        'title': title,
        'cover': pages[0],
        'pages': pages
    })

# Read current script.js
with open(script_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Build replacement JSON
json_str = json.dumps(data, ensure_ascii=False, indent=4)

# Replace the portfolioData array
pattern = r'const portfolioData = \[.*?\];'
replacement = 'const portfolioData = ' + json_str + ';'
new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open(script_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated script.js with " + str(len(data)) + " portfolio items")
for item in data:
    print("  " + item["id"] + ": " + item["title"] + " (" + item["category"] + ") - " + str(len(item["pages"])) + " pages")
