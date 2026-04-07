#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
素材质量评估器模块

从来源可信度、时效性、数据完整性、交叉验证等维度评估素材质量
输出综合评分和推荐理由
"""

from datetime import datetime, timedelta
from typing import List, Dict
import re


class QualityEvaluator:
    """素材质量评估器类"""
    
    def __init__(self, config: dict = None):
        """
        初始化评估器
        
        Args:
            config: 配置字典，包含各维度权重和阈值
        """
        self.config = config or {}
        
        # 默认权重配置
        self.weights = self.config.get('weights', {
            'credibility': 0.40,      # 来源可信度权重 40%
            'timeliness': 0.25,       # 时效性权重 25%
            'completeness': 0.20,     # 数据完整性权重 20%
            'verification': 0.15      # 交叉验证权重 15%
        })
        
        # 权威来源白名单（评分基准）
        self.authoritative_sources = {
            '官方披露': ['巨潮资讯网', '上交所', '深交所', '港交所', 'SEC', '公司官网'],
            '主流财经媒体': ['财新', '财经', '第一财经', '界面新闻', '澎湃新闻', '21 世纪经济报道'],
            '科技媒体': ['36 氪', '虎嗅', '晚点 LatePost', '钛媒体', '机器之心', '量子位'],
            '券商研报': ['中信证券', '中金公司', '国泰君安', '海通证券', '招商证券', '华泰证券'],
            '咨询公司': ['麦肯锡', 'BCG', '贝恩', '德勤', '普华永道', '安永', '毕马威'],
            '研究机构': ['艾瑞咨询', '易观分析', '亿欧智库', 'IDC', 'Gartner', 'Forrester']
        }
    
    def evaluate(self, material: Dict) -> Dict:
        """
        评估单个素材的质量
        
        Args:
            material: 素材字典
            
        Returns:
            添加评分信息的素材字典
        """
        # 各维度评分
        credibility_score = self._evaluate_credibility(material)
        timeliness_score = self._evaluate_timeliness(material)
        completeness_score = self._evaluate_completeness(material)
        verification_score = self._evaluate_verification(material)
        
        # 计算加权综合分
        total_score = (
            credibility_score * self.weights['credibility'] +
            timeliness_score * self.weights['timeliness'] +
            completeness_score * self.weights['completeness'] +
            verification_score * self.weights['verification']
        )
        
        # 生成评价等级
        rating = self._get_rating(total_score)
        
        # 生成推荐理由
        reasons = self._generate_reasons(
            credibility_score, timeliness_score, 
            completeness_score, verification_score
        )
        
        # 添加评估结果
        material['score'] = round(total_score, 2)
        material['score_breakdown'] = {
            'credibility': round(credibility_score, 2),
            'timeliness': round(timeliness_score, 2),
            'completeness': round(completeness_score, 2),
            'verification': round(verification_score, 2)
        }
        material['rating'] = rating
        material['recommendation_reasons'] = reasons
        
        return material
    
    def evaluate_batch(self, materials: List[Dict]) -> List[Dict]:
        """
        批量评估素材
        
        Args:
            materials: 素材列表
            
        Returns:
            添加评分信息的素材列表
        """
        return [self.evaluate(m) for m in materials]
    
    def _evaluate_credibility(self, material: Dict) -> float:
        """
        评估来源可信度
        
        Args:
            material: 素材字典
            
        Returns:
            可信度分数 (0-1)
        """
        source = material.get('author', '') or material.get('source', '')
        url = material.get('url', '')
        
        # 检查是否在权威来源列表中
        for category, sources in self.authoritative_sources.items():
            for auth_source in sources:
                if auth_source in source or auth_source in url:
                    # 根据来源类型给予不同基础分
                    if category in ['官方披露', '券商研报']:
                        return 0.95
                    elif category in ['主流财经媒体', '咨询公司']:
                        return 0.88
                    elif category in ['科技媒体', '研究机构']:
                        return 0.82
        
        # 检查域名后缀（政府、教育机构）
        if '.gov.cn' in url or '.edu.cn' in url:
            return 0.90
        
        # 检查是否为企业官方渠道
        if 'official' in url.lower() or 'investor' in url.lower():
            return 0.85
        
        # 默认分数
        return 0.65
    
    def _evaluate_timeliness(self, material: Dict) -> float:
        """
        评估时效性
        
        Args:
            material: 素材字典
            
        Returns:
            时效性分数 (0-1)
        """
        publish_date_str = material.get('publish_date', '')
        
        if not publish_date_str:
            return 0.50  # 无发布日期时给中等分数
        
        try:
            # 解析发布日期
            publish_date = datetime.strptime(publish_date_str, '%Y-%m-%d')
            days_old = (datetime.now() - publish_date).days
            
            if days_old < 0:
                return 0.50  # 日期异常
            
            # 时间衰减函数：7 天内 1.0，30 天内线性衰减到 0.5，超过 30 天快速衰减
            if days_old <= 7:
                return 1.0
            elif days_old <= 30:
                return 1.0 - (days_old - 7) / 23 * 0.5
            elif days_old <= 90:
                return 0.5 - (days_old - 30) / 60 * 0.3
            else:
                return max(0.1, 0.2 - (days_old - 90) / 365 * 0.1)
        
        except Exception:
            return 0.50
    
    def _evaluate_completeness(self, material: Dict) -> float:
        """
        评估数据完整性
        
        Args:
            material: 素材字典
            
        Returns:
            完整性分数 (0-1)
        """
        content = material.get('content', '')
        title = material.get('title', '')
        text = f"{title} {content}"
        
        score = 0.50  # 基础分
        
        # 检测是否包含具体数字
        number_pattern = r'\d+[,.]?\d*'
        numbers = re.findall(number_pattern, text)
        
        if len(numbers) >= 5:
            score += 0.30
        elif len(numbers) >= 3:
            score += 0.20
        elif len(numbers) >= 1:
            score += 0.10
        
        # 检测是否包含对比数据（同比、环比、vs 等）
        comparison_keywords = ['同比', '环比', '增长', '下降', '较', 'vs', '相比', '对比']
        has_comparison = any(kw in text for kw in comparison_keywords)
        if has_comparison:
            score += 0.15
        
        # 检测是否包含时间范围
        time_keywords = ['2025 年', '2026 年', 'Q4', 'Q3', '季度', '年度', '全年', '上半年', '下半年']
        has_timeframe = any(kw in text for kw in time_keywords)
        if has_timeframe:
            score += 0.05
        
        # 检测内容长度（过短可能信息量不足）
        if len(content) < 50:
            score -= 0.20
        elif len(content) < 100:
            score -= 0.10
        elif len(content) > 500:
            score += 0.10
        
        return min(max(score, 0), 1.0)
    
    def _evaluate_verification(self, material: Dict) -> float:
        """
        评估交叉验证程度
        
        Args:
            material: 素材字典
            
        Returns:
            交叉验证分数 (0-1)
            
        Note: 简化版本，实际项目中应该查询其他来源验证同一事件
        """
        # 这里可以扩展为：搜索相同事件在其他媒体的报道数量
        # 当前简化处理：如果素材来自权威来源且包含具体数据，给予较高分数
        
        credibility = self._evaluate_credibility(material)
        has_data = material.get('has_data', False)
        
        if credibility > 0.85 and has_data:
            return 0.85
        elif credibility > 0.70 and has_data:
            return 0.70
        elif has_data:
            return 0.60
        else:
            return 0.50
    
    def _get_rating(self, score: float) -> str:
        """
        根据分数获取评级
        
        Args:
            score: 综合分数
            
        Returns:
            评级字符串
        """
        if score >= 0.85:
            return 'S'  # 强烈推荐
        elif score >= 0.75:
            return 'A'  # 推荐
        elif score >= 0.65:
            return 'B'  # 可用
        elif score >= 0.50:
            return 'C'  # 谨慎使用
        else:
            return 'D'  # 不推荐
    
    def _generate_reasons(self, cred: float, time: float, comp: float, veri: float) -> List[str]:
        """
        生成推荐理由
        
        Args:
            cred: 可信度分数
            time: 时效性分数
            comp: 完整性分数
            veri: 交叉验证分数
            
        Returns:
            理由列表
        """
        reasons = []
        
        if cred >= 0.85:
            reasons.append("来源权威性高")
        elif cred >= 0.70:
            reasons.append("来源较为可靠")
        
        if time >= 0.9:
            reasons.append("信息时效性强（7 天内）")
        elif time >= 0.7:
            reasons.append("信息较新（30 天内）")
        
        if comp >= 0.8:
            reasons.append("数据详实完整")
        elif comp >= 0.6:
            reasons.append("包含关键数据")
        
        if veri >= 0.8:
            reasons.append("可交叉验证")
        
        return reasons


if __name__ == '__main__':
    # 测试代码
    evaluator = QualityEvaluator()
    
    test_material = {
        'title': '比亚迪 Q4 财报：营收 2,150 亿元，同比增长 42%',
        'content': '比亚迪发布 2025 年第四季度财报，实现营业收入 2,150 亿元，同比增长 42%；净利润 185 亿元，同比增长 68%。毛利率提升至 22.5%，较上年同期增加 3.2 个百分点。',
        'author': '巨潮资讯网',
        'url': 'https://example.com/byd-report',
        'publish_date': '2026-03-31',
        'has_data': True
    }
    
    result = evaluator.evaluate(test_material)
    print(f"综合评分：{result['score']}")
    print(f"评级：{result['rating']}")
    print(f"评分明细：{result['score_breakdown']}")
    print(f"推荐理由：{result['recommendation_reasons']}")
