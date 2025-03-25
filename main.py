#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
動画文字起こしアプリケーション
OpenAI Whisperを使用して動画ファイルから音声を抽出し、自動的に文字起こしを行うデスクトップアプリケーション
"""

import os
import sys
import json
import datetime
import customtkinter as ctk

# 自作モジュールのインポート
from transcriber import VideoTranscriber, AudioTranscriber
from ui.main_window import MainWindow
from utils.config_manager import ConfigManager

# テーマカラー定義
COLORS = {
    "primary": "#FF6B9A",       # メインカラー（ピンク）
    "primary_hover": "#FF5186", # ホバー時の色（濃いピンク）
    "secondary": "#FFB7C9",     # サブカラー（薄いピンク）
    "success": "#4CAF50",       # 成功色（緑）
    "warning": "#FFC107",       # 警告色（黄色）
    "error": "#FF5252",         # エラー色（赤）
    "bg_light": "#FFFFFF",      # 明るい背景色（白）
    "bg_dark": "#F0F0F5",       # 暗い背景色（薄いグレー）
    "text_dark": "#212121",     # 暗いテキスト色
    "text_light": "#FFFFFF",    # 明るいテキスト色
    "text_muted": "#757575",    # グレーアウトしたテキスト色
    "border": "#E0E0E0",        # ボーダー色
}

def main():
    """アプリケーションのメインエントリーポイント"""
    # システム設定
    ctk.set_appearance_mode("light")  # ライトモード
    ctk.set_default_color_theme("blue")  # ベースの色テーマ（後でカスタマイズ）
    
    # 設定の読み込み
    config_manager = ConfigManager()
    
    # メインウィンドウの作成
    root = ctk.CTk()
    
    # ウィンドウの設定
    root.title("音声・動画文字起こしアプリ")
    root.geometry("1000x650")
    
    # アプリケーションのアイコン設定（存在する場合）
    try:
        if os.path.exists("resources/icon.ico"):
            root.iconbitmap("resources/icon.ico")
    except Exception:
        pass
    
    # メインアプリケーションの作成
    app = MainWindow(root, config_manager, COLORS)
    
    # アプリケーションの実行
    root.mainloop()

if __name__ == "__main__":
    main() 