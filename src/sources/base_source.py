#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
采集源基类模块

定义所有采集源的统一接口和通用功能
提供 HTTP 请求、HTML 解析、错误处理等基础能力
"""

import requests
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import time
import re


class SourceError(Exception):
    """采集源错误的基类异常"""
    pass


class RequestError(SourceError):
    """HTTP 请求异常"""
    pass


class ParseError(SourceError):
    """页面解析异常"""
    pass


class VerificationError(SourceError):
    """数据验证失败（反幻觉机制）"""
    pass


class BaseSource(ABC):
    """采集源基类"""
    
    def __init__(self, config: dict = None):
        """
        初始化采集源
        
        Args:
            config: 配置字典，包含 URL、超时时间等参数
        """
        self.config = config or {}
        self.base_url = self.config.get('url', '')
        self.name = self.config.get('name', 'unknown')
        self.categories = self.config.get('categories', [])
        
        # HTTP 会话配置
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.config.get(
                'user_agent',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            ),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive'
        })
        
        # 爬虫配置
        self.timeout = self.config.get('timeout', 10)
        self.max_retries = self.config.get('max_retries', 3)
        self.retry_delay = self.config.get('retry_delay', 2)
        self.rate_limit = self.config.get('rate_limit', 1)  # 每秒请求数
        self.last_request_time = 0
    
    def _request(self, url: str, params: dict = None) -> str:
        """
        发送 HTTP GET 请求，带重试机制
        
        Args:
            url: 目标 URL
            params: 查询参数
            
        Returns:
            响应文本内容
            
        Raises:
            RequestError: 请求失败时抛出
        """
        # 频率限制控制
        elapsed = time.time() - self.last_request_time
        if elapsed < 1.0 / self.rate_limit:
            time.sleep(1.0 / self.rate_limit - elapsed)
        
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(
                    url,
                    params=params,
                    timeout=self.timeout
                )
                response.raise_for_status()
                self.last_request_time = time.time()
                return response.text
            
            except requests.exceptions.Timeout:
                if attempt == self.max_retries - 1:
                    raise RequestError(f"请求超时：{url}")
                time.sleep(self.retry_delay * (attempt + 1))
            
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    raise RequestError(f"页面不存在：{url}")
                elif e.response.status_code in [403, 429]:
                    raise RequestError(f"访问被拒绝 ({e.response.status_code})：{url}")
                if attempt == self.max_retries - 1:
                    raise RequestError(f"HTTP 错误 {e.response.status_code}: {url}")
                time.sleep(self.retry_delay * (attempt + 1))
            
            except requests.exceptions.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise RequestError(f"网络错误：{str(e)}")
                time.sleep(self.retry_delay * (attempt + 1))
        
        raise RequestError(f"请求失败：{url}")
    
    def _parse_html(self, html: str) -> BeautifulSoup:
        """
        解析 HTML 内容
        
        Args:
            html: HTML 字符串
            
        Returns:
            BeautifulSoup 对象
        """
        return BeautifulSoup(html, 'lxml')
    
    def _extract_text(self, element, default: str = '') -> str:
        """安全提取元素文本"""
        if element:
            return element.get_text(strip=True)
        return default
    
    def _extract_attr(self, element, attr: str, default: str = '') -> str:
        """安全提取元素属性"""
        if element and element.has_attr(attr):
            return element[attr]
        return default
    
    def _extract_publish_date(self, text: str) -> Optional[str]:
        """
        从文本中提取发布日期
        
        Args:
            text: 可能包含日期的文本
            
        Returns:
            格式化为 YYYY-MM-DD 的日期字符串，失败返回 None
        """
        # 匹配常见日期格式
        patterns = [
            r'(\d{4})-(\d{1,2})-(\d{1,2})',  # 2024-01-15
            r'(\d{4})年 (\d{1,2}) 月 (\d{1,2}) 日',  # 2024 年 1 月 15 日
            r'(\d{4})/(\d{1,2})/(\d{1,2})',  # 2024/01/15
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                year, month, day = map(int, match.groups())
                try:
                    date_obj = datetime(year, month, day)
                    # 检查日期是否合理（不超过今天）
                    if date_obj <= datetime.now():
                        return date_obj.strftime('%Y-%m-%d')
                except ValueError:
                    continue
        
        return None
    
    @abstractmethod
    def fetch(self, topic: str, days_back: int = 7) -> List[Dict]:
        """
        采集素材（抽象方法，子类必须实现）
        
        Args:
            topic: 采集主题关键词
            days_back: 采集过去 N 天的内容
            
        Returns:
            素材列表，每个素材是一个字典
        """
        pass
    
    def get_source_info(self) -> Dict:
        """获取采集源信息"""
        return {
            'name': self.name,
            'base_url': self.base_url,
            'categories': self.categories,
            'enabled': True
        }
    
    def _verify_data_point(self, data_text: str, source_url: str = None) -> Dict:
        """
        验证数据点的真实性（反幻觉机制）
        
        Args:
            data_text: 包含数据的文本
            source_url: 数据来源 URL
            
        Returns:
            验证结果字典
            
        Raises:
            VerificationError: 发现疑似幻觉数据时抛出
        """
        if not data_text or not data_text.strip():
            return {'valid': False, 'reason': '数据为空'}
        
        # 检查是否包含具体数值
        has_numbers = bool(re.search(r'\d+[,.]?\d*', data_text))
        
        # 检查是否有明确的主体（公司名、产品名等）
        has_subject = bool(re.search(r'[\u4e00-\u9fa5]{2,}|[A-Za-z]{2,}', data_text))
        
        # 检查是否有时间标识
        has_time = bool(re.search(r'\d{4}[-年]\d{1,2}[-月]\d{1,2}|近日 | 近期 | 上月|今年', data_text))
        
        # 检查是否有来源标识
        has_source = bool(source_url) or bool(re.search(r'据 | 显示 | 披露 | 报告|财报|数据显示', data_text))
        
        # 综合判断
        confidence_score = sum([has_numbers, has_subject, has_time, has_source]) / 4
        
        if confidence_score < 0.5:
            return {
                'valid': False,
                'reason': f'数据可信度低 (置信度：{confidence_score:.2f})',
                'confidence': confidence_score
            }
        
        return {
            'valid': True,
            'confidence': confidence_score,
            'features': {
                'has_numbers': has_numbers,
                'has_subject': has_subject,
                'has_time': has_time,
                'has_source': has_source
            }
        }
    
    def _extract_with_verification(self, html: BeautifulSoup, selector: dict, 
                                   source_url: str = None) -> Optional[str]:
        """
        提取数据并验证（防止幻觉）
        
        Args:
            html: BeautifulSoup 对象
            selector: 选择器配置
            source_url: 来源 URL
            
        Returns:
            验证通过的数据，None 表示验证失败
        """
        try:
            # 定位元素
            if 'tag' in selector:
                elements = html.find_all(selector['tag'], 
                                        class_=selector.get('class'),
                                        id=selector.get('id'))
            else:
                elements = html.select(selector['css'])
            
            if not elements:
                return None
            
            # 提取文本
            text = elements[0].get_text(strip=True)
            
            if not text:
                return None
            
            # 验证数据
            if selector.get('require_verification', False):
                verification = self._verify_data_point(text, source_url)
                if not verification['valid']:
                    print(f"   ⚠️  数据验证未通过：{verification['reason']}")
                    return None
            
            return text
            
        except Exception as e:
            print(f"   ⚠️  提取失败：{str(e)}")
            return None
