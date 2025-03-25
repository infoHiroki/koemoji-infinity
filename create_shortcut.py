#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
デスクトップにショートカットを作成するスクリプト
"""

import os
import sys
import winshell
from win32com.client import Dispatch

def create_shortcut():
    """デスクトップにショートカットを作成"""
    # 現在のディレクトリ
    current_dir = os.path.abspath(os.path.dirname(__file__))
    # バッチファイルのパス
    bat_path = os.path.join(current_dir, "run_app.bat")
    
    if not os.path.exists(bat_path):
        print(f"エラー: {bat_path} が見つかりません。")
        return False
    
    # デスクトップのパス
    desktop = winshell.desktop()
    
    # ショートカットの作成
    shortcut_path = os.path.join(desktop, "音声文字起こしアプリ.lnk")
    
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = bat_path
    shortcut.WorkingDirectory = current_dir
    shortcut.Description = "音声・動画の文字起こしアプリ"
    shortcut.IconLocation = os.path.join(current_dir, "resources", "icon.ico")
    shortcut.save()
    
    print(f"ショートカットを作成しました: {shortcut_path}")
    return True

if __name__ == "__main__":
    try:
        # pywin32とwinshellがインストールされているか確認
        import win32com
        import winshell
    except ImportError:
        print("必要なライブラリをインストールしています...")
        os.system("pip install pywin32 winshell")
        print("インストール完了。再度スクリプトを実行してください。")
        sys.exit(0)
    
    result = create_shortcut()
    if result:
        print("ショートカットの作成に成功しました。")
    else:
        print("ショートカットの作成に失敗しました。")
    
    input("Enterキーを押すと終了します...") 