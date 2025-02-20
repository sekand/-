import tkinter as tk
from tkinter import messagebox
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import rcParams

# フォント設定 (日本語対応)
font = ("Yu Gothic", 10)  # Tkinter用の日本語フォント
rcParams['font.family'] = 'Yu Gothic'  # matplotlib用の日本語フォント設定

# 初期設定
initial_price = 100  # 初期株価
turns = 20  # ゲームのターン数
prices = [initial_price]
trend = random.choice([-1, 1])  # 上昇 or 下降トレンド
cash = 1000  # 初期資金
stock_owned = 0  # 初期株数
current_turn = 1  # 現在のターン
event_message = ""  # イベントメッセージ
bubble_turns_remaining = 0  # バブル崩壊までのターン数

# プレイヤーの行動
def player_action(action, current_price):
    global cash, stock_owned, event_message
    event_message = ""  # イベントメッセージを初期化
    
    if action == "buy":  # 株を買う
        max_shares = cash // current_price  
        try:
            shares_to_buy = int(shares_entry.get())  
            if 0 < shares_to_buy <= max_shares:
                cash -= shares_to_buy * current_price
                stock_owned += shares_to_buy
                event_message = f"{shares_to_buy} 株を購入しました。"
            else:
                event_message = f"無効な株数です。最大で {max_shares} 株購入できます。"
        except ValueError:
            event_message = "無効な入力です。数字を入力してください。"
    
    elif action == "sell":  # 株を売る
        try:
            shares_to_sell = int(shares_entry.get())  # プレイヤーが指定した株数
            if 0 < shares_to_sell <= stock_owned:
                cash += shares_to_sell * current_price
                stock_owned -= shares_to_sell
                event_message = f"{shares_to_sell} 株を売却しました。"
            else:
                event_message = f"無効な株数です。最大で {stock_owned} 株売却できます。"
        except ValueError:
            event_message = "無効な入力です。数字を入力してください。"

# ランダムイベントの発生
def trigger_event():
    global event_message, bubble_turns_remaining, stock_owned
    event_chance = random.random()  
    if event_chance < 0.5:  # 10%の確率でイベントが発生
        event_type = random.choice(['earnings', 'crisis', 'bubble', 'recovery', 'intervention', 'disaster', 'split', 'new_product'])
        if event_type == 'earnings':
            event_message = "企業業績発表: 予想より良い業績発表で株価が上昇しました！"
            return random.uniform(5, 20)  # 株価が上昇
        elif event_type == 'crisis':
            event_message = "金融危機: 株価が急落しました！"
            return random.uniform(-30, -50)  # 株価が急落
        elif event_type == 'bubble':
            event_message = "バブル: 株価が急上昇し、その後崩壊します！"
            bubble_turns_remaining = random.randint(1, 3)  # バブル崩壊までのターン数を設定
            return random.uniform(30, 50)  # 株価が急上昇
        elif event_type == 'recovery':
            event_message = "景気回復: 市場全体が好転し、株価が上昇しました！"
            return random.uniform(10, 25)  # 市場全体が上昇
        elif event_type == 'intervention':
            event_message = "政府の介入: 政府が株式市場に介入し、株価が急上昇しました！"
            return random.uniform(20, 40)  # 株価が急上昇
        elif event_type == 'disaster':
            event_message = "自然災害: 自然災害が発生し、株価が急落しました！"
            return random.uniform(-20, -40)  # 株価が急落
        elif event_type == 'split':
            event_message = "株式分割: 株式が分割され、株価は下がりましたが、株数は増えました！"
            stock_owned = round(stock_owned * 1.1)
            return random.uniform(-5, -10)  # 株価が下がるが、株数は増加
        elif event_type == 'new_product':
            event_message = "新製品発表: 企業が新製品を発表し、株価が急上昇しました！"
            return random.uniform(15, 30)  # 株価が急上昇
    return 0  # イベントなしの場合は0を返す

# 株価シミュレーション（イベントを組み込む）
def simulate_stock_with_events():
    global cash, stock_owned, prices, trend, current_turn, event_message, bubble_turns_remaining
    if current_turn > turns:
        final_result()
        return
    
    current_price = prices[-1]
    
    # プレイヤーのアクション
    action = action_var.get()
    player_action(action, current_price)
    
    # ランダムイベント発生
    event_effect = trigger_event()
    if event_effect != 0:
        current_price += event_effect  # イベントによる株価の変動
    
    # バブル崩壊の処理
    if bubble_turns_remaining > 0:
        bubble_turns_remaining -= 1
        if bubble_turns_remaining == 0:
            event_message = "バブル崩壊: 株価が急落しました！"
            current_price += random.uniform(-50, -70)  # バブル崩壊による急落
    
    # 株価の変動
    change = random.uniform(-5, 5) + trend  # イベントの影響も加える
    new_price = max(1, round(current_price + change, 2))  # 小数点以下2桁に制限
    prices.append(new_price)

    # トレンド変化
    if random.random() < 0.2:
        trend *= -1
    
    # 更新された情報を表示
    update_gui(new_price)
    current_turn += 1

def final_result():
    total_assets = cash + stock_owned * prices[-1]
    result_message = f"ゲーム終了！\n最終資産: {round(total_assets, 2)} 円\n現金: {round(cash, 2)} 円\n保有株数: {stock_owned} 株\n最終株価: {round(prices[-1], 2)} 円"
    messagebox.showinfo("最終結果", result_message)
    window.quit()  # GUIを閉じる

def update_gui(new_price):
    # GUIの更新
    price_label.config(text=f"株価: {new_price}")
    cash_label.config(text=f"現金: {round(cash, 2)}")
    stock_label.config(text=f"保有株数: {stock_owned}")
    turn_label.config(text=f"ターン: {current_turn}")
    
    event_label.config(text=f"イベント: {event_message}")  # イベントメッセージを表示
    
    # 株価の推移グラフを更新
    ax.clear()
    ax.plot(prices, marker='o', linestyle='-')
    ax.set_xlabel('ターン')
    ax.set_ylabel('株価')
    ax.set_title('株価シミュレーション')
    canvas.draw()
    
    # 次のターンボタンを再表示
    simulate_button.grid(row=5, column=0, columnspan=3)  # 修正: ボタンの行を変更して確実に再表示

# GUIのセットアップ
window = tk.Tk()
window.title("株価シミュレーションゲーム")

# ラベルの配置
turn_label = tk.Label(window, text=f"ターン: {current_turn}", font=font)
turn_label.grid(row=0, column=0)

price_label = tk.Label(window, text=f"株価: {round(initial_price, 2)}", font=font)
price_label.grid(row=0, column=1)

cash_label = tk.Label(window, text=f"現金: {round(cash, 2)}", font=font)
cash_label.grid(row=1, column=0)

stock_label = tk.Label(window, text=f"保有株数: {stock_owned}", font=font)
stock_label.grid(row=1, column=1)

# アクション選択ラジオボタン
action_var = tk.StringVar(value="buy")
buy_button = tk.Radiobutton(window, text="株を買う", variable=action_var, value="buy", font=font)
buy_button.grid(row=2, column=0)

sell_button = tk.Radiobutton(window, text="株を売る", variable=action_var, value="sell", font=font)
sell_button.grid(row=2, column=1)

hold_button = tk.Radiobutton(window, text="何もしない", variable=action_var, value="hold", font=font)
hold_button.grid(row=2, column=2)

# 株数入力フィールド
shares_label = tk.Label(window, text="株数:", font=font)
shares_label.grid(row=3, column=0)

shares_entry = tk.Entry(window, font=font)
shares_entry.grid(row=3, column=1)

# イベントメッセージ表示
event_label = tk.Label(window, text="イベント: ", font=font)
event_label.grid(row=4, column=0, columnspan=3)

# シミュレーション実行ボタン
simulate_button = tk.Button(window, text="次のターン", command=simulate_stock_with_events, font=font)
simulate_button.grid(row=5, column=0, columnspan=3)

# 初期グラフのセットアップ
fig, ax = plt.subplots(figsize=(6, 4))
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().grid(row=6, column=0, columnspan=3)

# GUI実行
window.mainloop()
