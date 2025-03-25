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
        self.window.geometry("700x550")
        self.window.minsize(500, 400)
        self.window.configure(bg=COLORS["bg_primary"])
        
        # ウィンドウを画面中央に配置
        self._center_window(parent)
        
        # スタイルの設定
        self._setup_styles()
        
        # メインレイアウト作成
        self._create_main_layout(transcript, title)
    
    def _setup_styles(self):
        """スタイルを設定"""
        style = ttk.Style()
        
        # 標準フォント定義
        heading_font = ("Segoe UI", 11, "bold")
        normal_font = ("Segoe UI", 10)
        small_font = ("Segoe UI", 9)
        
        # フレームスタイル
        style.configure("TFrame", background=COLORS["bg_primary"])
        style.configure("Card.TFrame", background=COLORS["bg_secondary"])
        
        # ラベルスタイル
        style.configure("TLabel", background=COLORS["bg_primary"], foreground=COLORS["text_primary"], font=normal_font)
        style.configure("Header.TLabel", background=COLORS["bg_primary"], foreground=COLORS["text_primary"], font=heading_font)
        style.configure("Card.TLabel", background=COLORS["bg_secondary"], foreground=COLORS["text_primary"], font=normal_font)
        style.configure("CardHeader.TLabel", background=COLORS["bg_secondary"], foreground=COLORS["text_primary"], font=heading_font)
        style.configure("Info.TLabel", background=COLORS["bg_primary"], foreground=COLORS["text_secondary"], font=small_font)
        
        # セパレータスタイル
        style.configure("TSeparator", background=COLORS["border"])
    
    def _create_main_layout(self, transcript, title):
        """メインレイアウトを作成"""
        # メインコンテナ
        main_frame = ttk.Frame(self.window, style="TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # ヘッダーエリア
        self._create_header_area(main_frame, title)
        
        # 結果テキストカード
        self._create_text_card(main_frame, transcript)
        
        # ボタンエリア
        self._create_button_area(main_frame)
    
    def _create_header_area(self, parent, title):
        """ヘッダーエリアを作成"""
        header_frame = ttk.Frame(parent, style="TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        # タイトル
        title_label = ttk.Label(
            header_frame, 
            text="文字起こし結果", 
            style="Header.TLabel"
        )
        title_label.pack(anchor=tk.W)
        
        # ファイル名
        file_label = ttk.Label(
            header_frame, 
            text=f"ファイル: {title}", 
            style="TLabel"
        )
        file_label.pack(anchor=tk.W, pady=(5, 0))
        
        # 説明
        info_label = ttk.Label(
            header_frame, 
            text="以下に文字起こし結果を表示しています。テキストをコピーしたり、ファイルに保存できます。", 
            style="Info.TLabel",
            wraplength=680
        )
        info_label.pack(anchor=tk.W, pady=(5, 0))
    
    def _create_text_card(self, parent, transcript):
        """テキスト表示カードを作成"""
        # カード外側フレーム
        card_outer = ttk.Frame(parent, style="TFrame")
        card_outer.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # カード内側フレーム
        card = ttk.Frame(card_outer, style="Card.TFrame")
        card.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        card.configure(relief="solid", borderwidth=1)
        
        # テキスト領域
        text_area = ttk.Frame(card, style="Card.TFrame")
        text_area.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # スクロールバー（縦）
        scrollbar_y = ttk.Scrollbar(text_area, orient=tk.VERTICAL)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        # スクロールバー（横）
        scrollbar_x = ttk.Scrollbar(text_area, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # テキストウィジェット
        self.text_widget = tk.Text(
            text_area,
            wrap=tk.NONE,
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set,
            font=("Segoe UI", 10),
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_primary"],
            padx=10,
            pady=10,
            relief="flat",
            borderwidth=0
        )
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # スクロールバーの設定
        scrollbar_y.config(command=self.text_widget.yview)
        scrollbar_x.config(command=self.text_widget.xview)
        
        # 結果テキストの挿入
        self.text_widget.insert(tk.END, transcript)
    
    def _create_button_area(self, parent):
        """ボタンエリアを作成"""
        button_frame = ttk.Frame(parent, style="TFrame")
        button_frame.pack(fill=tk.X, pady=(15, 0))
        
        # 閉じるボタン
        close_button = tk.Button(
            button_frame,
            text="閉じる",
            command=self.window.destroy,
            bg=COLORS["bg_primary"],
            fg=COLORS["text_primary"],
            font=("Segoe UI", 10),
            relief="solid",
            borderwidth=1,
            padx=15,
            pady=6,
            activebackground=COLORS["border"],
            activeforeground=COLORS["text_primary"]
        )
        close_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # コピーボタン
        copy_button = tk.Button(
            button_frame,
            text="コピー",
            command=self._copy_to_clipboard,
            bg=COLORS["accent"],
            fg=COLORS["text_light"],
            font=("Segoe UI", 10),
            relief="flat",
            borderwidth=0,
            padx=15,
            pady=6,
            activebackground=COLORS["accent_hover"],
            activeforeground=COLORS["text_light"]
        )
        copy_button.pack(side=tk.RIGHT, padx=5)
        
        # 保存ボタン
        save_button = tk.Button(
            button_frame,
            text="保存",
            command=self._save_as,
            bg=COLORS["accent"],
            fg=COLORS["text_light"],
            font=("Segoe UI", 10),
            relief="flat",
            borderwidth=0,
            padx=15,
            pady=6,
            activebackground=COLORS["accent_hover"],
            activeforeground=COLORS["text_light"]
        )
        save_button.pack(side=tk.RIGHT, padx=5)
    
    def _copy_to_clipboard(self):
        """テキストをクリップボードにコピー"""
        text = self.text_widget.get("1.0", tk.END)
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
                text = self.text_widget.get("1.0", tk.END)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(text)
                messagebox.showinfo("保存完了", f"文字起こし結果を以下に保存しました:\n{file_path}")
                
                # ファイルを開くかどうか尋ねる
                if messagebox.askyesno("確認", "保存したファイルを開きますか？"):
                    self._open_file(file_path)
            except Exception as e:
                messagebox.showerror("エラー", f"ファイルの保存中にエラーが発生しました:\n{str(e)}")
    
    def _center_window(self, parent):
        """ウィンドウを画面中央に配置"""
        # ウィンドウのサイズを取得
        window_width = 700
        window_height = 550
        
        # 親ウィンドウの位置とサイズを取得
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        
        # 親ウィンドウの中央に配置
        center_x = parent_x + int((parent_width - window_width) / 2)
        center_y = parent_y + int((parent_height - window_height) / 2)
        
        # 画面の範囲内に収める
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        
        # X座標が画面外にならないよう調整
        if center_x + window_width > screen_width:
            center_x = screen_width - window_width
        if center_x < 0:
            center_x = 0
            
        # Y座標が画面外にならないよう調整
        if center_y + window_height > screen_height:
            center_y = screen_height - window_height
        if center_y < 0:
            center_y = 0
        
        # ウィンドウの位置を設定
        self.window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    
    def _open_file(self, file_path):
        """保存したファイルを開く"""
        try:
            if platform.system() == "Windows":
                os.startfile(file_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.call(["open", file_path])
            else:  # Linux
                subprocess.call(["xdg-open", file_path])
        except Exception as e:
            messagebox.showerror("エラー", f"ファイルを開けませんでした:\n{str(e)}")