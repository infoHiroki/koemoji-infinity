#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
アプリケーションのアイコンを生成するスクリプト
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """シンプルなアイコンを作成"""
    # アイコンのサイズ
    icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    
    # リソースディレクトリを確保
    os.makedirs("resources", exist_ok=True)
    
    # 各サイズのアイコンを作成
    for size in icon_sizes:
        width, height = size
        img = Image.new('RGBA', size, color=(255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        # 背景の円を描画
        circle_size = min(width, height) - 2
        circle_pos = ((width - circle_size) // 2, (height - circle_size) // 2)
        draw.ellipse(
            [circle_pos[0], circle_pos[1], circle_pos[0] + circle_size, circle_pos[1] + circle_size], 
            fill=(33, 150, 243, 255)  # アクセントカラー（青）
        )
        
        # 音声波形を描画
        wave_color = (255, 255, 255, 230)  # 白色
        center_x = width // 2
        center_y = height // 2
        wave_width = circle_size * 0.6
        
        # 中央の波形
        wave_height = circle_size * 0.3
        draw.rectangle(
            [center_x - 2, center_y - wave_height // 2, center_x + 2, center_y + wave_height // 2],
            fill=wave_color
        )
        
        # 左側の波形
        left_x = center_x - wave_width // 3
        left_height = circle_size * 0.2
        draw.rectangle(
            [left_x - 2, center_y - left_height // 2, left_x + 2, center_y + left_height // 2],
            fill=wave_color
        )
        
        # 右側の波形
        right_x = center_x + wave_width // 3
        right_height = circle_size * 0.2
        draw.rectangle(
            [right_x - 2, center_y - right_height // 2, right_x + 2, center_y + right_height // 2],
            fill=wave_color
        )
        
        # 保存
        filename = f"resources/icon_{width}x{height}.png"
        img.save(filename)
        print(f"Created {filename}")
    
    # Windows用のicoファイルを生成
    images = []
    for size in icon_sizes:
        filename = f"resources/icon_{size[0]}x{size[1]}.png"
        img = Image.open(filename)
        images.append(img)
    
    # アイコンファイルを保存
    icon_path = "resources/icon.ico"
    images[0].save(icon_path, format='ICO', sizes=[(img.width, img.height) for img in images])
    print(f"Created {icon_path}")
    
    return icon_path

if __name__ == "__main__":
    icon_path = create_icon()
    print(f"アイコンが正常に生成されました: {icon_path}") 