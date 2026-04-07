#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试分类器模块

验证 MaterialClassifier 的分类准确性和功能完整性
"""

import sys
import os
import unittest
from pathlib import Path

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from classifier import MaterialClassifier


class TestMaterialClassifier(unittest.TestCase):
    """分类器测试类"""
    
    def setUp(self):
        """每个测试前的准备工作"""
        self.classifier = MaterialClassifier()
    
    def test_classify_financial_data(self):
        """测试财务数据分类"""
        material = {
            'title': '比亚迪 Q4 财报：营收增长 42%，净利润翻倍',
            'content': '比亚迪发布 2025 年第四季度财报，实现营业收入 2,150 亿元，同比增长 42%；净利润 185 亿元，同比增长 68%。毛利率提升至 22.5%。',
            'source': '财经日报'
        }
        
        result = self.classifier.classify(material)
        
        self.assertEqual(result['category'], '财务数据')
        self.assertEqual(result['material_type'], '事实数据')
        self.assertTrue(result['has_data'])
    
    def test_classify_market_data(self):
        """测试市场数据分类"""
        material = {
            'title': '新能源汽车市场份额分析',
            'content': '2025 年新能源汽车市场渗透率达到 35%，比亚迪以 18.5% 的市场份额位居第一，特斯拉中国占 12.3%。全年销量突破 950 万辆，同比增长 38%。',
            'source': '艾瑞咨询'
        }
        
        result = self.classifier.classify(material)
        
        self.assertIn(result['category'], ['市场数据', '财务数据'])
        self.assertTrue(result['has_data'])
    
    def test_classify_executive_opinion(self):
        """测试高管言论分类"""
        material = {
            'title': '李斌：蔚来将在 2026 年实现盈利',
            'content': '蔚来 CEO 李斌在投资者大会上表示，公司预计 2026 年 Q4 实现单季度盈利。他强调，随着规模效应释放和成本控制优化，蔚来的盈利能力将持续提升。',
            'source': '36 氪'
        }
        
        result = self.classifier.classify(material)
        
        self.assertEqual(result['category'], '高管言论')
        self.assertEqual(result['material_type'], '专家观点')
    
    def test_classify_product_innovation(self):
        """测试产品创新分类"""
        material = {
            'title': '宁德时代发布新一代神行电池，能量密度提升 30%',
            'content': '宁德时代正式发布第四代神行超充电池，采用磷酸锰铁锂正极材料，能量密度达到 255Wh/kg，较上一代提升 30%。支持 5C 超快充，10 分钟可充电至 80%。',
            'source': '机器之心'
        }
        
        result = self.classifier.classify(material)
        
        self.assertEqual(result['category'], '产品创新')
        self.assertEqual(result['material_type'], '典型案例')
    
    def test_has_data_detection(self):
        """测试数据检测功能"""
        # 包含数据的文本
        material_with_data = {
            'title': '测试标题',
            'content': '营收 100 亿元，同比增长 25%',
            'source': '测试'
        }
        result = self.classifier.classify(material_with_data)
        self.assertTrue(result['has_data'])
        
        # 不包含数据的文本
        material_without_data = {
            'title': '测试标题',
            'content': '这是一个普通的描述性文本，没有具体数字',
            'source': '测试'
        }
        result = self.classifier.classify(material_without_data)
        self.assertFalse(result['has_data'])
    
    def test_batch_classification(self):
        """测试批量分类"""
        materials = [
            {
                'title': '财报数据',
                'content': '净利润增长 50%',
                'source': '测试'
            },
            {
                'title': '高管访谈',
                'content': 'CEO 表示未来很乐观',
                'source': '测试'
            }
        ]
        
        results = self.classifier.classify_batch(materials)
        
        self.assertEqual(len(results), 2)
        self.assertIn(results[0]['category'], ['财务数据', '市场数据', '高管言论'])
    
    def test_category_statistics(self):
        """测试分类统计功能"""
        materials = [
            {'category': '财务数据', 'material_type': '事实数据', 'has_data': True},
            {'category': '财务数据', 'material_type': '事实数据', 'has_data': True},
            {'category': '高管言论', 'material_type': '专家观点', 'has_data': False},
            {'category': '产品创新', 'material_type': '典型案例', 'has_data': True}
        ]
        
        stats = self.classifier.get_statistics(materials)
        
        self.assertEqual(stats['total'], 4)
        self.assertEqual(stats['by_type']['事实数据'], 2)
        self.assertEqual(stats['by_type']['专家观点'], 1)
        self.assertEqual(stats['with_data'], 3)
    
    def test_empty_material(self):
        """测试空内容处理"""
        material = {
            'title': '',
            'content': '',
            'source': ''
        }
        
        result = self.classifier.classify(material)
        
        self.assertEqual(result['category'], '其他')
        self.assertFalse(result['has_data'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
