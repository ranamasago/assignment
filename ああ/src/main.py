from datetime import datetime
import flet as ft
import requests
import sqlite3
from datetime import datetime



# SQLiteデータベースに接続（なければ新しく作成）
conn = sqlite3.connect('weather_data.db')
cursor = conn.cursor()

# テーブル作成（天気情報用）
cursor.execute('''
CREATE TABLE IF NOT EXISTS weather (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    area_name TEXT,
    forecast_date TEXT,
    temperature_min REAL,
    temperature_max REAL,
    weather_condition TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# テーブル作成（エリア情報用）
cursor.execute('''
CREATE TABLE IF NOT EXISTS area (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    area_code TEXT UNIQUE,
    area_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# 気象庁APIのエンドポイント
base_url = "https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"

# エリアコード一覧（全国すべてのエリアコードを指定）
area_codes = {
    "宗谷": "011000", "上川・留萌": "012000", "網走・北見・紋別": "013000",
    "釧路・根室": "014100", "胆振・日高": "015000", "石狩・空知・後志": "016000",
    "渡島・檜山": "017000", "青森": "020000", "岩手": "030000",
    "宮城": "040000", "秋田": "050000", "山形": "060000",
    "福島": "070000", "茨城": "080000", "栃木": "090000",
    "群馬": "100000", "埼玉": "110000", "千葉": "120000",
    "東京": "130000", "神奈川": "140000", "新潟": "150000",
    "富山": "160000", "石川": "170000", "福井": "180000",
    "山梨": "190000", "長野": "200000", "岐阜": "210000",
    "静岡": "220000", "愛知": "230000", "三重": "240000",
    "滋賀": "250000", "京都": "260000", "大阪": "270000",
    "兵庫": "280000", "奈良": "290000", "和歌山": "300000",
    "鳥取": "310000", "島根": "320000", "岡山": "330000",
    "広島": "340000", "山口": "350000", "徳島": "360000",
    "香川": "370000", "愛媛": "380000", "高知": "390000",
    "福岡": "400000", "佐賀": "410000", "長崎": "420000",
    "熊本": "430000", "大分": "440000", "宮崎": "450000",
    "鹿児島": "460100", "奄美": "460400", "沖縄本島": "471000",
    "大東島": "472000", "宮古島": "473000", "石垣島": "474000", "与那国島": "475000"
}

# データベースにエリア情報を保存
for area_name, area_code in area_codes.items():
    cursor.execute('''
    INSERT OR IGNORE INTO area (area_code, area_name) VALUES (?, ?)
    ''', (area_code, area_name))
conn.commit()

# 各エリアの天気情報を取得
for area_name, area_code in area_codes.items():
    print(f"{area_name} の天気情報を取得中...")
    url = base_url.format(area_code=area_code)
    response = requests.get(url)

    if response.status_code == 200:
        # JSONデータを取得
        data = response.json()

        # データが正しいか確認
        if data and len(data) > 0:
            forecast_date = data[0].get('reportDatetime', '').split("T")[0] if 'reportDatetime' in data[0] else "データなし"

            # timeSeriesの存在確認
            if 'timeSeries' in data[0] and len(data[0]['timeSeries']) > 0:
                forecasts = data[0]['timeSeries'][0].get('areas', [])

                # 予報データが存在する場合のみループ処理
                for forecast in forecasts:
                    temperature_min = forecast.get('temps', ["-"])[0] if forecast.get('temps') else "不明"
                    temperature_max = forecast.get('temps', ["-"])[1] if forecast.get('temps') else "不明"
                    weather_condition = forecast.get('weatherCodes', ["不明"])[0] if forecast.get('weatherCodes') else "不明"

                    # データベースに保存
                    cursor.execute('''
                    INSERT INTO weather (area_name, forecast_date, temperature_min, temperature_max, weather_condition)
                    VALUES (?, ?, ?, ?, ?)
                    ''', (area_name, forecast_date, temperature_min, temperature_max, weather_condition))
                    conn.commit()

                    print(f"日付: {forecast_date}, 最低気温: {temperature_min}, 最高気温: {temperature_max}, 天気: {weather_condition}")
            else:
                print(f"{area_name} の timeSeries データがありません。")
        else:
            print(f"{area_name} のデータが不正です。")
    else:
        print(f"エリア {area_name} のデータ取得に失敗しました。ステータスコード: {response.status_code}")

# データ保存が完了したことを通知
print("天気情報の保存が完了しました！")

# 保存されたデータを確認
cursor.execute('SELECT * FROM weather')
rows = cursor.fetchall()

print("\nデータベース内の天気情報:")
for row in rows:
    print(row)

# データベース接続を閉じる
conn.close()


# 地域リストを取得する関数
def fetch_area_list():
    url = "http://www.jma.go.jp/bosai/common/const/area.json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"HTTP Error (Area List): {response.status_code} - {response.reason}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request Exception (Area List): {e}")
        return None

# 天気予報を取得する関数
def fetch_weather(area_code):
    url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"HTTP Error: {response.status_code} - {response.reason}")
            print(f"Response URL: {response.url}")
            print(f"Response Text: {response.text}")  # デバッグ用
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")
        return None

# ISO形式の日付を日本語表記にフォーマットする関数
def format_date(iso_date):
    try:
        dt = datetime.fromisoformat(iso_date)
        return dt.strftime("%Y年%m月%d日")
    except ValueError:
        return iso_date

# 天気に応じたカスタムアイコン画像を選択する関数
def get_weather_icon(weather_text):
    if "晴" in weather_text:
        return "assets/sunny.png"
    elif "曇" in weather_text:
        return "assets/cloudy.png"
    elif "雨" in weather_text:
        return "assets/rainy.png"
    elif "雪" in weather_text:
        return "assets/snowy.png"
    else:
        return "assets/default.png"

# メインアプリ
def main(page: ft.Page):
    page.title = "天気予報アプリ"
    page.scroll = "adaptive"

    # ローディングインジケーター
    loading_indicator = ft.ProgressRing(visible=False)

    # 地域リストを取得
    area_data = fetch_area_list()
    if not area_data:
        page.add(ft.Text("地域リストの取得に失敗しました。", theme_style="bodyMedium"))
        return

    # 地域リストを選択肢として表示
    area_names = []
    area_code_map = {}
    for area_code, area_info in area_data["offices"].items():
        area_names.append(area_info["name"])
        area_code_map[area_info["name"]] = area_code

    # UIコンポーネント
    title = ft.Text("天気予報", theme_style="headlineMedium", text_align="center")
    dropdown = ft.Dropdown(
        label="地域を選択してください",
        options=[ft.dropdown.Option(name) for name in area_names],
        width=300,
    )
    weather_grid = ft.GridView(expand=True, runs_count=3, spacing=10, padding=10)

    # 地域選択時の処理
    def on_area_selected(e):
        selected_area = dropdown.value
        if selected_area:
            weather_grid.controls.clear()
            weather_grid.update()

            # ローディングインジケーターを表示
            loading_indicator.visible = True
            loading_indicator.update()

            area_code = area_code_map[selected_area]
            weather_data = fetch_weather(area_code)

            # ローディングインジケーターを非表示
            loading_indicator.visible = False
            loading_indicator.update()

            if weather_data:
                try:
                    time_series = weather_data[0]["timeSeries"]
                    for time_entry in time_series:
                        dates = time_entry.get("timeDefines", [])

                        for i, area in enumerate(time_entry["areas"]):
                            weather = (
                                area["weathers"][0]
                                if "weathers" in area and len(area["weathers"]) > 0
                                else "天気情報が利用できません"
                            )
                            temp_min = (
                                area.get("tempsMin", [None])[0]
                                if len(area.get("tempsMin", [])) > 0
                                else None
                            )
                            temp_max = (
                                area.get("tempsMax", [None])[0]
                                if len(area.get("tempsMax", [])) > 0
                                else None
                            )

                            temp_text = (
                                f"{temp_min}°C / {temp_max}°C"
                                if temp_min is not None and temp_max is not None
                                else "気温情報なし"
                            )

                            if i < len(dates):
                                formatted_date = format_date(dates[i])
                                weather_icon = get_weather_icon(weather)

                                weather_grid.controls.append(
                                    ft.Card(
                                        content=ft.Container(
                                            content=ft.Column(
                                                [
                                                    ft.Text(
                                                        formatted_date,
                                                        theme_style="titleMedium",
                                                        text_align="center",
                                                    ),
                                                    ft.Image(
                                                        src=weather_icon,
                                                        width=40,
                                                        height=40,
                                                    ),
                                                    ft.Text(
                                                        weather,
                                                        theme_style="bodyMedium",
                                                        text_align="center",
                                                    ),
                                                    ft.Text(
                                                        temp_text,
                                                        theme_style="bodySmall",
                                                        text_align="center",
                                                    ),
                                                ],
                                                alignment="center",
                                                spacing=5,
                                            ),
                                            padding=10,
                                        ),
                                    )
                                )
                except KeyError as ke:
                    weather_grid.controls.append(
                        ft.Text(f"データ構造のエラー: {ke}", theme_style="bodyMedium")
                    )
            else:
                weather_grid.controls.append(
                    ft.Container(
                        content=ft.Text(
                            "天気情報の取得に失敗しました。\nインターネット接続を確認してください。",
                            theme_style="bodyLarge",
                            text_align="center",
                        ),
                        padding=20,
                        bgcolor="red",
                        border_radius=10,
                    )
                )
            weather_grid.update()

    dropdown.on_change = on_area_selected

    container = ft.Column(
        controls=[
            title,
            dropdown,
            loading_indicator,
            weather_grid,
        ]
    )
    page.add(container)

ft.app(target=main)






