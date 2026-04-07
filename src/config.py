"""
config.py - 配置管理模块
负责加载和管理全局配置参数
"""

import os
import json
from typing import Dict, Any, Optional
from pathlib import Path


class Config:
    """配置管理器 - 单例模式"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self.config = self._load_default_config()
        self._load_user_config()
    
    def _load_default_config(self) -> Dict[str, Any]:
        """加载默认配置"""
        return {
            # 采集器配置
            "collector": {
                "max_pages_per_source": 10,  # 每个来源最多采集页数
                "request_timeout": 30,  # 请求超时时间（秒）
                "retry_times": 3,  # 失败重试次数
                "user_agent": "ResearchMate/0.1.0 (Commercial Research Assistant)"
            },
            
            # 分类器配置
            "classifier": {
                "confidence_threshold": 0.7,  # 分类置信度阈值
                "enable_auto_tagging": True,  # 是否自动打标签
                "max_tags_per_material": 5  # 每个素材最多标签数
            },
            
            # 评估器配置
            "evaluator": {
                "quality_weights": {
                    "source_credibility": 0.3,  # 来源可信度权重
                    "timeliness": 0.2,  # 时效性权重
                    "completeness": 0.25,  # 信息完整度权重
                    "cross_validation": 0.25  # 交叉验证权重
                },
                "high_quality_threshold": 80,  # 高质量分数线
                "low_quality_threshold": 60  # 低质量分数线
            },
            
            # 导出器配置
            "exporter": {
                "default_format": "markdown",  # 默认导出格式
                "output_dir": "./output",  # 输出目录
                "include_raw_data": False  # 是否包含原始数据
            },
            
            # 日志配置
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "file": "research_mate.log"
            }
        }
    
    def _load_user_config(self):
        """加载用户自定义配置（如果存在）"""
        config_paths = [
            Path.home() / ".research_mate" / "config.json",
            Path("./config.json"),
            Path("./research_mate_config.json")
        ]
        
        for config_path in config_paths:
            if config_path.exists():
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        user_config = json.load(f)
                        self._merge_config(user_config)
                    print(f"✓ 已加载用户配置文件：{config_path}")
                    return
                except Exception as e:
                    print(f"⚠ 读取配置文件失败：{e}")
    
    def _merge_config(self, user_config: Dict[str, Any]):
        """合并用户配置到默认配置（递归深度合并）"""
        for key, value in user_config.items():
            if key in self.config and isinstance(self.config[key], dict) and isinstance(value, dict):
                self._merge_config_recursive(self.config[key], value)
            else:
                self.config[key] = value
    
    def _merge_config_recursive(self, base: Dict, override: Dict):
        """递归合并配置字典"""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config_recursive(base[key], value)
            else:
                base[key] = value
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        获取配置值（支持点号分隔的路径）
        
        Args:
            key_path: 配置键路径，如 "collector.max_pages_per_source"
            default: 默认值
            
        Returns:
            配置值
        """
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path: str, value: Any):
        """
        设置配置值（支持点号分隔的路径）
        
        Args:
            key_path: 配置键路径
            value: 配置值
        """
        keys = key_path.split('.')
        config = self.config
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value
    
    def save_to_file(self, filepath: str):
        """保存当前配置到文件"""
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 配置已保存到：{filepath}")
    
    def show(self):
        """打印当前配置（调试用）"""
        print("\n=== ResearchMate 配置 ===\n")
        print(json.dumps(self.config, ensure_ascii=False, indent=2))
        print()


# 全局配置实例
config = Config()


# 便捷函数
def get_config(key_path: str, default: Any = None) -> Any:
    """获取配置值的便捷函数"""
    return config.get(key_path, default)


def set_config(key_path: str, value: Any):
    """设置配置值的便捷函数"""
    config.set(key_path, value)


# 使用示例
if __name__ == "__main__":
    cfg = Config()
    
    # 读取配置
    timeout = cfg.get("collector.request_timeout")
    print(f"请求超时时间：{timeout}秒")
    
    # 修改配置
    cfg.set("collector.max_pages_per_source", 20)
    
    # 保存配置
    cfg.save_to_file("./my_config.json")
    
    # 显示全部配置
    cfg.show()
