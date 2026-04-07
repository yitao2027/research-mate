#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试评估器模块

验证 QualityEvaluator 的评分逻辑和准确性
"""

import sys
import os
import unittest
from pathlib import Path
from datetime import datetime, timedelta

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from evaluator import QualityEvaluator


class TestQualityEvaluator(unittest.TestCase):
    """评估器测试类"""
    
    def setUp(self):
        """每个测试前的准备工作"""
        self.evaluator = QualityEvaluator()
    
    def test_high_credibility_source(self):
        """测试高可信度来源评分"""
        material = {
            'title': '比亚迪财报',
            'content': '营收 2,150 亿元',
            'author': '巨潮资讯网',
            'url': 'http://www.cninfo.com.cn/report',
            'publish_date': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
            'has_data': True
        }
        
        result = self.evaluator.evaluate(material)
        
        self.assertGreaterEqual(result['score_breakdown']['credibility'], 0.90)
        self.assertIn(result['rating'], ['S', 'A'])  # 综合分应该很高（S 或 A）
    
    def test_medium_credibility_source(self):
        """测试中等可信度来源"""
        material = {
            'title': '某科技媒体报道',
            'content': '据传某公司将发布新产品',
            'author': '未知自媒体',
            'url': 'https://unknown-blog.com/post',
            'publish_date': (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d'),
            'has_data': False
        }
        
        result = self.evaluator.evaluate(material)
        
        self.assertLess(result['score_breakdown']['credibility'], 0.70)
    
    def test_timeliness_scoring(self):
        """测试时效性评分"""
        # 7 天内的文章应该得满分
        recent_material = {
            'title': '最新文章',
            'content': '内容',
            'author': '测试',
            'url': 'https://example.com',
            'publish_date': (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d'),
            'has_data': False
        }
        result = self.evaluator.evaluate(recent_material)
        self.assertEqual(result['score_breakdown']['timeliness'], 1.0)
        
        # 30 天前的文章分数降低
        old_material = {
            'title': '旧文章',
            'content': '内容',
            'author': '测试',
            'url': 'https://example.com',
            'publish_date': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
            'has_data': False
        }
        result = self.evaluator.evaluate(old_material)
        self.assertLess(result['score_breakdown']['timeliness'], 0.8)
    
    def test_completeness_scoring(self):
        """测试数据完整性评分"""
        # 数据丰富的内容
        rich_material = {
            'title': '详细财报分析',
            'content': '营业收入 2,150 亿元，同比增长 42%；净利润 185 亿元，同比增长 68%。毛利率提升至 22.5%，较上年同期增加 3.2 个百分点。研发投入 128 亿元。',
            'author': '财经日报',
            'url': 'https://example.com',
            'publish_date': (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'),
            'has_data': True
        }
        result = self.evaluator.evaluate(rich_material)
        self.assertGreaterEqual(result['score_breakdown']['completeness'], 0.8)
        
        # 数据匮乏的内容
        poor_material = {
            'title': '简单描述',
            'content': '某公司表现不错',
            'author': '测试',
            'url': 'https://example.com',
            'publish_date': (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'),
            'has_data': False
        }
        result = self.evaluator.evaluate(poor_material)
        self.assertLess(result['score_breakdown']['completeness'], 0.6)
    
    def test_rating_classification(self):
        """测试评级分类"""
        # S 级（>=0.85）
        s_material = {
            'title': '高质量报告',
            'content': '详细数据内容 100 亿元，增长 50%',
            'author': '巨潮资讯网',
            'url': 'http://www.cninfo.com.cn',
            'publish_date': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
            'has_data': True
        }
        result = self.evaluator.evaluate(s_material)
        self.assertEqual(result['rating'], 'S')
        
        # A 级（>=0.75）
        a_material = {
            'title': '较好报告',
            'content': '一些数据 80 亿元',
            'author': '36 氪',
            'url': 'https://36kr.com',
            'publish_date': (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d'),
            'has_data': True
        }
        result = self.evaluator.evaluate(a_material)
        self.assertIn(result['rating'], ['A', 'B'])
    
    def test_recommendation_reasons(self):
        """测试推荐理由生成"""
        material = {
            'title': '优质素材',
            'content': '营收 200 亿元，同比增长 45%，数据来源权威',
            'author': '巨潮资讯网',
            'url': 'http://www.cninfo.com.cn',
            'publish_date': (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'),
            'has_data': True
        }
        
        result = self.evaluator.evaluate(material)
        
        self.assertIn('来源权威性高', result['recommendation_reasons'])
        self.assertIn('信息时效性强（7 天内）', result['recommendation_reasons'])
    
    def test_batch_evaluation(self):
        """测试批量评估"""
        materials = [
            {
                'title': '素材 1',
                'content': '内容 100 亿',
                'author': '巨潮资讯网',
                'url': 'http://www.cninfo.com.cn',
                'publish_date': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
                'has_data': True
            },
            {
                'title': '素材 2',
                'content': '普通内容',
                'author': '未知',
                'url': 'https://unknown.com',
                'publish_date': (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d'),
                'has_data': False
            }
        ]
        
        results = self.evaluator.evaluate_batch(materials)
        
        self.assertEqual(len(results), 2)
        self.assertGreater(results[0]['score'], results[1]['score'])
    
    def test_missing_publish_date(self):
        """测试缺失发布日期的处理"""
        material = {
            'title': '无日期文章',
            'content': '内容',
            'author': '测试',
            'url': 'https://example.com',
            'publish_date': '',
            'has_data': False
        }
        
        result = self.evaluator.evaluate(material)
        
        self.assertEqual(result['score_breakdown']['timeliness'], 0.50)


if __name__ == '__main__':
    unittest.main(verbosity=2)
