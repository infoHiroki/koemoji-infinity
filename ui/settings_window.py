#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
設定ウィンドウモジュール
アプリケーションの設定画面を定義
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

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
        
        # ウィンドウの作成
        self.window = tk.Toplevel(parent)
        self.window.title("設定")
        self.window.geometry("500x400")
        self.window.transient(parent)
        self.window.grab_set()
        self.window.configure(bg=COLORS["bg_primary"])
        
        # スタイルの設定
        self._setup_styles()
        
        # メインフレームの作成
        self.main_frame = ttk.Frame(self.window, padding=15, style="Modern.TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # モデル設定
        self._create_model_settings()
        
        # 言語設定
        self._create_language_settings()
        
        # 出力ディレクトリ設定
        self._create_output_settings()
        
        # 実行ボタンエリア
        self._create_action_buttons()
        
        # 設定を読み込み
        self._load_settings()
    
    def _setup_styles(self):
        """スタイルの設定"""
        style = ttk.Style()
        
        # フォント定義
        heading_font = ("Segoe UI", 12, "bold")
        normal_font = ("Segoe UI", 10)
        small_font = ("Segoe UI", 9)
        button_font = ("Segoe UI", 10, "bold")
        
        # フレームのスタイル
        style.configure("Modern.TFrame", background=COLORS["bg_primary"])
        
        # ラベルフレームのスタイル
        style.configure("Modern.TLabelframe", background=COLORS["bg_primary"])
        style.configure("Modern.TLabelframe.Label", 
                       background=COLORS["bg_primary"], 
                       foreground=COLORS["accent_primary"], 
                       font=heading_font)
        
        # ラベルのスタイル
        style.configure("Modern.TLabel", 
                       background=COLORS["bg_primary"], 
                       foreground=COLORS["text_primary"], 
                       font=normal_font)
        
        # 説明ラベルのスタイル
        style.configure("Description.TLabel", 
                       background=COLORS["bg_primary"], 
                       foreground=COLORS["text_secondary"], 
                       font=small_font)
        
        # ボタンのスタイル
        style.configure("Modern.TButton", 
                       background=COLORS["accent_primary"],
                       foreground=COLORS["text_light"],
                       font=button_font,
                       padding=(10, 6))
        style.map("Modern.TButton",
                 background=[("active", COLORS["accent_secondary"]), 
                            ("pressed", COLORS["accent_secondary"]),
                            ("disabled", "#A0A0A0"),
                            ("readonly", COLORS["accent_primary"]),
                            ("!disabled", COLORS["accent_primary"])],
                 foreground=[("active", COLORS["text_light"]), 
                            ("pressed", COLORS["text_light"]),
                            ("disabled", "#D0D0D0"),
                            ("readonly", COLORS["text_light"]),
                            ("!disabled", COLORS["text_light"])])
        
        # 保存ボタンのスタイル
        style.configure("Save.TButton", 
                       background=COLORS["success"],
                       foreground=COLORS["text_light"],
                       font=button_font,
                       padding=(15, 8))
        style.map("Save.TButton",
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
        
        # コンボボックスのスタイル
        style.configure("Modern.TCombobox", 
                       background=COLORS["accent_primary"],
                       fieldbackground=COLORS["bg_secondary"],
                       foreground=COLORS["text_primary"],
                       arrowcolor=COLORS["accent_secondary"],
                       font=normal_font)
        style.map("Modern.TCombobox",
                 fieldbackground=[("readonly", COLORS["bg_secondary"])],
                 selectbackground=[("readonly", COLORS["accent_primary"])],
                 selectforeground=[("readonly", COLORS["text_light"])])
        
        # エントリのスタイル
        style.configure("Modern.TEntry", 
                       fieldbackground=COLORS["bg_secondary"],
                       foreground=COLORS["text_primary"],
                       font=normal_font)
        
        # セパレータのスタイル
        style.configure("Modern.TSeparator", background=COLORS["border"])
    
    def _create_model_settings(self):
        """モデル設定エリアを作成"""
        # モデル設定フレーム
        model_frame = ttk.LabelFrame(self.main_frame, text="Whisperモデル設定", padding=12, style="Modern.TLabelframe")
        model_frame.pack(fill=tk.X, padx=5, pady=8)
        
        # モデルサイズの説明ラベル
        model_label = ttk.Label(model_frame, text="モデルサイズ:", style="Modern.TLabel")
        model_label.pack(anchor=tk.W, pady=(0, 5))
        
        # モデルサイズ選択コンボボックス
        self.model_var = tk.StringVar()
        model_combo = ttk.Combobox(model_frame, textvariable=self.model_var, state="readonly", style="Modern.TCombobox")
        model_combo["values"] = ["tiny", "base", "small", "medium", "large"]
        model_combo.pack(fill=tk.X, pady=5)
        
        # モデルサイズの説明
        descriptions = {
            "tiny": "最小モデル (約39MB) - 速度優先、低負荷、精度は限定的",
            "base": "基本モデル (約74MB) - バランス型、一般的な用途に適切",
            "small": "小型モデル (約244MB) - バランス型、精度と速度のバランスが良好",
            "medium": "中型モデル (約769MB) - 高精度、複雑な音声に適している",
            "large": "大型モデル (約2.87GB) - 最高精度、多言語対応が最も優れている"
        }
        
        # 説明テキストエリア
        self.model_desc_var = tk.StringVar()
        model_desc_label = ttk.Label(
            model_frame, 
            textvariable=self.model_desc_var, 
            wraplength=450, 
            justify=tk.LEFT, 
            style="Description.TLabel"
        )
        model_desc_label.pack(fill=tk.X, pady=5)
        
        # 説明テキスト更新関数
        def update_description(*args):
            selected = self.model_var.get()
            if selected in descriptions:
                self.model_desc_var.set(descriptions[selected])
        
        # 選択変更時の処理を登録
        self.model_var.trace("w", update_description)
    
    def _create_language_settings(self):
        """言語設定エリアを作成"""
        # 言語設定フレーム
        lang_frame = ttk.LabelFrame(self.main_frame, text="言語設定", padding=12, style="Modern.TLabelframe")
        lang_frame.pack(fill=tk.X, padx=5, pady=8)
        
        # 言語設定の説明ラベル
        lang_label = ttk.Label(lang_frame, text="文字起こし対象の言語:", style="Modern.TLabel")
        lang_label.pack(anchor=tk.W, pady=(0, 5))
        
        # 言語選択コンボボックス
        self.lang_var = tk.StringVar()
        lang_combo = ttk.Combobox(lang_frame, textvariable=self.lang_var, style="Modern.TCombobox")
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
        output_frame = ttk.LabelFrame(self.main_frame, text="出力設定", padding=12, style="Modern.TLabelframe")
        output_frame.pack(fill=tk.X, padx=5, pady=8)
        
        # 出力ディレクトリの説明ラベル
        output_label = ttk.Label(output_frame, text="文字起こし結果の出力ディレクトリ:", style="Modern.TLabel")
        output_label.pack(anchor=tk.W, pady=(0, 5))
        
        # 出力ディレクトリ選択エリア
        dir_frame = ttk.Frame(output_frame, style="Modern.TFrame")
        dir_frame.pack(fill=tk.X, pady=5)
        
        # 出力ディレクトリパステキストボックス
        self.output_dir_var = tk.StringVar()
        output_entry = ttk.Entry(dir_frame, textvariable=self.output_dir_var, style="Modern.TEntry")
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        # ディレクトリ選択ボタン
        browse_button = ttk.Button(
            dir_frame, 
            text="参照...", 
            command=self._browse_output_dir, 
            style="Modern.TButton"
        )
        browse_button.pack(side=tk.RIGHT, padx=5, pady=5)
    
    def _create_action_buttons(self):
        """アクションボタンエリアを作成"""
        # セパレータ
        separator = ttk.Separator(self.main_frame, orient=tk.HORIZONTAL, style="Modern.TSeparator")
        separator.pack(fill=tk.X, padx=5, pady=12)
        
        # ボタンフレーム
        button_frame = ttk.Frame(self.main_frame, style="Modern.TFrame")
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # キャンセルボタン
        cancel_button = ttk.Button(
            button_frame, 
            text="キャンセル", 
            command=self.window.destroy, 
            style="Modern.TButton"
        )
        cancel_button.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # 保存ボタン
        save_button = ttk.Button(
            button_frame, 
            text="保存", 
            command=self._save_settings, 
            style="Save.TButton"
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