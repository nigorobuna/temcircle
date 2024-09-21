import flet as ft
from PIL import Image
import numpy as np
import cv2
import csv
from flet import FilePickerResultEvent

# アプリの状態を管理するクラス
class AppState:
    def __init__(self):
        self.csv_filename = "circle_diameters.csv"  # デフォルトのCSVファイル名
        self.image_filename = "numbered_image.png"  # デフォルトの画像ファイル名

# アプリケーションの状態を保持するインスタンスを作成
app_state = AppState()

# メインアプリケーション関数
def main(page: ft.Page):
    # ウィンドウのタイトルとサイズを設定
    page.title = "(c) 2024 Taichi Yamashita"
    page.window_width = 1000
    page.window_height = 800

    # ウェルカムテキストの作成
    welcome_text = ft.Text(value="直径はかるクンです！", size=30, color=ft.colors.BLUE)
    # 画像表示用のウィジェット
    img_display = ft.Image(src="", width=500, height=500)
    # ログ表示用テキスト
    log = ft.Text(value="")
    # 検出結果を表示するためのカラム
    result_text = ft.Column()

    # 画像ファイル選択の結果処理
    def pick_image_result(e: FilePickerResultEvent):
        if e.files:
            log.value = f"Selected image: {e.files[0].name}"  # 選択された画像の名前を表示
            img_display.src = e.files[0].path  # 画像を表示
            page.update()  # ページを更新
            process_image(e.files[0].path)  # 画像処理を実行

    # ファイルピッカーの設定
    file_picker = ft.FilePicker(on_result=pick_image_result)
    page.overlay.append(file_picker)  # ページにファイルピッカーを追加

    # 画像処理関数
    def process_image(image_path):
        # 画像を開く
        image = Image.open(image_path)
        gray_image = np.array(image.convert("L"))  # グレースケールに変換
        gaus_image = cv2.GaussianBlur(gray_image, (5, 5), 0)  # ノイズを除去するためにガウシアンフィルタを適用
        _, image_nichi = cv2.threshold(gaus_image, 80, 255, cv2.THRESH_BINARY)  # 二値化処理
        contours, _ = cv2.findContours(image_nichi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # 輪郭を抽出
        log.value = f"Detected circles: {len(contours)}"  # 検出された円の数を表示

        output_image = np.array(image.convert("RGB"))  # 出力画像用のRGB配列を作成
        font = cv2.FONT_HERSHEY_SIMPLEX  # フォントの設定
        circle_diameters = []  # 円の直径を格納するリスト
        result_text.controls.clear()  # 検出結果をクリア

        # 各円に対して直径を計算し、表示
        for i, contour in enumerate(contours):
            x, y, w, h = cv2.boundingRect(contour)  # 輪郭の外接矩形を取得
            diameter = (w + h) / 2  # 直径を計算
            circle_diameters.append((i + 1, diameter))  # 円の番号と直径をリストに追加
            result_text.controls.append(ft.Text(f"Circle {i + 1}: Diameter = {diameter:.2f} pixels"))  # 結果を表示
            cv2.putText(output_image, f"{i + 1}", (x + w // 2, y + h // 2), font, 1, (255, 0, 0), 2)  # 画像に番号を描画

        # CSVファイルと画像ファイルの保存
        csv_filename = app_state.csv_filename
        image_filename = app_state.image_filename

        # CSVファイルに直径データを保存
        with open(csv_filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["number", "diameter(pixels)"])  # ヘッダー行を追加
            writer.writerows(circle_diameters)  # データを書き込む

        Image.fromarray(output_image).save(image_filename)  # 出力画像を保存
        img_display.src = image_filename  # 保存した画像を表示
        page.update()  # ページを更新

    # コメントページに遷移する関数
    def open_comment_page(e):
        page.go("/comments")  # コメントページに遷移

    # データをクリアして最初の画面に戻る関数
    def clear_data_and_reset(e):  # 引数にeを追加
        img_display.src = ""  # 画像をクリア
        log.value = ""  # ログをクリア
        result_text.controls.clear()  # 検出結果をクリア
        page.update()  # ページを更新

    # UIの構築
    page.add(
        ft.Row([
            ft.Column([
                ft.ElevatedButton(
                    content=ft.Text("最初の画面に戻る", size=20),
                    on_click=clear_data_and_reset  # データをクリアして最初の画面に戻るボタン
                ),
            ], alignment=ft.MainAxisAlignment.START),  # 左上に配置
            img_display,  # 画像表示部分
            ft.Column([
                welcome_text,  # ウェルカムテキスト
                log,  # ログ
                result_text  # 検出結果
            ], scroll="ALWAYS"),
        ]),
        ft.Row([
            ft.ElevatedButton(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(value="画像をパソコンから選択", size=30),
                            ft.Text(value="png,jpeg,tiffとかいけます"),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=5,
                    ),
                    padding=ft.padding.all(20),
                ),
                on_click=lambda _: file_picker.pick_files()  # ボタンをクリックしたときにファイルピッカーを開く
            )
        ]),
        ft.Row([
            ft.TextField(
                label="保存するCSVファイル名を入力",
                hint_text="例: circle_diameters.csv",
                width=300,
                on_change=lambda e: setattr(app_state, "csv_filename", e.control.value)  # CSVファイル名を更新
            ),
            ft.TextField(
                label="保存する画像ファイル名を入力",
                hint_text="例: numbered_image.png",
                width=300,
                on_change=lambda e: setattr(app_state, "image_filename", e.control.value)  # 画像ファイル名を更新
            )
        ]),
        ft.Row([
            ft.ElevatedButton(
                content=ft.Text("メモを追加", size=20),
                on_click=open_comment_page  # コメントページへのボタン
            )
        ])
    )

    # ページの切り替えを管理する関数
    def route_change(e):
        if e.route == "/comments":
            comment_page(page)  # コメントページを表示
        else:
            main(page)  # メインページを表示

    # ページ遷移の設定
    page.on_route_change = route_change

# コメントページの関数
def comment_page(page: ft.Page):
    page.title = "コメントページ"  # コメントページのタイトル

    # コメント入力用のテキストフィールド
    comment_input = ft.TextField(label="コメントを入力", multiline=True, width=400, height=200)
    comment_list = ft.Column()  # コメント表示用のカラム

    # コメント送信処理
    def submit_comment(e):
        if comment_input.value:  # コメントが空でない場合
            comment_list.controls.append(ft.Text(comment_input.value))  # コメントをリストに追加
            comment_input.value = ""  # 入力フィールドをクリア
            page.update()  # ページを更新

    # コメント入力フィールドと送信ボタンを追加
    page.add(
        ft.Row([
            comment_input,
            ft.ElevatedButton("送信", on_click=submit_comment)  # コメント送信ボタン
        ]),
        comment_list  # コメントリストを表示
    )

# アプリを実行
ft.app(target=main)
