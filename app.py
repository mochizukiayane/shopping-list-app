import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# データの保存ファイル
DATA_FILE = 'shopping_list.json'

def load_data():
    """データをJSONファイルから読み込む"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # ファイルがないか、内容が不正な場合は初期データを返す
        return {
            "budget": 26000,
            "items": {
                "飲み物": [],
                "おつまみ": [],
                "弁当": [],
                "雑貨": []
            }
        }

def save_data(data):
    """データをJSONファイルに保存する"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route('/')
def index():
    """メイン画面を表示"""
    data = load_data()
    return render_template('index.html', data=data)

@app.route('/add_item', methods=['POST'])
def add_item():
    """商品を追加"""
    data = load_data()
    item_data = request.json
    category = item_data['category']
    
    # 既存の商品かチェック
    for item in data['items'][category]:
        if item['name'] == item_data['name']:
            item['quantity'] += int(item_data['quantity'])
            save_data(data)
            return jsonify({'success': True, 'message': '数量を更新しました。'})

    # 新しい商品として追加
    item = {
        'name': item_data['name'],
        'price': int(item_data['price']),
        'quantity': int(item_data['quantity'])
    }
    data['items'][category].append(item)
    save_data(data)
    return jsonify({'success': True, 'message': '商品を追加しました。'})

@app.route('/update_budget', methods=['POST'])
def update_budget():
    """予算を更新"""
    data = load_data()
    budget = request.json['budget']
    data['budget'] = int(budget)
    save_data(data)
    return jsonify({'success': True})

@app.route('/delete_item', methods=['POST'])
def delete_item():
    """商品を削除"""
    data = load_data()
    item_data = request.json
    category = item_data['category']
    item_name = item_data['name']
    
    # 該当する商品をリストから削除
    data['items'][category] = [item for item in data['items'][category] if item['name'] != item_name]
    save_data(data)
    return jsonify({'success': True})

@app.route('/update_quantity', methods=['POST'])
def update_quantity():
    """商品の個数を更新"""
    data = load_data()
    item_data = request.json
    category = item_data['category']
    item_name = item_data['name']
    new_quantity = int(item_data['quantity'])
    
    for item in data['items'][category]:
        if item['name'] == item_name:
            item['quantity'] = new_quantity
            save_data(data)
            return jsonify({'success': True})
    return jsonify({'success': False, 'message': '商品が見つかりません。'})


if __name__ == '__main__':
    app.run(debug=True)