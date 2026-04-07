#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自定义异常模块

定义 ResearchMate 项目中的各类异常，提供清晰的错误定位和处理机制
"""


class ResearchMateError(Exception):
    """ResearchMate 基础异常类"""
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}
    
    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            'error_type': self.__class__.__name__,
            'message': self.message,
            'details': self.details
        }


# ===========================================
# 采集相关异常
# ===========================================

class CollectionError(ResearchMateError):
    """素材采集失败的异常"""
    pass


class SourceNotAvailableError(CollectionError):
    """采集源不可用（网络问题、服务关闭等）"""
    pass


class RateLimitError(CollectionError):
    """触发频率限制"""
    pass


class AuthenticationError(CollectionError):
    """认证失败（API Key 无效、Token 过期等）"""
    pass


# ===========================================
# 解析相关异常
# ===========================================

class ParseError(ResearchMateError):
    """内容解析失败"""
    pass


class HTMLParseError(ParseError):
    """HTML 解析失败"""
    pass


class DataExtractionError(ParseError):
    """数据提取失败"""
    pass


# ===========================================
# 分类相关异常
# ===========================================

class ClassificationError(ResearchMateError):
    """素材分类失败"""
    pass


class LowConfidenceError(ClassificationError):
    """分类置信度过低"""
    pass


# ===========================================
# 评估相关异常
# ===========================================

class EvaluationError(ResearchMateError):
    """质量评估失败"""
    pass


class InvalidScoreError(EvaluationError):
    """评分无效（超出范围、NaN 等）"""
    pass


# ===========================================
# 导出相关异常
# ===========================================

class ExportError(ResearchMateError):
    """导出失败"""
    pass


class FileWriteError(ExportError):
    """文件写入失败"""
    pass


class InvalidFormatError(ExportError):
    """导出格式无效"""
    pass


# ===========================================
# 配置相关异常
# ===========================================

class ConfigurationError(ResearchMateError):
    """配置错误"""
    pass


class MissingConfigError(ConfigurationError):
    """缺少必要配置项"""
    pass


class InvalidConfigValueError(ConfigurationError):
    """配置值无效"""
    pass


# ===========================================
# 数据处理相关异常
# ===========================================

class DataValidationError(ResearchMateError):
    """数据验证失败"""
    pass


class EmptyDataError(DataValidationError):
    """数据为空"""
    pass


class DuplicateDataError(DataValidationError):
    """重复数据"""
    pass


# ===========================================
# 使用示例
# ===========================================

if __name__ == '__main__':
    # 示例：抛出和捕获自定义异常
    try:
        # 模拟采集失败
        raise SourceNotAvailableError(
            "无法访问 36 氪网站",
            {'source': '36kr', 'url': 'https://36kr.com', 'retry_after': 300}
        )
    except CollectionError as e:
        print(f"采集错误：{e.message}")
        print(f"详细信息：{e.to_dict()}")
    
    # 示例：检查配置
    try:
        config = {}
        if 'api_key' not in config:
            raise MissingConfigError(
                "缺少 API 密钥配置",
                {'required_field': 'api_key', 'config_file': 'config.yaml'}
            )
    except ConfigurationError as e:
        print(f"配置错误：{e.message}")
