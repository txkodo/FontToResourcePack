# FontToResourcePack
.otf .ttf のフォントをMinecraftのリソースパックに変換する


# 必要環境
* Python 3.10.0 (作者が使用しているバージョン。他のバージョンでも使えると思われる)

  * CairoSVG 2.5.2

  * fontTools 4.29.1

  * Pillow 9.0.1

  * tqdm 4.62.3

pipを使用している場合は1コマンドでライブラリの導入ができる
```bash
pip install -r requirements.txt
```

# 使用方法
本リポジトリをgit cloneもしくはzipでダウンロードし展開する

上記ライブラリうを導入する

main.py を起動する

対話形式でフォントのパス、完成品のパス、ピクセル数、名前空間、フォント名を聞かれるので入力する

変換完了!

# ライセンス
本リポジトリにはMITライセンスが適用されます

ただし変換したフォントにはフォント自体のライセンスが適用されますので、公開、配布等する際には十分ご注意ください

# Contact
不明点がある、バグを見つけた、3.10.0以外のPythonで動いた等の場合はぜひtwitterのDMにお願いします。
[Twitter @txkodo](https://mobile.twitter.com/txkodo)
