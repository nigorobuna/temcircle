created by Taichi Yamashita 2024.09.21
pythonでTEM画像を読み込み、析出物の直径をピクセル単位でCSVに保存するアプリです。fletというフレームワークを使用しています。
pngファイルでしか動作確認をしていないのでtiffファイルに関してはおいおいやっていきます。

<用意するもの>
・TEMで撮影した画像
・pythonをインストールしているパソコン
・VSCodeなどのテキストエディタ

<使い方>
・テキストエディタでmaruapp4.pyを開き、プログラムを実行します
・出力ファイルの名前を決めます。拡張子付け忘れないように！
・パソコンから画像を選択、をクリックします
・画像を読み込ませるとしかるべきプログラムが走り、CSVと画像が生成されます
・画像を見ながら除外する番号を決定します
・ピクセル単位からnm単位に変換します(手作業）
・あとはExcelかなんかで体積を計算してください

<注意>
・連続で処理を行う場合、画像の更新システムを作成していないため都度プログラムを終了（バツボタンを押す）してください。
・画像は任意の拡張子で出力できますが、入力画面で拡張子(.csvなど)を忘れると狂うので注意してください。
・結果画面ではスクロールききませんごめんなさい　CSVで詳細は確認してください