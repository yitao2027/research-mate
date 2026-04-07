#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
素材采集器模块

负责从多个信息源采集原始素材
支持行业报告、科技媒体、公司公告、社交媒体等渠道
"""

import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import re


class MaterialCollector:
    """素材采集器类"""
    
    def __init__(self, config: dict = None):
        """
        初始化采集器
        
        Args:
            config: 配置字典，包含各信息源的开关和参数
        """
        self.config = config or {}
        self.sources_enabled = self.config.get('sources', {})
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        # 注册可用的采集源
        self.available_sources = []
        if self.sources_enabled.get('industry_reports', True):
            self.available_sources.append('industry_reports')
        if self.sources_enabled.get('tech_media', True):
            self.available_sources.append('tech_media')
        if self.sources_enabled.get('social_media', True):
            self.available_sources.append('social_media')
    
    def collect(self, topic: str, days_back: int = 7) -> List[Dict]:
        """
        执行素材采集
        
        Args:
            topic: 采集主题关键词
            days_back: 采集过去 N 天的内容
            
        Returns:
            原始素材列表，每个素材是一个字典
        """
        print(f"   启用采集源：{', '.join(self.available_sources)}")
        
        all_materials = []
        
        # 遍历所有启用的采集源
        for source_name in self.available_sources:
            try:
                materials = self._fetch_from_source(source_name, topic, days_back)
                all_materials.extend(materials)
                print(f"   ✓ {source_name}: 采集到 {len(materials)} 条")
            except Exception as e:
                print(f"   ⚠ {source_name}: 采集失败 - {str(e)}")
        
        return all_materials
    
    def _fetch_from_source(self, source_name: str, topic: str, days_back: int) -> List[Dict]:
        """
        从指定源采集素材
        
        Args:
            source_name: 采集源名称
            topic: 主题关键词
            days_back: 时间范围
            
        Returns:
            素材列表
        """
        # 这里是框架代码，实际项目中需要实现具体的采集逻辑
        # 示例返回一些模拟数据用于测试
        
        mock_data = self._generate_mock_materials(source_name, topic, days_back)
        return mock_data
    
    def _generate_mock_materials(self, source_name: str, topic: str, days_back: int) -> List[Dict]:
        """
        生成模拟素材数据（用于演示和测试）
        
        在实际部署时，这里应该替换为真实的网络爬虫逻辑
        """
        from datetime import datetime, timedelta
        
        materials = []
        
        # 根据主题生成相关的模拟素材
        if "新能源" in topic or "汽车" in topic:
            materials = [
                {
                    'title': f'比亚迪 2025 年 Q4 交付量突破 50 万辆，同比增长 68%',
                    'content': '比亚迪发布 2025 年第四季度财报显示，公司单季交付量达到 50.3 万辆，同比增长 68%，环比增长 22%。全年累计交付 185 万辆新能源汽车，继续保持全球新能源车销量冠军地位。营收方面，Q4 实现营业收入 2,150 亿元，同比增长 42%；净利润 185 亿元，同比增长 68%。毛利率提升至 22.5%，较上年同期增加 3.2 个百分点。',
                    'source_type': source_name,
                    'url': 'https://example.com/byd-q4-2025-delivery',
                    'publish_date': (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'),
                    'author': '财经日报',
                    'keywords': ['比亚迪', '新能源车', '交付量', '财报', '增长率']
                },
                {
                    'title': '宁德时代发布新一代神行电池，能量密度提升 30%',
                    'content': '宁德时代在福建宁德总部正式发布第四代神行超充电池。新电池采用磷酸锰铁锂正极材料，能量密度达到 255Wh/kg，较上一代产品提升 30%。支持 5C 超快充，10 分钟可充电至 80%。预计 2026 年 Q2 开始量产装车，首发客户包括理想汽车、蔚来汽车等。',
                    'source_type': source_name,
                    'url': 'https://example.com/catl-new-battery-tech',
                    'publish_date': (datetime.now() - timedelta(days=4)).strftime('%Y-%m-%d'),
                    'author': '36 氪',
                    'keywords': ['宁德时代', '电池技术', '能量密度', '快充', '磷酸锰铁锂']
                },
                {
                    'title': '特斯拉上海工厂 2025 年出口量达 45 万辆，占全球产能 60%',
                    'content': '据上海海关数据统计，特斯拉上海超级工厂 2025 年全年出口整车 45.2 万辆，主要销往欧洲、亚太和北美市场。目前上海工厂承担特斯拉全球 60% 的产能， Model Y 和 Model 3 是出口主力车型。工厂单日最高产量突破 2,800 辆，生产节拍达到 45 秒/辆。',
                    'source_type': source_name,
                    'url': 'https://example.com/tesla-shanghai-export-2025',
                    'publish_date': (datetime.now() - timedelta(days=6)).strftime('%Y-%m-%d'),
                    'author': '界面新闻',
                    'keywords': ['特斯拉', '上海工厂', '出口量', '产能', 'Model Y']
                }
            ]
        
        elif "人工智能" in topic or "AI" in topic.upper():
            materials = [
                {
                    'title': 'OpenAI 发布 GPT-5，推理能力提升 10 倍',
                    'content': 'OpenAI 在旧金山举办发布会，正式推出第五代大语言模型 GPT-5。新模型在数学推理、代码生成、多模态理解等基准测试中表现优异，GSM8K 数学推理得分 98.5%，HumanEval 代码生成通过率 92.3%。GPT-5 采用混合专家架构（MoE），参数量未公开但推理效率提升 5 倍。',
                    'source_type': source_name,
                    'url': 'https://example.com/openai-gpt5-release',
                    'publish_date': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
                    'author': '机器之心',
                    'keywords': ['OpenAI', 'GPT-5', '大模型', '推理能力', 'MoE 架构']
                },
                {
                    'title': '百度文心一言 4.5 通过国家生成式 AI 备案',
                    'content': '百度宣布文心一言 4.5 版本正式通过国家互联网信息办公室生成式人工智能服务备案。新版本在中文理解、知识问答、长文本处理等方面显著优化，支持 128K 上下文窗口。百度智能云已接入文心一言 4.5，为企业客户提供定制化大模型服务。',
                    'source_type': source_name,
                    'url': 'https://example.com/baidu-ernie-45-filing',
                    'publish_date': (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d'),
                    'author': '钛媒体',
                    'keywords': ['百度', '文心一言', 'AI 备案', '大模型', '智能云']
                }
            ]
        
        else:
            # 通用模板素材
            materials = [
                {
                    'title': f'{topic} 行业最新动态分析',
                    'content': f'近期{topic}领域出现多个重要变化。从市场规模来看，2025 年整体规模达到 3,500 亿元，同比增长 28%。头部企业市场份额集中度进一步提升，CR5 达到 65%。技术创新方面，多项关键技术取得突破，推动行业进入新发展阶段。',
                    'source_type': source_name,
                    'url': 'https://example.com/industry-analysis-generic',
                    'publish_date': (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d'),
                    'author': '行业研究院',
                    'keywords': [topic, '行业动态', '市场规模', '竞争格局']
                }
            ]
        
        # 为每个素材添加唯一 ID 和采集时间
        for i, m in enumerate(materials, 1):
            m['id'] = f"{source_name}_{i}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            m['collected_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return materials
    
    def fetch_url(self, url: str) -> Optional[str]:
        """
        抓取指定 URL 的页面内容
        
        Args:
            url: 目标网址
            
        Returns:
            页面 HTML 内容，失败时返回 None
        """
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"   抓取失败 {url}: {str(e)}")
            return None


if __name__ == '__main__':
    # 测试代码
    collector = MaterialCollector()
    materials = collector.collect("新能源汽车", days_back=7)
    print(f"\n共采集到 {len(materials)} 条素材")
    for m in materials[:3]:
        print(f"- {m['title']}")
