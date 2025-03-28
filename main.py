#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
コエモジ∞ - 音声・動画文字起こしアプリケーション
OpenAI Whisperを使用して動画ファイルから音声を抽出し、自動的に文字起こしを行うデスクトップアプリケーション
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import threading
import json
import datetime

# 自作モジュールのインポート
from transcriber import VideoTranscriber
from ui.main_window import MainWindow
from ui.settings_window import SettingsWindow
from utils.config_manager import ConfigManager

# モダンなカラーパレット定義
COLORS = {
    "bg_primary": "#FAFAFA",        # 背景色（ほぼ白）
    "bg_secondary": "#FFFFFF",      # 白背景
    "accent": "#2196F3",            # アクセント色（青）
    "accent_hover": "#1976D2",      # ホバー時のアクセント色（濃い青）
    "success": "#4CAF50",           # 成功色（緑）
    "warning": "#FF9800",           # 警告色（オレンジ）
    "error": "#F44336",             # エラー色（赤）
    "text_primary": "#212121",      # 主要テキスト（黒に近いグレー）
    "text_secondary": "#757575",    # 副次テキスト（ミディアムグレー）
    "text_light": "#FFFFFF",        # 明るいテキスト（白）
    "border": "#E0E0E0",            # 標準ボーダー色（薄いグレー）
}

def main():
    """アプリケーションのメインエントリーポイント"""
    # 設定の読み込み
    config_manager = ConfigManager()
    
    # メインウィンドウの作成
    root = tk.Tk()
    
    # ウィンドウの設定
    root.title("コエモジ∞")
    root.geometry("900x650")
    root.configure(bg=COLORS["bg_primary"])
    
    # ウィンドウを画面中央に配置
    # ウィンドウサイズを取得
    window_width = 900
    window_height = 650
    # 画面サイズを取得
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # 中央の座標を計算
    center_x = int((screen_width - window_width) / 2)
    center_y = int((screen_height - window_height) / 2)
    # ウィンドウの位置を設定
    root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    
    # フォントの設定
    default_font = ("游ゴシック", 10)
    root.option_add("*Font", default_font)
    
    # アプリケーションのアイコン設定（存在する場合）
    try:
        # アイコンの設定
        if os.path.exists("resources/koemoji-infinity-icon.png"):
            icon_img = Image.open("resources/koemoji-infinity-icon.png")
            icon_photo = ImageTk.PhotoImage(icon_img)
            root.iconphoto(True, icon_photo)
        elif os.path.exists("resources/icon.ico"):
            root.iconbitmap("resources/icon.ico")
    except Exception as e:
        print(f"アイコンの読み込みに失敗しました: {e}")
    
    # メインアプリケーションの作成
    app = MainWindow(root, config_manager)
    
    # アプリケーションの実行
    root.mainloop()

if __name__ == "__main__":
    main() 