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