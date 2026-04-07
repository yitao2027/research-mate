#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
素材采集器模块（重构版）

负责从多个信息源采集原始素材
支持行业报告、科技媒体、社交媒体等多渠道
集成真实爬虫逻辑和降级策略
"""

import sys
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.dirname(__file__))

from sources.base_source import BaseSource, RequestError, ParseError
from sources.tech_media_source import TechMediaSource, create_tech_media_source
from sources.industry_reports_source import IndustryReportsSource


class MaterialCollector:
    """素材采集器类"""
    
    def __init__(self, config: dict = None):
        """
        初始化采集器
        
        Args:
            config: 配置字典，包含各信息源的开关和参数
        """
        self.config = config or {}
        self.sources_config = self.config.get('sources', {})
        self.crawler_config = self.config.get('crawler', {})
        
        # 初始化采集源列表
        self.sources: List[BaseSource] = []
        self._init_sources()
    
    def _init_sources(self):
        """初始化所有启用的采集源"""
        # 1. 科技媒体采集源
        if self.sources_config.get('tech_media', {}).get('enabled', True):
            tech_sources = self.sources_config['tech_media'].get('sources', [
                {'name': '36kr', 'url': 'https://36kr.com'},
                {'name': 'huxiu', 'url': 'https://www.huxiu.com'},
                {'name': 'tmtpost', 'url': 'https://www.tmtpost.com'}
            ])
            
            for source_cfg in tech_sources:
                source_cfg.update(self.crawler_config)
                try:
                    source = create_tech_media_source(source_cfg['name'], source_cfg)
                    self.sources.append(source)
                except Exception as e:
                    print(f"   ⚠ 初始化{source_cfg['name']}失败：{e}")
        
        # 2. 行业报告采集源
        if self.sources_config.get('industry_reports', {}).get('enabled', True):
            try:
                report_source = IndustryReportsSource({
                    'name': 'industry_reports',
                    'url': '',
                    **self.crawler_config
                })
                self.sources.append(report_source)
            except Exception as e:
                print(f"   ⚠ 初始化行业报告源失败：{e}")
        
        # 3. 社交媒体采集源（简化版本，后续可扩展）
        if self.sources_config.get('social_media', {}).get('enabled', True):
            # TODO: 实现知乎、雪球等社交媒体采集源
            print("   ℹ️  社交媒体采集源待实现")
    
    def collect(self, topic: str, days_back: int = 7) -> List[Dict]:
        """
        执行素材采集
        
        Args:
            topic: 采集主题关键词
            days_back: 采集过去 N 天的内容
            
        Returns:
            原始素材列表，每个素材是一个字典
        """
        print(f"\n📥 开始采集主题：【{topic}】")
        print(f"📅 时间范围：过去 {days_back} 天")
        print(f"🔧 启用采集源数量：{len(self.sources)}")
        print("-" * 60)
        
        all_materials = []
        
        # 遍历所有采集源
        for source in self.sources:
            try:
                materials = source.fetch(topic, days_back)
                all_materials.extend(materials)
                print(f"   ✓ {source.name}: 采集到 {len(materials)} 条")
            except Exception as e:
                print(f"   ⚠ {source.name}: 采集失败 - {str(e)}")
                # 继续处理其他源
        
        print("-" * 60)
        print(f"✅ 总计采集：{len(all_materials)} 条素材\n")
        
        return all_materials
    
    def fetch_url(self, url: str) -> Optional[str]:
        """
        抓取指定 URL 的页面内容（通用方法）
        
        Args:
            url: 目标网址
            
        Returns:
            页面 HTML 内容，失败时返回 None
        """
        try:
            import requests
            headers = {
                'User-Agent': self.crawler_config.get(
                    'user_agent',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
                )
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"   抓取失败 {url}: {str(e)}")
            return None
    
    def get_available_sources(self) -> List[Dict]:
        """获取所有可用采集源信息"""
        return [source.get_source_info() for source in self.sources]


if __name__ == '__main__':
    # 测试代码
    collector = MaterialCollector()
    materials = collector.collect("新能源汽车", days_back=7)
    print(f"\n共采集到 {len(materials)} 条素材")
    for i, m in enumerate(materials[:5], 1):
        print(f"{i}. {m['title']} [{m['source']}]")
