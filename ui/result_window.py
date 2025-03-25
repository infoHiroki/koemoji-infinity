#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
結果表示ウィンドウモジュール
文字起こし結果を表示するウィンドウを定義
"""

import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import platform
import subprocess

# 標準的なカラーパレット定義
COLORS = {
    "bg_primary": "#F0F0F0",        # 標準的な背景色（薄いグレー）
    "bg_secondary": "#FFFFFF",      # 白背景
    "accent": "#0078D7",            # Windows標準の青
    "accent_hover": "#106EBE",      # ホバー時の青
    "success": "#107C10",           # 成功色（緑）
    "warning": "#D83B01",           # 警告色（オレンジ）
    "error": "#E81123",             # エラー色（赤）
    "text_primary": "#000000",      # 主要テキスト（黒）
    "text_secondary": "#666666",    # 副次テキスト（グレー）
    "text_light": "#FFFFFF",        # 明るいテキスト（白）
    "border": "#CCCCCC",            # 標準ボーダー色
}

class ResultWindow:
    """文字起こし結果表示ウィンドウクラス"""
    
    def __init__(self, parent, transcript, title):
        """
        結果ウィンドウを初期化
        
        Args:
            parent (tk.Tk): 親ウィンドウ
            transcript (str): 文字起こしの結果
            title (str): 結果ウィンドウのタイトル
        """
        # ウィンドウの設定
        self.window = tk.Toplevel(parent)
        self.window.title(f"文字起こし結果 - {title}")
        self.window.geometry("700x500")
        self.window.minsize(500, 400)
        self.window.configure(bg=COLORS["bg_primary"])
        
        # スタイルの設定
        self._setup_styles()
        
        # メインフレームの作成
        main_frame = ttk.Frame(self.window, style="TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ヘッダーフレームの作成
        header_frame = ttk.Frame(main_frame, style="TFrame")
        header_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # タイトルラベル
        title_label = ttk.Label(
            header_frame, 
            text=f"ファイル: {title}", 
            style="Header.TLabel"
        )
        title_label.pack(anchor=tk.W, padx=5, pady=5)
        
        # 説明ラベル
        info_label = ttk.Label(
            header_frame, 
            text="以下に文字起こし結果を表示しています。結果をクリップボードにコピーしたり、ファイルに保存できます。", 
            style="Info.TLabel",
            wraplength=680
        )
        info_label.pack(anchor=tk.W, padx=5, pady=5)
        
        # セパレータ
        separator = ttk.Separator(main_frame, orient=tk.HORIZONTAL, style="TSeparator")
        separator.pack(fill=tk.X, padx=5, pady=8)
        
        # テキストエリアの作成
        text_frame = ttk.Frame(main_frame, style="TFrame")
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 縦スクロールバー
        scrollbar_y = tk.Scrollbar(text_frame)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 横スクロールバー
        scrollbar_x = tk.Scrollbar(text_frame, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # テキストウィジェット
        self.text_widget = tk.Text(
            text_frame,
            wrap=tk.NONE,
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set,
            font=("Yu Gothic UI", 10),
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_primary"],
            padx=8,
            pady=8,
            relief="solid",
            borderwidth=1
        )
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # スクロールバーの設定
        scrollbar_y.config(command=self.text_widget.yview)
        scrollbar_x.config(command=self.text_widget.xview)
        
        # 結果テキストの挿入
        self.text_widget.insert(tk.END, transcript)
        
        # ボタンフレームの作成
        button_frame = ttk.Frame(main_frame, style="TFrame")
        button_frame.pack(fill=tk.X, padx=5, pady=10)
        
        # 閉じるボタン
        close_button = tk.Button(
            button_frame,
            text="閉じる",
            command=self.window.destroy,
            bg=COLORS["bg_primary"],
            fg=COLORS["text_primary"],
            font=("Yu Gothic UI", 10),
            relief="solid",
            borderwidth=1,
            padx=15,
            pady=3,
            activebackground=COLORS["bg_secondary"],
            activeforeground=COLORS["text_primary"]
        )
        close_button.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # コピーボタン
        copy_button = tk.Button(
            button_frame,
            text="クリップボードにコピー",
            command=self._copy_to_clipboard,
            bg=COLORS["accent"],
            fg=COLORS["text_light"],
            font=("Yu Gothic UI", 10),
            relief="flat",
            borderwidth=1,
            padx=15,
            pady=3,
            activebackground=COLORS["accent_hover"],
            activeforeground=COLORS["text_light"]
        )
        copy_button.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # 保存ボタン
        save_button = tk.Button(
            button_frame,
            text="名前を付けて保存",
            command=self._save_as,
            bg=COLORS["accent"],
            fg=COLORS["text_light"],
            font=("Yu Gothic UI", 10),
            relief="flat",
            borderwidth=1,
            padx=15,
            pady=3,
            activebackground=COLORS["accent_hover"],
            activeforeground=COLORS["text_light"]
        )
        save_button.pack(side=tk.RIGHT, padx=5, pady=5)
    
    def _setup_styles(self):
        """スタイルを設定"""
        style = ttk.Style()
        
        # フレームスタイル
        style.configure("TFrame", background=COLORS["bg_primary"])
        
        # ラベルスタイル
        style.configure("TLabel", 
                     background=COLORS["bg_primary"], 
                     foreground=COLORS["text_primary"], 
                     font=("Yu Gothic UI", 10))
        
        # ヘッダーラベルスタイル
        style.configure("Header.TLabel", 
                     background=COLORS["bg_primary"], 
                     foreground=COLORS["text_primary"], 
                     font=("Yu Gothic UI", 12, "bold"))
        
        # 情報ラベルスタイル
        style.configure("Info.TLabel", 
                     background=COLORS["bg_primary"], 
                     foreground=COLORS["text_secondary"], 
                     font=("Yu Gothic UI", 9))
        
        # セパレータスタイル
        style.configure("TSeparator", background=COLORS["border"])
    
    def _copy_to_clipboard(self):
        """テキストをクリップボードにコピー"""
        text = self.text_widget.get(1.0, tk.END)
        self.window.clipboard_clear()
        self.window.clipboard_append(text)
        messagebox.showinfo("コピー完了", "文字起こし結果をクリップボードにコピーしました。")
    
    def _save_as(self):
        """テキストをファイルに保存"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("テキストファイル", "*.txt"),
                ("すべてのファイル", "*.*")
            ],
            title="文字起こし結果を保存"
        )
        
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    text = self.text_widget.get(1.0, tk.END)
                    f.write(text)
                messagebox.showinfo("保存完了", f"文字起こし結果を保存しました: {file_path}")
            except Exception as e:
                messagebox.showerror("エラー", f"保存中にエラーが発生しました: {e}")