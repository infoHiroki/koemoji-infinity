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
    default_font = ("游ゴシック", 12)
    root.option_add("*Font", default_font)
    
    # アプリケーションのアイコン設定（存在する場合）
    try:
        # ロゴ画像をアイコンとして使用（ファビコンをロゴに統一）
        logo_path = "resources/koemoji-infinity-logo-48x48 px.png"
        if os.path.exists(logo_path):
            try:
                icon_img = Image.open(logo_path)
                icon_photo = ImageTk.PhotoImage(icon_img)
                root.iconphoto(True, icon_photo)
                # Windowsタイトルバー用のアイコンも設定
                import ctypes
                app_id = 'com.koemoji.infinity'  # アプリケーション識別子
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
                # サブウィンドウでアイコンを再利用するためにプロパティとして保存
                root.iconphoto_master = icon_photo
                print(f"アイコンが正常に設定されました: {logo_path}")
            except Exception as e:
                print(f"ロゴ画像の読み込みに失敗しました（詳細）: {e}")
                # ファイル名にスペースがある場合の代替処理
                try:
                    # 代替ロゴを使用
                    alt_logo_path = "resources/koemoji-infinity-logo.png"
                    if os.path.exists(alt_logo_path):
                        icon_img = Image.open(alt_logo_path)
                        # 適切なサイズにリサイズ
                        icon_img = icon_img.resize((48, 48), Image.LANCZOS)
                        icon_photo = ImageTk.PhotoImage(icon_img)
                        root.iconphoto(True, icon_photo)
                        # Windowsタイトルバー用のアイコンも設定
                        import ctypes
                        app_id = 'com.koemoji.infinity'  # アプリケーション識別子
                        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
                        root.iconphoto_master = icon_photo
                        print(f"代替アイコンを設定しました: {alt_logo_path}")
                except Exception as e2:
                    print(f"代替ロゴの読み込みにも失敗しました: {e2}")
        elif os.path.exists("resources/koemoji-infinity-logo.png"):
            icon_img = Image.open("resources/koemoji-infinity-logo.png")
            # 適切なサイズにリサイズ
            icon_img = icon_img.resize((48, 48), Image.LANCZOS)
            icon_photo = ImageTk.PhotoImage(icon_img)
            root.iconphoto(True, icon_photo)
            # サブウィンドウでアイコンを再利用するためにプロパティとして保存
            root.iconphoto_master = icon_photo
            print("通常ロゴ画像をアイコンとして使用します")
        elif os.path.exists("resources/koemoji-infinity-logo-touka.png"):
            icon_img = Image.open("resources/koemoji-infinity-logo-touka.png")
            # 適切なサイズにリサイズ
            icon_img = icon_img.resize((48, 48), Image.LANCZOS)
            icon_photo = ImageTk.PhotoImage(icon_img)
            root.iconphoto(True, icon_photo)
            # サブウィンドウでアイコンを再利用するためにプロパティとして保存
            root.iconphoto_master = icon_photo
            print("透過ロゴ画像をアイコンとして使用します")
        elif os.path.exists("resources/icon.ico"):
            root.iconbitmap("resources/icon.ico")
            print("アイコンファイルを使用します")
        else:
            print("アイコンファイルが見つかりませんでした")
    except Exception as e:
        print(f"アイコンの読み込みに失敗しました: {e}")
    
    # メインアプリケーションの作成
    app = MainWindow(root, config_manager)
    
    # アプリケーションの実行
    root.mainloop()

if __name__ == "__main__":
    main() 