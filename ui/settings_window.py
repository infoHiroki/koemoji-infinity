#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
設定ウィンドウモジュール
アプリケーションの設定画面を定義
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

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

class SettingsWindow:
    """設定ウィンドウクラス"""
    
    def __init__(self, parent, config_manager):
        """
        初期化
        
        Args:
            parent (tk.Tk): 親ウィンドウ
            config_manager (ConfigManager): 設定管理オブジェクト
        """
        self.parent = parent
        self.config_manager = config_manager
        
        # 設定ウィンドウを作成
        self.window = tk.Toplevel(parent)
        self.window.title("設定")
        self.window.geometry("500x450")
        self.window.transient(parent)
        self.window.grab_set()
        self.window.configure(bg=COLORS["bg_primary"])
        
        # スタイルの設定
        self._setup_styles()
        
        # メインフレームの作成
        self.main_frame = ttk.Frame(self.window, padding=10, style="TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # モデル設定
        self._create_model_settings()
        
        # 言語設定
        self._create_language_settings()
        
        # 出力設定
        self._create_output_settings()
        
        # アクションボタン
        self._create_action_buttons()
        
        # 初期設定を読み込み
        self._load_settings()
    
    def _setup_styles(self):
        """スタイルの設定"""
        style = ttk.Style()
        
        # 標準フォント定義
        heading_font = ("Yu Gothic UI", 11, "bold")
        normal_font = ("Yu Gothic UI", 10)
        small_font = ("Yu Gothic UI", 9)
        
        # フレームのスタイル
        style.configure("TFrame", background=COLORS["bg_primary"])
        
        # ラベルフレームのスタイル
        style.configure("TLabelframe", background=COLORS["bg_primary"])
        style.configure("TLabelframe.Label", 
                       background=COLORS["bg_primary"], 
                       foreground=COLORS["text_primary"], 
                       font=heading_font)
        
        # ラベルのスタイル
        style.configure("TLabel", 
                       background=COLORS["bg_primary"], 
                       foreground=COLORS["text_primary"], 
                       font=normal_font)
        
        # 説明ラベルのスタイル
        style.configure("Description.TLabel", 
                       background=COLORS["bg_primary"], 
                       foreground=COLORS["text_secondary"], 
                       font=small_font)
        
        # セパレータのスタイル
        style.configure("TSeparator", background=COLORS["border"])
        
        # コンボボックスのスタイル
        style.configure("TCombobox", 
                       background=COLORS["bg_secondary"],
                       foreground=COLORS["text_primary"],
                       arrowcolor=COLORS["accent"],
                       font=normal_font)
        
        # エントリのスタイル
        style.configure("TEntry", 
                       fieldbackground=COLORS["bg_secondary"],
                       foreground=COLORS["text_primary"],
                       font=normal_font)
    
    def _create_model_settings(self):
        """モデル設定エリアを作成"""
        # モデル設定フレーム
        model_frame = ttk.LabelFrame(self.main_frame, text="Whisperモデル設定", padding=10)
        model_frame.pack(fill=tk.X, padx=5, pady=8)
        
        # モデルサイズの説明ラベル
        model_label = ttk.Label(model_frame, text="モデルサイズ:", style="TLabel")
        model_label.pack(anchor=tk.W, pady=(0, 5))
        
        # モデルサイズ選択コンボボックス
        self.model_var = tk.StringVar()
        model_combo = ttk.Combobox(model_frame, textvariable=self.model_var, state="readonly", style="TCombobox")
        model_combo["values"] = ["tiny", "base", "small", "medium", "large"]
        model_combo.pack(fill=tk.X, pady=5)
        
        # モデルサイズの説明
        self.model_desc_var = tk.StringVar()
        model_desc_label = ttk.Label(
            model_frame, 
            textvariable=self.model_desc_var, 
            wraplength=450, 
            justify=tk.LEFT, 
            style="Description.TLabel"
        )
        model_desc_label.pack(fill=tk.X, pady=5)
        
        # モデル選択時の説明更新
        model_combo.bind("<<ComboboxSelected>>", self._update_model_description)
    
    def _create_language_settings(self):
        """言語設定エリアを作成"""
        # 言語設定フレーム
        lang_frame = ttk.LabelFrame(self.main_frame, text="言語設定", padding=10)
        lang_frame.pack(fill=tk.X, padx=5, pady=8)
        
        # 言語設定の説明ラベル
        lang_label = ttk.Label(lang_frame, text="文字起こし対象の言語:", style="TLabel")
        lang_label.pack(anchor=tk.W, pady=(0, 5))
        
        # 言語選択コンボボックス
        self.lang_var = tk.StringVar()
        lang_combo = ttk.Combobox(lang_frame, textvariable=self.lang_var, style="TCombobox")
        lang_combo["values"] = ["", "ja", "en", "zh", "de", "es", "ru", "ko", "fr", "pt", "tr", "pl", "it"]
        lang_combo.pack(fill=tk.X, pady=5)
        
        # 言語の説明
        lang_desc_label = ttk.Label(
            lang_frame, 
            text="自動検出する場合は空欄にしてください。主要言語コード: ja(日本語), en(英語), zh(中国語), de(ドイツ語), es(スペイン語), ru(ロシア語), ko(韓国語), fr(フランス語), pt(ポルトガル語)", 
            wraplength=450, 
            justify=tk.LEFT, 
            style="Description.TLabel"
        )
        lang_desc_label.pack(fill=tk.X, pady=5)
    
    def _create_output_settings(self):
        """出力設定エリアを作成"""
        # 出力設定フレーム
        output_frame = ttk.LabelFrame(self.main_frame, text="出力設定", padding=10)
        output_frame.pack(fill=tk.X, padx=5, pady=8)
        
        # 出力ディレクトリの説明ラベル
        output_label = ttk.Label(output_frame, text="文字起こし結果の出力ディレクトリ:", style="TLabel")
        output_label.pack(anchor=tk.W, pady=(0, 5))
        
        # 出力ディレクトリ選択エリア
        dir_frame = ttk.Frame(output_frame, style="TFrame")
        dir_frame.pack(fill=tk.X, pady=5)
        
        # 出力ディレクトリパステキストボックス
        self.output_dir_var = tk.StringVar()
        output_entry = ttk.Entry(dir_frame, textvariable=self.output_dir_var, style="TEntry")
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        # ディレクトリ選択ボタン
        browse_button = tk.Button(
            dir_frame, 
            text="参照...", 
            command=self._browse_output_dir,
            bg=COLORS["accent"],
            fg=COLORS["text_light"],
            font=("Yu Gothic UI", 10),
            relief="flat",
            borderwidth=1,
            padx=10,
            pady=3,
            activebackground=COLORS["accent_hover"],
            activeforeground=COLORS["text_light"]
        )
        browse_button.pack(side=tk.RIGHT, padx=5, pady=5)
    
    def _create_action_buttons(self):
        """アクションボタンエリアを作成"""
        # セパレータ
        separator = ttk.Separator(self.main_frame, orient=tk.HORIZONTAL, style="TSeparator")
        separator.pack(fill=tk.X, padx=5, pady=12)
        
        # ボタンフレーム
        button_frame = ttk.Frame(self.main_frame, style="TFrame")
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # キャンセルボタン
        cancel_button = tk.Button(
            button_frame, 
            text="キャンセル", 
            command=self.window.destroy,
            bg=COLORS["bg_primary"],
            fg=COLORS["text_primary"],
            font=("Yu Gothic UI", 10),
            relief="solid",
            borderwidth=1,
            padx=10,
            pady=3,
            activebackground=COLORS["bg_secondary"],
            activeforeground=COLORS["text_primary"]
        )
        cancel_button.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # 保存ボタン
        save_button = tk.Button(
            button_frame, 
            text="保存", 
            command=self._save_settings,
            bg=COLORS["success"],
            fg=COLORS["text_light"],
            font=("Yu Gothic UI", 10),
            relief="flat",
            borderwidth=1,
            padx=15,
            pady=5,
            activebackground="#0B6A0B",
            activeforeground=COLORS["text_light"]
        )
        save_button.pack(side=tk.RIGHT, padx=5, pady=5)
    
    def _browse_output_dir(self):
        """出力ディレクトリ選択ダイアログを表示"""
        current_dir = self.output_dir_var.get()
        if not current_dir or not os.path.isdir(current_dir):
            current_dir = os.path.expanduser("~")
        
        directory = filedialog.askdirectory(
            initialdir=current_dir,
            title="出力ディレクトリを選択"
        )
        
        if directory:
            self.output_dir_var.set(directory)
    
    def _load_settings(self):
        """設定を読み込み"""
        # モデル設定の読み込み
        model = self.config_manager.get_model()
        if model:
            self.model_var.set(model)
        else:
            self.model_var.set("small")  # デフォルト値
        
        # 言語設定の読み込み
        language = self.config_manager.get_language()
        if language:
            self.lang_var.set(language)
        
        # 出力ディレクトリの読み込み
        output_dir = self.config_manager.get_output_directory()
        if output_dir and os.path.isdir(output_dir):
            self.output_dir_var.set(output_dir)
        else:
            # デフォルトは現在のディレクトリ
            self.output_dir_var.set(os.getcwd())
    
    def _save_settings(self):
        """設定を保存"""
        # モデルの保存
        model = self.model_var.get()
        if model:
            self.config_manager.set_model(model)
        
        # 言語の保存
        language = self.lang_var.get()
        self.config_manager.set_language(language)
        
        # 出力ディレクトリの保存
        output_dir = self.output_dir_var.get()
        if output_dir:
            # ディレクトリが存在するか確認
            if not os.path.isdir(output_dir):
                try:
                    # ディレクトリが存在しない場合は作成
                    os.makedirs(output_dir, exist_ok=True)
                except Exception as e:
                    messagebox.showerror("エラー", f"出力ディレクトリの作成に失敗しました: {str(e)}")
                    return
            
            self.config_manager.set_output_directory(output_dir)
        
        # 設定を保存
        self.config_manager.save_config()
        
        # ウィンドウを閉じる
        self.window.destroy() 