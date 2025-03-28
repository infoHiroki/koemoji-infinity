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
        self.window.title("コエモジ∞ - 設定")
        self.window.geometry("520x550")  # 高さを小さくする
        self.window.minsize(450, 550)    # 最小サイズも調整
        self.window.transient(parent)
        self.window.grab_set()
        self.window.configure(bg=COLORS["bg_primary"])
        
        # 親ウィンドウと同じアイコンを使用
        try:
            self.window.iconphoto(True, parent.iconphoto_master)
        except Exception:
            pass
        
        # ウィンドウを画面中央に配置
        self._center_window()
        
        # スタイルの設定
        self._setup_styles()
        
        # メインレイアウト作成
        self._create_main_layout()
        
        # 初期設定を読み込み
        self._load_settings()
    
    def _setup_styles(self):
        """スタイルの設定"""
        style = ttk.Style()
        
        # 標準フォント定義
        heading_font = ("游ゴシック", 13, "bold")  # フォントサイズを大きく
        normal_font = ("游ゴシック", 12)          # フォントサイズを大きく
        small_font = ("游ゴシック", 11)          # フォントサイズを大きく
        
        # フレームのスタイル
        style.configure("TFrame", background=COLORS["bg_primary"])
        style.configure("Card.TFrame", background=COLORS["bg_secondary"])
        
        # ラベルのスタイル
        style.configure("TLabel", background=COLORS["bg_primary"], foreground=COLORS["text_primary"], font=normal_font)
        style.configure("Header.TLabel", background=COLORS["bg_primary"], foreground=COLORS["text_primary"], font=heading_font)
        style.configure("Card.TLabel", background=COLORS["bg_secondary"], foreground=COLORS["text_primary"], font=normal_font)
        style.configure("CardHeader.TLabel", background=COLORS["bg_secondary"], foreground=COLORS["text_primary"], font=heading_font)
        style.configure("Description.TLabel", background=COLORS["bg_primary"], foreground=COLORS["text_secondary"], font=small_font)

        # コンボボックスのスタイル
        style.configure("TCombobox", foreground=COLORS["text_primary"], font=normal_font)
        style.map("TCombobox", fieldbackground=[("readonly", COLORS["bg_secondary"])])
        
        # エントリのスタイル
        style.configure("TEntry", foreground=COLORS["text_primary"], font=normal_font)
        style.map("TEntry", fieldbackground=[("readonly", COLORS["bg_secondary"])])
        
        # セパレータのスタイル
        style.configure("TSeparator", background=COLORS["border"])
        
        # タブのスタイル設定
        style.configure("TNotebook", background=COLORS["bg_primary"], borderwidth=0)
        
        # タブのスタイル修正 - 非選択時は薄いグレー背景に黒文字、選択時も黒文字に変更
        style.configure("TNotebook.Tab", 
                        background=COLORS["border"],  # 非選択時は薄いグレー背景
                        foreground=COLORS["text_primary"], 
                        font=normal_font, 
                        padding=[12, 6], 
                        borderwidth=0)
        
        # タブマッピング - 選択時の文字色を黒に統一
        style.map("TNotebook.Tab", 
                  background=[("selected", COLORS["accent"]), 
                              ("active", COLORS["border"])],  # アクティブ時は薄いグレー
                  foreground=[("selected", COLORS["text_primary"]), 
                              ("active", COLORS["text_primary"])],  # 全て黒文字に統一
                  expand=[("selected", [1, 1, 1, 0])])

    def _create_main_layout(self):
        """メインレイアウトを作成"""
        # メインコンテナ
        self.main_frame = ttk.Frame(self.window, style="TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # タイトル
        title_label = ttk.Label(self.main_frame, text="アプリケーション設定", style="Header.TLabel")
        title_label.pack(anchor=tk.W, pady=(0, 15))
        
        # タブコントロールを作成
        self.tab_control = ttk.Notebook(self.main_frame)
        self.tab_control.pack(fill=tk.BOTH, expand=True)
        
        # タブページを作成
        self.model_tab = ttk.Frame(self.tab_control, style="TFrame")
        self.language_tab = ttk.Frame(self.tab_control, style="TFrame")
        self.output_tab = ttk.Frame(self.tab_control, style="TFrame")
        
        # タブをタブコントロールに追加
        self.tab_control.add(self.model_tab, text="モデル設定")
        self.tab_control.add(self.language_tab, text="言語設定")
        self.tab_control.add(self.output_tab, text="出力設定")
        
        # 各タブにコンテンツを作成
        self._create_model_tab()
        self._create_language_tab()
        self._create_output_tab()
        
        # アクションボタン
        self._create_action_buttons()
    
    def _create_model_tab(self):
        """モデル設定タブの内容を作成"""
        # コンテンツフレーム
        content = ttk.Frame(self.model_tab, style="TFrame")
        content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # モデルサイズ選択
        model_label = ttk.Label(content, text="モデルサイズ:", style="TLabel")
        model_label.pack(anchor=tk.W, pady=(0, 5))
        
        # モデルサイズ選択コンボボックス
        self.model_var = tk.StringVar()
        model_combo = ttk.Combobox(content, textvariable=self.model_var, state="readonly", width=20)
        model_combo["values"] = ["tiny", "base", "small", "medium", "large"]
        model_combo.pack(fill=tk.X, pady=2)
        
        # モデル説明
        self.model_desc_var = tk.StringVar()
        model_desc = ttk.Label(
            content, 
            textvariable=self.model_desc_var, 
            wraplength=450, 
            justify=tk.LEFT,
            style="Description.TLabel"
        )
        model_desc.pack(fill=tk.X, pady=(5, 0))
        
        # モデル選択変更時のイベント設定
        model_combo.bind("<<ComboboxSelected>>", self._update_model_description)
    
    def _create_language_tab(self):
        """言語設定タブの内容を作成"""
        # コンテンツフレーム
        content = ttk.Frame(self.language_tab, style="TFrame")
        content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # 言語選択
        lang_label = ttk.Label(content, text="文字起こしの言語:", style="TLabel")
        lang_label.pack(anchor=tk.W, pady=(0, 5))
        
        # 言語選択コンボボックス
        self.lang_var = tk.StringVar()
        lang_combo = ttk.Combobox(content, textvariable=self.lang_var, width=20)
        lang_options = [
            ("自動検出", ""),
            ("日本語", "ja"),
            ("英語", "en"),
            ("中国語", "zh"),
            ("ドイツ語", "de"),
            ("スペイン語", "es"),
            ("ロシア語", "ru"),
            ("韓国語", "ko"),
            ("フランス語", "fr"),
            ("ポルトガル語", "pt"),
            ("トルコ語", "tr"),
            ("ポーランド語", "pl"),
            ("イタリア語", "it")
        ]
        lang_combo["values"] = [name for name, code in lang_options]
        self.lang_options = {name: code for name, code in lang_options}
        lang_combo.pack(fill=tk.X, pady=2)
        
        # 言語説明
        lang_desc = ttk.Label(
            content,
            text="文字起こしを行う言語を選択します。自動検出を選ぶと、WhisperがAIで言語を判定します。",
            wraplength=450,
            justify=tk.LEFT,
            style="Description.TLabel"
        )
        lang_desc.pack(fill=tk.X, pady=(5, 0))
    
    def _create_output_tab(self):
        """出力設定タブの内容を作成"""
        # コンテンツフレーム
        content = ttk.Frame(self.output_tab, style="TFrame")
        content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # 出力ディレクトリ
        output_label = ttk.Label(content, text="文字起こし結果の出力先:", style="TLabel")
        output_label.pack(anchor=tk.W, pady=(0, 5))
        
        # 出力ディレクトリ選択エリア
        dir_frame = ttk.Frame(content, style="TFrame")
        dir_frame.pack(fill=tk.X, pady=2)
        
        # 出力ディレクトリパス
        self.output_dir_var = tk.StringVar()
        output_entry = ttk.Entry(dir_frame, textvariable=self.output_dir_var)
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        # 参照ボタン
        browse_button = tk.Button(
            dir_frame,
            text="参照...",
            command=self._browse_output_dir,
            bg=COLORS["accent"],
            fg=COLORS["text_light"],
            font=("游ゴシック", 9),
            relief="flat",
            borderwidth=0,
            padx=8,
            pady=2,
            activebackground=COLORS["accent_hover"],
            activeforeground=COLORS["text_light"]
        )
        browse_button.pack(side=tk.RIGHT)
        
        # 出力説明
        output_desc = ttk.Label(
            content,
            text="文字起こし結果のテキストファイルが保存されるフォルダを指定します。指定しない場合はデスクトップの「文字起こしデータ」フォルダに保存されます。",
            wraplength=450,
            justify=tk.LEFT,
            style="Description.TLabel"
        )
        output_desc.pack(fill=tk.X, pady=(5, 0))
    
    def _create_action_buttons(self):
        """アクションボタンエリアを作成"""
        button_frame = ttk.Frame(self.main_frame, style="TFrame")
        button_frame.pack(fill=tk.X, pady=(15, 0))
        
        # キャンセルボタン
        cancel_button = tk.Button(
            button_frame,
            text="キャンセル",
            command=self.window.destroy,
            bg=COLORS["bg_primary"],
            fg=COLORS["text_primary"],
            font=("游ゴシック", 10),
            relief="solid",
            borderwidth=1,
            padx=10,
            pady=5,
            activebackground=COLORS["border"],
            activeforeground=COLORS["text_primary"]
        )
        cancel_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # 保存ボタン
        save_button = tk.Button(
            button_frame,
            text="保存",
            command=self._save_settings,
            bg=COLORS["accent"],
            fg=COLORS["text_light"],
            font=("游ゴシック", 10),
            relief="flat",
            borderwidth=0,
            padx=15,
            pady=5,
            activebackground=COLORS["accent_hover"],
            activeforeground=COLORS["text_light"]
        )
        save_button.pack(side=tk.RIGHT)
    
    def _browse_output_dir(self):
        """出力ディレクトリ参照ダイアログを表示"""
        current_dir = self.output_dir_var.get()
        if current_dir and os.path.isdir(current_dir):
            initial_dir = current_dir
        else:
            initial_dir = os.path.dirname(os.path.abspath(__file__))
        
        # ディレクトリ選択ダイアログを表示
        selected_dir = filedialog.askdirectory(
            initialdir=initial_dir,
            title="文字起こし結果の出力先を選択"
        )
        
        if selected_dir:
            self.output_dir_var.set(selected_dir)
    
    def _center_window(self):
        """ウィンドウを画面中央に配置"""
        # ウィンドウのサイズを取得
        window_width = 520
        window_height = 550  # 高さを小さく変更
        
        # 親ウィンドウの位置とサイズを取得
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        # 親ウィンドウの中央に配置
        center_x = parent_x + int((parent_width - window_width) / 2)
        center_y = parent_y + int((parent_height - window_height) / 2)
        
        # 画面の範囲内に収める
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        
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
    
    def _update_model_description(self, event=None):
        """モデルサイズの説明を更新"""
        model = self.model_var.get()
        
        descriptions = {
            "tiny": "最小のモデル (約39M)。最速ですが精度は低めです。低スペックのPCやノートPCでも動作します。",
            "base": "小さいモデル (約74M)。精度と速度のバランスが良好です。一般的な使用に適しています。",
            "small": "中小モデル (約244M)。baseより精度が良く、一般的なPCで十分な速度で動作します。",
            "medium": "中型モデル (約769M)。高い精度を提供し、ある程度のGPUスペックが必要です。",
            "large": "最大のモデル (約1.5G)。最高の精度を提供しますが、高いGPUスペックが必要で処理時間も長くなります。"
        }
        
        if model in descriptions:
            self.model_desc_var.set(descriptions[model])
        else:
            self.model_desc_var.set("")
    
    def _load_settings(self):
        """設定を読み込み"""
        config = self.config_manager.get_config()
        
        # モデル設定
        model = config.get("model", "medium")
        self.model_var.set(model)
        self._update_model_description()
        
        # 言語設定
        language_code = config.get("language", "")
        language_name = "自動検出"
        
        # コードから言語名を逆引き
        for name, code in self.lang_options.items():
            if code == language_code:
                language_name = name
                break
        
        self.lang_var.set(language_name)
        
        # 出力ディレクトリ
        output_dir = config.get("output_directory", "output")
        self.output_dir_var.set(output_dir)
    
    def _save_settings(self):
        """設定を保存"""
        # 値を取得
        model = self.model_var.get()
        language_name = self.lang_var.get()
        language_code = self.lang_options.get(language_name, "")
        output_dir = self.output_dir_var.get()
        
        # 必須項目のチェック
        if not model:
            messagebox.showerror("エラー", "モデルサイズを選択してください。")
            return
        
        # 出力ディレクトリが指定されていない場合はデフォルト値を設定
        if not output_dir:
            output_dir = os.path.join(os.path.expanduser("~/Desktop"), "文字起こしデータ")
        
        # 設定を更新
        config = {
            "model": model,
            "language": language_code,
            "output_directory": output_dir
        }
        
        # 設定を保存
        self.config_manager.update_config(config)
        
        # ダイアログを閉じる
        self.window.destroy() 