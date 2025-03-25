#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
動画文字起こしアプリケーション
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
    "bg_primary": "#F5F7FA",        # 背景色（明るいグレー）
    "bg_secondary": "#FFFFFF",      # セカンダリ背景（白）
    "accent_primary": "#4361EE",    # メインアクセント（青）
    "accent_secondary": "#3F37C9",  # セカンダリアクセント（濃い青）
    "accent_light": "#4895EF",      # 明るいアクセント（薄い青）
    "text_primary": "#2B2D42",      # 主要テキスト（濃紺）
    "text_secondary": "#6C757D",    # 副次テキスト（グレー）
    "text_light": "#FFFFFF",        # 明るいテキスト（白）
    "border": "#DEE2E6",            # ボーダー色（薄灰）
}

def main():
    """アプリケーションのメインエントリーポイント"""
    # 設定の読み込み
    config_manager = ConfigManager()
    
    # メインウィンドウの作成
    root = tk.Tk()
    
    # ウィンドウの設定
    root.title("音声・動画文字起こしアプリ")
    root.geometry("900x650")
    root.configure(bg=COLORS["bg_primary"])
    
    # フォントの設定
    default_font = ("Segoe UI", 10)
    root.option_add("*Font", default_font)
    
    # アプリケーションのアイコン設定（存在する場合）
    try:
        if os.path.exists("resources/icon.ico"):
            root.iconbitmap("resources/icon.ico")
    except Exception:
        pass
    
    # メインアプリケーションの作成
    app = MainWindow(root, config_manager)
    
    # アプリケーションの実行
    root.mainloop()

if __name__ == "__main__":
    main() 