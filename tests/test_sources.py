#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试采集源模块

验证 BaseSource 和具体采集源的功能
"""

import sys
import os
import unittest
from pathlib import Path
from datetime import datetime, timedelta

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from sources.base_source import BaseSource, RequestError, ParseError
from sources.tech_media_source import TechMediaSource


class ConcreteTestSource(BaseSource):
    """用于测试的具体实现类"""
    def fetch(self, topic: str, days_back: int = 7):
        return []


class TestBaseSource(unittest.TestCase):
    """基类测试"""
    
    def test_extract_publish_date_various_formats(self):
        """测试多种日期格式提取"""
        source = ConcreteTestSource({'name': 'test'})
        
        # 测试 YYYY-MM-DD
        self.assertEqual(
            source._extract_publish_date('发布于 2024-01-15'),
            '2024-01-15'
        )
        
        # 测试 YYYY 年 MM 月 DD 日
        self.assertEqual(
            source._extract_publish_date('2024 年 1 月 15 日发布'),
            '2024-01-15'
        )
        
        # 测试 YYYY/MM/DD
        self.assertEqual(
            source._extract_publish_date('时间：2024/01/15'),
            '2024-01-15'
        )
        
        # 测试无效日期
        result = source._extract_publish_date('没有日期')
        self.assertIsNone(result)  # 无效日期返回 None
    
    def test_extract_text_safety(self):
        """测试安全文本提取"""
        source = ConcreteTestSource({'name': 'test'})
        
        # None 元素
        self.assertEqual(source._extract_text(None, '默认值'), '默认值')
        
        # 空字符串
        self.assertEqual(source._extract_text('', '默认'), '')


class TestTechMediaSource(unittest.TestCase):
    """科技媒体采集源测试"""
    
    def setUp(self):
        self.source = TechMediaSource({'name': '36kr', 'url': 'https://36kr.com'})
    
    def test_is_within_date(self):
        """测试日期范围判断"""
        # 3 天前应该在范围内
        three_days_ago = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
        self.assertTrue(self.source._is_within_date(three_days_ago, 7))
        
        # 10 天前应该超出 7 天范围
        ten_days_ago = (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d')
        self.assertFalse(self.source._is_within_date(ten_days_ago, 7))
        
        # 无效日期应该返回 False
        self.assertFalse(self.source._is_within_date('invalid-date', 7))
    
    def test_fallback_data_generation(self):
        """测试降级数据生成"""
        materials = self.source._fallback_data('人工智能', 7)
        
        self.assertGreater(len(materials), 0)
        
        # 检查返回的数据结构
        for material in materials:
            self.assertIn('title', material)
            self.assertIn('content', material)
            self.assertIn('source_type', material)
            self.assertIn('url', material)
            self.assertIn('publish_date', material)
            
            # 标题应该包含主题关键词
            self.assertIn('人工智能', material['title'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
