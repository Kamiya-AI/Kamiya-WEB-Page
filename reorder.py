import json, re

path = r'c:\Users\misam\OneDrive\デスクトップ\AI関係資料\記憶の保管庫\WEB制作\神谷じんいちろう_Portfolio\assets\js\script.js'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'const portfolioData = (\[.*?\]);', content, flags=re.DOTALL)
if not match:
    print('ERROR: portfolioData not found')
    exit()

data = json.loads(match.group(1))

# Desired order by current title
order = [
    '少年漫画カラータッチ',
    'ミステリアスタッチ1',
    'ミステリアスタッチ2',
    'ミステリアスカラータッチ',
    'モノクロ青年漫画タッチ',
    'モノクロ少年漫画タッチ',
    '少年漫画バトルタッチ',
    '墨モノクロ肉質タッチ',
    'ゆるキャラアニメタッチ',
    '水彩タッチ',
    'LP漫画',
]

# Rename map
rename_map = {
    '墨モノクロ肉質タッチ': ('黒モノクロ肉質タッチ', '黒モノクロ肉質タッチ'),
    'LP漫画': ('LP漫画例', 'LP漫画例'),
}

# Build lookup
lookup = {}
for item in data:
    lookup[item['title']] = item

sorted_data = []
for i, title in enumerate(order, 1):
    if title in lookup:
        item = lookup[title]
        item['id'] = 'manga' + str(i)
        # Apply rename
        if title in rename_map:
            new_title, new_tag = rename_map[title]
            item['title'] = new_title
            item['tag'] = item['tag'].replace(title, new_title)
        sorted_data.append(item)
    else:
        print('WARNING: not found: ' + title)

new_json = json.dumps(sorted_data, ensure_ascii=False, indent=4)
new_content = content[:match.start()] + 'const portfolioData = ' + new_json + ';' + content[match.end():]

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Done - reordered and renamed')
for item in sorted_data:
    print('  ' + item['id'] + ': ' + item['title'] + ' (' + item['category'] + ')')
