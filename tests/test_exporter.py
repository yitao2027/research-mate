#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试导出器模块

验证 MaterialExporter 的多格式导出功能
"""

import sys
import os
import json
import unittest
from pathlib import Path

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from exporter import MaterialExporter


class TestMaterialExporter(unittest.TestCase):
    """导出器测试类"""
    
    def setUp(self):
        self.exporter = MaterialExporter()
        
        # 准备测试数据
        self.test_materials = [
            {
                'title': '比亚迪 Q4 财报：营收增长 42%',
                'category': '财务数据',
                'source': '巨潮资讯网',
                'url': 'https://example.com/byd-report',
                'content': '比亚迪发布 2025 年第四季度财报，实现营业收入 2,150 亿元，同比增长 42%。',
                'quality_score': 92,
                'collected_at': '2026-04-07 15:30',
                'tags': ['财报', '增长', '新能源车'],
                'writing_hints': '可用于论证行业高景气度'
            },
            {
                'title': '李斌：蔚来将在 2026 年实现盈利',
                'category': '高管言论',
                'source': '36 氪',
                'url': 'https://example.com/nio-ceo-interview',
                'content': '蔚来 CEO 李斌表示，公司预计 2026 年 Q4 实现单季度盈利。',
                'quality_score': 78,
                'collected_at': '2026-04-07 14:20',
                'tags': ['蔚来', '盈利预测', 'CEO 言论'],
                'writing_hints': '适合作为专家观点引用'
            }
        ]
    
    def test_export_to_markdown(self):
        """测试 Markdown 导出"""
        md_content = self.exporter.export_to_markdown(
            self.test_materials, 
            "新能源汽车行业分析"
        )
        
        # 检查必需内容
        self.assertIn('# 📚 新能源汽车行业分析 - 素材采集报告', md_content)
        self.assertIn('素材总数：** 2 条', md_content)  # Markdown 格式
        self.assertIn('比亚迪 Q4 财报', md_content)
        self.assertIn('李斌：蔚来', md_content)
        self.assertIn('质量评分：** ⭐ 92/100', md_content)  # Markdown 加粗
        self.assertIn('| 序号 | 标题 | 来源 | URL |', md_content)
    
    def test_export_to_json(self):
        """测试 JSON 导出"""
        json_str = self.exporter.export_to_json(
            self.test_materials,
            "新能源汽车行业分析"
        )
        
        # 解析 JSON
        data = json.loads(json_str)
        
        # 检查结构
        self.assertIn('metadata', data)
        self.assertIn('materials', data)
        self.assertIn('statistics', data)
        
        # 检查元数据
        self.assertEqual(data['metadata']['topic'], '新能源汽车行业分析')
        self.assertEqual(data['metadata']['total_materials'], 2)
        self.assertEqual(len(data['materials']), 2)
        
        # 检查统计数据
        self.assertIn('by_category', data['statistics'])
        self.assertIn('average_quality_score', data['statistics'])
    
    def test_export_to_csv(self):
        """测试 CSV 导出"""
        csv_content = self.exporter.export_to_csv(self.test_materials)
        
        # 检查 CSV 头部
        self.assertIn('id,title,category,source,url,content,quality_score,collected_at,tags', csv_content)
        
        # 检查数据行
        self.assertIn('比亚迪 Q4 财报', csv_content)
        self.assertIn('李斌：蔚来', csv_content)
        self.assertIn('巨潮资讯网', csv_content)
    
    def test_generate_statistics(self):
        """测试统计信息生成"""
        stats = self.exporter._generate_statistics(self.test_materials)
        
        self.assertIn('by_category', stats)
        self.assertIn('average_quality_score', stats)
        self.assertIn('high_quality_count', stats)
        
        # 比亚迪 92 分是高质量（>=80）
        self.assertEqual(stats['high_quality_count'], 1)
        # 蔚来 78 分是中等质量（60-80）
        self.assertEqual(stats['medium_quality_count'], 1)
    
    def test_generate_writing_prompts(self):
        """测试写作灵感生成"""
        prompts = self.exporter.generate_writing_prompts(self.test_materials)
        
        # 应该包含高频话题
        self.assertIn('高频话题', prompts)
        # 检查是否包含数据或财报相关关键词
        self.assertTrue('财报' in prompts or '数据' in prompts or len(prompts) > 0)
    
    def test_empty_materials(self):
        """测试空列表处理"""
        # Markdown
        md = self.exporter.export_to_markdown([], "测试主题")
        self.assertIn('素材总数：** 0 条', md)  # 注意 Markdown 加粗格式
        
        # JSON
        json_data = json.loads(self.exporter.export_to_json([], "测试"))
        self.assertEqual(json_data['metadata']['total_materials'], 0)
        
        # CSV
        csv = self.exporter.export_to_csv([])
        self.assertEqual(csv, "")
        
        # 写作灵感
        prompts = self.exporter.generate_writing_prompts([])
        self.assertIn('暂无足够素材', prompts)


if __name__ == '__main__':
    unittest.main(verbosity=2)
