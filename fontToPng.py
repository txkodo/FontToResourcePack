from configparser import InterpolationMissingOptionError
from math import ceil
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from cairosvg import svg2png
from PIL import Image
import io
from tqdm import tqdm
from itertools import count
import json
from pathlib import Path

def fontToGlyphs(fontpath:str|Path,fontheight:int):
  font = TTFont(fontpath)
  glyphMap = font.getGlyphSet()
  cmap = font.getBestCmap()
  ascender = font['OS/2'].sTypoAscender
  descender = font['OS/2'].sTypoDescender
  height = ascender - descender

  imgMap:dict[int,Image.Image] = {}

  maxWidth = fontheight
  for charInt in tqdm(cmap):
    charInt:int
    if charInt >= 0xffff:
      continue
    try:
      char = chr(charInt)
      glyph = glyphMap[cmap[charInt]]
      svg_path_pen = SVGPathPen(glyphMap)
      glyph.draw(svg_path_pen)
      
      width = glyph.width

      svg = f'''\
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 {-ascender} {width} {height}">
          <g transform="scale(1, -1)">
              <rect x="0" y="{descender}" width="{width}" height="{height}"
                  stroke="cyan" fill="none"/>
              <circle cx="0" cy="0" r="5" fill="blue"/>
              <path d="{svg_path_pen.getCommands()}"/>
          </g>
      </svg>
      '''
      fontwidth = ceil(fontheight * width / height)
      # if maxWidth < fontwidth:
      #   print(char,charInt,fontwidth)
      # maxWidth = max(maxWidth,fontwidth)
      png = svg2png(bytestring = svg, output_height = fontheight, output_width = fontwidth,negate_colors=True)
      img = Image.open(io.BytesIO(png))
      imgMap[charInt] = img
    except ValueError:
      continue

  return (maxWidth,imgMap)

def fontToMcFont(fontpath:str|Path,fontheight:int):
  maxWidth,imgMap = fontToGlyphs(fontpath,fontheight)
  chars:list[str] = []
  n = 16

  keys = list(imgMap.keys())
  values = list(imgMap.values())
  image = Image.new('RGBA',(maxWidth * n,fontheight * ceil( len(keys) / 16)),"#00000000")
  for i,row in zip(range(0, len(keys), n),count()):
    line = ""
    for j in range(16):
      if i + j < len(keys):
        line += f"\\u{(keys[i + j]):04x}"
        image.paste(values[i + j], ( maxWidth * j, fontheight * row ))
      else:
        line += "\\u0000"
    chars.append(line)

  return (chars,image)


def fontToResourcePack(fontpath:str|Path,fontheight:int,resourcePackPath:str|Path,namespace:str = "minecraft",fontname:str = "default"):
  chars,image = fontToMcFont(fontpath,fontheight)

  resourcePackPath = Path(resourcePackPath)
  resourcePackPath.mkdir(parents=True,exist_ok=True)
  mcmeta = {
  "pack": {
      "pack_format": 8,
      "description": " Font Pack made with FontGen by @txkodo"
    }
  }
  (resourcePackPath/"pack.mcmeta").write_text(json.dumps(mcmeta))
  
  namespacePath = resourcePackPath / f"assets/{namespace}"

  jsonData = {
    "providers": [
      {
      "type": "bitmap",
      "file": f"{namespace}:font/{fontname}.png",
      "height": 9,
      "ascent": 8,
      "chars": chars
      }
    ]
  }
  (namespacePath/"font").mkdir(parents=True,exist_ok=True)
  (namespacePath/f"font/{fontname}.json").write_text(json.dumps(jsonData).replace("\\\\","\\"))

  (namespacePath/"textures/font").mkdir(parents=True,exist_ok=True)
  image.save(namespacePath/f"textures/font/{fontname}.png",bitmap_format='png')
