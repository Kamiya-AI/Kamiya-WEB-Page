import json, re

path = r'c:\Users\misam\OneDrive\デスクトップ\AI関係資料\記憶の保管庫\WEB制作\神谷じんいちろう_Portfolio\assets\js\script.js'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract portfolioData JSON array
match = re.search(r'const portfolioData = (\[.*?\]);', content, flags=re.DOTALL)
if match:
    data = json.loads(match.group(1))
    # Remove カラーアニメ風タッチ
    data = [item for item in data if 'カラーアニメ風タッチ' not in item.get('title', '')]
    new_json = json.dumps(data, ensure_ascii=False, indent=4)
    new_content = content[:match.start()] + 'const portfolioData = ' + new_json + ';' + content[match.end():]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('Done - removed カラーアニメ風タッチ')
    print('Remaining items:')
    for item in data:
        print('  ' + item['title'])
else:
    print('ERROR: portfolioData not found')
