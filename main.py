from fontToPng import fontToResourcePack

def main():
  fontPath = input(r"フォントファイル(.ttf .otf)のパスを入力してください\n例: C:\Users\...\MyFont.ttf")
  resourcePackPath = input(r"生成するリソースパックのディレクトリパスを入力してください\n例: C:\Users\...\AppData\Roaming\.minecraft\resourcepacks\MyFontPack")
  size = None
  while not size:
    try:
      size = int(input('文字のピクセル数を入力してください'))
    except:
      print("整数値のみ使用可能です")
  namespace = input(r"生成するフォントの名前空間を入力してください\nデフォルトのフォントを置き換える場合は何も入力せずにEnter") or "minecraft"
  name = input(r"生成するフォントの名前を入力してください\nデフォルトのフォントを置き換える場合は何も入力せずにEnter") or "default"

  print("変換を開始します")
  fontToResourcePack(fontPath,size,resourcePackPath,namespace,name)
  print("変換が終了しました")
  input("Enterを入力して終了")

main()