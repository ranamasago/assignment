from datetime import datetime
import flet as ft
import requests

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