#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
結果表示ウィンドウモジュール
文字起こし結果を表示するウィンドウを定義
"""

import os
import tkinter as tk
from tkinter import ttk, messagebox
import platform
import subprocess

# モダンなカラーパレット定義
COLORS = {
    "bg_primary": "#F5F7FA",        # 背景色（明るいグレー）
    "bg_secondary": "#FFFFFF",      # セカンダリ背景（白）
    "accent_primary": "#4361EE",    # メインアクセント（青）
    "accent_secondary": "#3F37C9",  # セカンダリアクセント（濃い青）
    "accent_light": "#4895EF",      # 明るいアクセント（薄い青）
    "success": "#4CC9B0",           # 成功色（緑）
    "warning": "#F72585",           # 警告色（ピンク）
    "error": "#E63946",             # エラー色（赤）
    "text_primary": "#2B2D42",      # 主要テキスト（濃紺）
    "text_secondary": "#6C757D",    # 副次テキスト（グレー）
    "text_light": "#FFFFFF",        # 明るいテキスト（白）
    "border": "#DEE2E6",            # ボーダー色（薄灰）
    "hover": "#3A0CA3",             # ホバー色（紫）
    "timestamp": "#4361EE",         # タイムスタンプ色（青）
}

class ResultWindow:
    """文字起こし結果表示ウィンドウクラス"""
    
    def __init__(self, parent, results):
        """
        初期化
        
        Args:
            parent (tk.Tk): 親ウィンドウ
            results (list): 文字起こし結果のリスト
        """
        self.parent = parent
        self.results = results
        
        # ウィンドウの作成
        self.window = tk.Toplevel(parent)
        self.window.title("文字起こし結果")
        self.window.geometry("800x600")
        self.window.transient(parent)
        self.window.configure(bg=COLORS["bg_primary"])
        
        # スタイルの設定
        self._setup_styles()
        
        # 結果表示領域の作成
        self._create_result_view()
    
    def _setup_styles(self):
        """スタイルの設定"""
        style = ttk.Style()
        
        # フォント定義
        heading_font = ("Segoe UI", 12, "bold")
        title_font = ("Segoe UI", 16, "bold")
        normal_font = ("Segoe UI", 10)
        small_font = ("Segoe UI", 9)
        button_font = ("Segoe UI", 10, "bold")
        
        # フレームのスタイル
        style.configure("Modern.TFrame", background=COLORS["bg_primary"])
        
        # ノートブックのスタイル
        style.configure("Modern.TNotebook", background=COLORS["bg_primary"], borderwidth=0)
        style.configure("Modern.TNotebook.Tab", 
                       background=COLORS["bg_secondary"], 
                       foreground=COLORS["text_secondary"],
                       padding=[12, 6], 
                       font=normal_font,
                       borderwidth=0)
        style.map("Modern.TNotebook.Tab",
                 background=[("selected", COLORS["accent_primary"]), ("active", COLORS["accent_light"])],
                 foreground=[("selected", COLORS["text_light"]), ("active", COLORS["text_primary"])])
        
        # ラベルのスタイル
        style.configure("Modern.TLabel", 
                       background=COLORS["bg_primary"], 
                       foreground=COLORS["text_primary"], 
                       font=normal_font)
        
        # 見出しラベルのスタイル
        style.configure("Title.TLabel", 
                       background=COLORS["bg_primary"], 
                       foreground=COLORS["accent_secondary"], 
                       font=title_font)
        
        # 情報ラベルのスタイル
        style.configure("Info.TLabel", 
                       background=COLORS["bg_primary"], 
                       foreground=COLORS["text_secondary"], 
                       font=small_font)
        
        # ボタンのスタイル
        style.configure("Modern.TButton", 
                       background=COLORS["accent_primary"],
                       foreground=COLORS["text_light"],
                       font=button_font,
                       padding=(10, 5))
        style.map("Modern.TButton",
                 background=[("active", COLORS["accent_secondary"]), 
                            ("pressed", COLORS["accent_primary"]),
                            ("disabled", "#A0A0A0"),
                            ("readonly", COLORS["accent_primary"]),
                            ("!disabled", COLORS["accent_primary"])],
                 foreground=[("active", COLORS["text_light"]), 
                            ("pressed", COLORS["text_light"]),
                            ("disabled", "#D0D0D0"),
                            ("readonly", COLORS["text_light"]),
                            ("!disabled", COLORS["text_light"])])
        
        # アクションボタンのスタイル
        style.configure("Action.TButton", 
                       background=COLORS["success"],
                       foreground=COLORS["text_light"],
                       font=button_font,
                       padding=(12, 6))
        style.map("Action.TButton",
                 background=[("active", "#3DB39E"), 
                            ("pressed", COLORS["success"]),
                            ("disabled", "#A0A0A0"),
                            ("readonly", COLORS["success"]),
                            ("!disabled", COLORS["success"])],
                 foreground=[("active", COLORS["text_light"]), 
                            ("pressed", COLORS["text_light"]),
                            ("disabled", "#D0D0D0"),
                            ("readonly", COLORS["text_light"]),
                            ("!disabled", COLORS["text_light"])])
    
    def _create_result_view(self):
        """結果表示領域の作成"""
        # メインフレームの作成
        main_frame = ttk.Frame(self.window, style="Modern.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # タイトルラベル
        title_label = ttk.Label(main_frame, text="文字起こし結果", style="Title.TLabel")
        title_label.pack(pady=(0, 15))
        
        # タブノートブックの作成
        self.notebook = ttk.Notebook(main_frame, style="Modern.TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 各結果を処理
        for result in self.results:
            file_name = result.get("file_name", "不明なファイル")
            output_path = result.get("output_path", "")
            text = result.get("text", "")
            segments = result.get("segments", [])
            
            # タブの作成
            tab_frame = ttk.Frame(self.notebook, style="Modern.TFrame", padding=12)
            self.notebook.add(tab_frame, text=file_name)
            
            # テキスト表示エリアの作成
            text_frame = ttk.Frame(tab_frame, style="Modern.TFrame")
            text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # テキスト表示ウィジェット
            text_widget = tk.Text(
                text_frame, 
                wrap=tk.WORD, 
                padx=15, 
                pady=15,
                bg=COLORS["bg_secondary"],
                fg=COLORS["text_primary"],
                insertbackground=COLORS["accent_primary"],
                font=("Segoe UI", 10),
                relief="flat",
                borderwidth=0,
                highlightthickness=1,
                highlightcolor=COLORS["border"],
                selectbackground=COLORS["accent_primary"],
                selectforeground=COLORS["text_light"]
            )
            text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            # スクロールバーの作成
            scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            text_widget.config(yscrollcommand=scrollbar.set)
            
            # テキストの挿入
            text_widget.insert(tk.END, text)
            text_widget.config(state=tk.DISABLED)  # 読み取り専用に設定
            
            # 情報と操作ボタンのフレーム
            info_frame = ttk.Frame(tab_frame, style="Modern.TFrame", padding=(0, 12, 0, 0))
            info_frame.pack(fill=tk.X)
            
            # ファイル情報の表示
            if output_path:
                info_label = ttk.Label(
                    info_frame, 
                    text=f"保存先: {output_path}", 
                    style="Info.TLabel"
                )
                info_label.pack(side=tk.LEFT, padx=5)
            
            # ボタンフレーム
            button_frame = ttk.Frame(info_frame, style="Modern.TFrame")
            button_frame.pack(side=tk.RIGHT)
            
            # 保存先を開くボタン
            if output_path and os.path.exists(output_path):
                open_folder_button = ttk.Button(
                    button_frame, 
                    text="保存先フォルダを開く", 
                    command=lambda path=output_path: self._open_folder(path),
                    style="Modern.TButton"
                )
                open_folder_button.pack(side=tk.RIGHT, padx=5, pady=5)
            
            # ファイルを開くボタン
            if output_path and os.path.exists(output_path):
                open_file_button = ttk.Button(
                    button_frame, 
                    text="ファイルを開く", 
                    command=lambda path=output_path: self._open_file(path),
                    style="Modern.TButton"
                )
                open_file_button.pack(side=tk.RIGHT, padx=5, pady=5)
            
            # セグメント情報があれば、詳細タブを追加
            if segments:
                # 詳細タブの作成
                detail_tab = ttk.Frame(self.notebook, style="Modern.TFrame", padding=12)
                self.notebook.add(detail_tab, text=f"{file_name} (詳細)")
                
                # 詳細テキスト表示エリアの作成
                detail_frame = ttk.Frame(detail_tab, style="Modern.TFrame")
                detail_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
                
                # 詳細テキスト表示ウィジェット
                detail_text = tk.Text(
                    detail_frame, 
                    wrap=tk.WORD, 
                    padx=15, 
                    pady=15,
                    bg=COLORS["bg_secondary"],
                    fg=COLORS["text_primary"],
                    font=("Segoe UI", 10),
                    relief="flat",
                    borderwidth=0,
                    highlightthickness=1,
                    highlightcolor=COLORS["border"],
                    selectbackground=COLORS["accent_primary"],
                    selectforeground=COLORS["text_light"]
                )
                detail_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                
                # スクロールバーの作成
                detail_scrollbar = ttk.Scrollbar(detail_frame, orient=tk.VERTICAL, command=detail_text.yview)
                detail_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                detail_text.config(yscrollcommand=detail_scrollbar.set)
                
                # 詳細テキストの挿入
                detail_text.tag_configure("timestamp", foreground=COLORS["accent_primary"], font=("Segoe UI", 10, "bold"))
                detail_text.tag_configure("text", foreground=COLORS["text_primary"], font=("Segoe UI", 10))
                
                for segment in segments:
                    start_time = self._format_time(segment.get("start", 0))
                    end_time = self._format_time(segment.get("end", 0))
                    segment_text = segment.get("text", "")
                    
                    timestamp = f"[{start_time} --> {end_time}] "
                    detail_text.insert(tk.END, timestamp, "timestamp")
                    detail_text.insert(tk.END, segment_text + "\n\n", "text")
                
                detail_text.config(state=tk.DISABLED)  # 読み取り専用に設定
        
        # 閉じるボタンフレーム
        close_frame = ttk.Frame(main_frame, style="Modern.TFrame")
        close_frame.pack(fill=tk.X, pady=12)
        
        # 閉じるボタン
        close_button = ttk.Button(
            close_frame, 
            text="閉じる", 
            command=self.window.destroy,
            style="Modern.TButton"
        )
        close_button.pack(side=tk.RIGHT, padx=5, pady=5)
    
    def _format_time(self, seconds):
        """
        秒数を時:分:秒形式に変換
        
        Args:
            seconds (float): 秒数
            
        Returns:
            str: 時:分:秒形式の文字列
        """
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return f"{int(h):02d}:{int(m):02d}:{int(s):02d}.{int((seconds % 1) * 1000):03d}"
    
    def _open_folder(self, file_path):
        """
        ファイルの保存フォルダを開く
        
        Args:
            file_path (str): ファイルパス
        """
        folder_path = os.path.dirname(file_path)
        try:
            if platform.system() == "Windows":
                os.startfile(folder_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", folder_path])
            else:  # Linux
                subprocess.run(["xdg-open", folder_path])
        except Exception as e:
            messagebox.showerror("エラー", f"フォルダを開けませんでした: {str(e)}")
    
    def _open_file(self, file_path):
        """
        ファイルを開く
        
        Args:
            file_path (str): ファイルパス
        """
        try:
            if platform.system() == "Windows":
                os.startfile(file_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", file_path])
            else:  # Linux
                subprocess.run(["xdg-open", file_path])
        except Exception as e:
            messagebox.showerror("エラー", f"ファイルを開けませんでした: {str(e)}") 