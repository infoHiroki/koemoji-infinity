#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
設定管理モジュール
アプリケーションの設定を管理する
"""

import os
import json
import datetime
import logging

# ロガーの設定
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class ConfigManager:
    """設定管理クラス"""
    
    def __init__(self, config_file="config.json"):
        """
        初期化
        
        Args:
            config_file (str): 設定ファイルのパス
        """
        # 設定ファイルのパスを絶対パスに変換
        if not os.path.isabs(config_file):
            # 相対パスの場合は、現在の作業ディレクトリからの絶対パスに変換
            config_file = os.path.abspath(config_file)
        
        self.config_file = config_file
        self.config = self._load_config()
        
    def _load_config(self):
        """
        設定ファイルを読み込む
        
        Returns:
            dict: 設定データ
        """
        # デフォルト設定
        default_config = {
            "model": "small",
            "language": "",  # 空欄=自動検出
            "output_dir": os.path.join(os.path.expanduser("~"), "Documents"),
            "timestamp_format": "[%H:%M:%S.%f]",
            "use_gpu": True,
            "threads": 4,
            "theme_mode": "light",
            "history": []
        }
        
        # 設定ファイルが存在する場合は読み込む
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    
                    # デフォルト設定とマージ
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
                    
                    return config
            except Exception as e:
                logger.error(f"設定ファイルの読み込みに失敗しました: {e}")
        
        # 設定ファイルが存在しない場合や読み込みに失敗した場合はデフォルト設定を使用
        return default_config
    
    def save(self):
        """設定ファイルを保存"""
        try:
            # ディレクトリが存在することを確認
            config_dir = os.path.dirname(self.config_file)
            if config_dir and not os.path.exists(config_dir):
                os.makedirs(config_dir)
            
            # 設定ファイルを保存
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.config, f, ensure_ascii=False, indent=4)
            
            return True
        except Exception as e:
            logger.error(f"設定の保存に失敗しました: {e}")
            return False
    
    def get(self, key, default=None):
        """
        設定値を取得
        
        Args:
            key (str): 設定キー
            default: デフォルト値
            
        Returns:
            設定値
        """
        return self.config.get(key, default)
    
    def set(self, key, value):
        """
        設定値を設定
        
        Args:
            key (str): 設定キー
            value: 設定値
        """
        self.config[key] = value
    
    def add_to_history(self, file_path, output_path, time_taken=None):
        """
        履歴に追加
        
        Args:
            file_path (str): 処理したファイルのパス
            output_path (str): 出力ファイルのパス
            time_taken (float, optional): 処理にかかった時間（秒）
        """
        history = self.config.get("history", [])
        
        # 新しい履歴項目
        new_entry = {
            "file": os.path.basename(file_path),
            "file_path": file_path,
            "output": os.path.basename(output_path),
            "output_path": output_path,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "model": self.get("model", "small")
        }
        
        if time_taken is not None:
            new_entry["time_taken"] = time_taken
        
        # 履歴の先頭に追加
        history.insert(0, new_entry)
        
        # 履歴の最大数を制限（最新の50件を保持）
        if len(history) > 50:
            history = history[:50]
        
        self.config["history"] = history
        self.save()
    
    def get_history(self):
        """
        履歴を取得
        
        Returns:
            list: 履歴リスト
        """
        return self.config.get("history", []) 