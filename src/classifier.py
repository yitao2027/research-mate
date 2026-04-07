#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
素材分类器模块（优化版）

使用加权关键词匹配和规则引擎对素材进行智能分类
支持事实数据、典型案例、专家观点、竞品动态等类别

优化点：
1. 引入关键词权重机制（核心词权重 > 一般词）
2. 添加否定词检测，避免误判
3. 增加组合规则匹配
4. 支持置信度评估
"""

from typing import List, Dict, Tuple
import re


class MaterialClassifier:
    """素材分类器类"""
    
    def __init__(self):
        """初始化分类器"""
        
        # 定义各类别的关键词库（带权重）
        # 权重说明：3=核心词，2=重要词，1=一般词
        self.category_keywords = {
            '财务数据': {
                '营收': 3, '收入': 3, '利润': 3, '净利润': 3, '毛利率': 3, 
                '净利率': 3, '每股收益': 3, 'EPS': 3, '资产负债': 2, '现金流': 2, 
                'ROE': 3, 'ROA': 3, '同比增长': 2, '环比增长': 2, '财报': 3, 
                '季报': 2, '年报': 2, '净利': 2, '营利': 1
            },
            '市场数据': {
                '市场份额': 3, '市场规模': 3, '占有率': 3, '用户数': 3, 
                'DAU': 3, 'MAU': 3, '渗透率': 2, '增长率': 2, 'CAGR': 3, 
                '销量': 2, '交付量': 2, '订单量': 2, 'GMV': 3, '客单价': 2,
                '装机量': 2, '下载量': 2
            },
            '运营数据': {
                '留存率': 3, '复购率': 3, '转化率': 3, '获客成本': 3, 
                'LTV': 3, 'CAC': 3, '付费率': 2, '活跃度': 2, '使用时长': 2, 
                '日活': 2, '月活': 2
            },
            '融资数据': {
                '融资': 3, '投资': 2, '估值': 3, 'IPO': 3, '上市': 3, 
                '轮次': 2, '天使轮': 3, 'A 轮': 3, 'B 轮': 3, 'C 轮': 3, 
                'D 轮': 3, 'Pre-IPO': 3, '战略投资': 2, '并购': 2, '收购': 2, 
                '金额': 1, '亿美元': 2, '亿元': 1
            },
            '产品创新': {
                '发布': 2, '推出': 2, '上线': 2, '新品': 2, '新产品': 3, 
                '迭代': 2, '版本更新': 2, '功能升级': 2, '技术创新': 3, 
                '专利': 2, '研发': 2, '自研': 2, '首发': 3, '全球首款': 3, 
                '行业首创': 3
            },
            '企业战略': {
                '战略': 3, '布局': 2, '转型': 2, '调整': 1, '重组': 2, 
                '架构优化': 2, '业务聚焦': 3, '扩张': 1, '收缩': 1, 
                '出海': 2, '国际化': 2, '本土化': 2, '生态建设': 2, 
                '合作伙伴': 1
            },
            '高管言论': {
                '表示': 2, '指出': 2, '强调': 2, '认为': 2, '预测': 2, 
                '预计': 2, '透露': 2, '宣布': 2, '采访': 2, '访谈': 3, 
                '演讲': 2, '发言': 2, 'CEO': 3, '创始人': 3, '董事长': 3, 
                '总裁': 3, '副总裁': 2, 'CFO': 3, 'CTO': 3, '高管': 2, 
                '管理层': 2
            },
            '行业政策': {
                '政策': 3, '规定': 2, '办法': 2, '通知': 2, '指导意见': 3, 
                '监管': 2, '合规': 2, '审批': 2, '牌照': 2, '准入': 2, 
                '标准': 1, '规范': 1, '发改委': 3, '工信部': 3, '证监会': 3, 
                '国务院': 3
            },
            '竞争动态': {
                '竞争': 2, '对手': 2, '竞品': 3, '对标': 2, '超越': 2, 
                '领先': 1, '落后': 1, '差距': 1, '价格战': 3, '营销战': 2, 
                '人才争夺': 3, '挖角': 2, '挖人': 2, '跳槽': 1
            },
            '风险事件': {
                '风险': 2, '危机': 3, '诉讼': 3, '处罚': 3, '罚款': 3, 
                '调查': 2, '召回': 3, '投诉': 2, '负面': 2, '亏损': 2, 
                '下滑': 1, '下跌': 1, '裁员': 3, '倒闭': 3, '破产': 3, 
                '暴雷': 3
            }
        }
        
        # 否定词列表（用于降低误判）
        self.negation_words = [
            '未', '没有', '无', '非', '不', '否', '莫', '勿', '别', '休',
            '尚未', '并未', '并无', '不曾', '未能', '不可', '不会'
        ]
        
        # 数据类型标识词（带权重）
        self.data_indicators = {
            '%': 2, '％': 2, '亿元': 2, '万元': 1, '亿美元': 3, '百万': 1, 
            '千万': 1, '亿': 1, '万': 1, '倍': 1, '个百分点': 2, 'pct': 2, 
            'bps': 2, '同比': 2, '环比': 2, '增长': 1, '下降': 1, 
            '达到': 1, '突破': 1, '超过': 1, '低于': 1, '高于': 1, 
            '约': 0.5, '左右': 0.5, '近': 0.5, '超': 1
        }
        
        # 类别映射到素材大类
        self.type_mapping = {
            '财务数据': '事实数据',
            '市场数据': '事实数据',
            '运营数据': '事实数据',
            '融资数据': '事实数据',
            '产品创新': '典型案例',
            '企业战略': '典型案例',
            '高管言论': '专家观点',
            '行业政策': '专家观点',
            '竞争动态': '竞品动态',
            '风险事件': '竞品动态'
        }
    
    def classify(self, material: Dict) -> Dict:
        """
        对单个素材进行分类
        
        Args:
            material: 素材字典，包含 title, content 等字段
            
        Returns:
            添加分类信息的素材字典
        """
        text = f"{material.get('title', '')} {material.get('content', '')}"
        
        # 检测是否包含数据
        has_data = self._detect_data(text)
        
        # 检测是否有否定词（降低某些类别的置信度）
        has_negation = self._detect_negation(text)
        
        # 计算与各分类的加权匹配分数
        category_scores = {}
        for category, keywords in self.category_keywords.items():
            score, matched_keywords = self._calculate_weighted_score(text, keywords)
            
            # 如果有否定词，降低高管言论等主观类别的分数
            if has_negation and category in ['高管言论', '风险事件']:
                score *= 0.7
            
            if score > 0:
                category_scores[category] = {
                    'score': score,
                    'matched_keywords': matched_keywords
                }
        
        # 确定主分类和子分类
        if category_scores:
            sorted_categories = sorted(
                category_scores.items(), 
                key=lambda x: x[1]['score'], 
                reverse=True
            )
            primary_category = sorted_categories[0][0]
            primary_score = sorted_categories[0][1]['score']
            secondary_category = sorted_categories[1][0] if len(sorted_categories) > 1 else None
        else:
            primary_category = '其他'
            primary_score = 0
            secondary_category = None
        
        # 映射到更高层级的类型
        material_type = self._map_to_material_type(primary_category)
        
        # 计算置信度（归一化到 0-1）
        confidence = min(primary_score / 10.0, 1.0)  # 假设满分 10 分
        
        # 添加分类结果
        material['category'] = primary_category
        material['sub_category'] = secondary_category
        material['material_type'] = material_type
        material['has_data'] = has_data
        material['category_confidence'] = round(confidence, 2)
        material['matched_keywords'] = category_scores.get(primary_category, {}).get('matched_keywords', [])
        
        return material
    
    def classify_batch(self, materials: List[Dict]) -> List[Dict]:
        """
        批量分类素材
        
        Args:
            materials: 素材列表
            
        Returns:
            添加分类信息的素材列表
        """
        return [self.classify(m) for m in materials]
    
    def _detect_data(self, text: str) -> bool:
        """检测文本是否包含具体数据"""
        # 检查数据指示词
        total_weight = 0
        for indicator, weight in self.data_indicators.items():
            if indicator in text:
                total_weight += weight
        
        if total_weight >= 2:  # 权重和达到 2 才认为有数据
            return True
        
        # 检测数字模式（如 123.45, 1,234,567 等）
        number_pattern = r'\d+[,.]?\d*'
        numbers = re.findall(number_pattern, text)
        
        # 至少 2 个数字才认为有数据
        return len(numbers) >= 2
    
    def _detect_negation(self, text: str) -> bool:
        """检测文本中是否包含否定词"""
        for negation in self.negation_words:
            if negation in text:
                return True
        return False
    
    def _calculate_weighted_score(self, text: str, keywords: Dict[str, int]) -> Tuple[float, List[str]]:
        """
        计算文本与关键词列表的加权匹配分数
        
        Args:
            text: 待分析文本
            keywords: 关键词字典（词->权重）
            
        Returns:
            (分数，匹配的关键词列表)
        """
        if not keywords:
            return 0.0, []
        
        matched_keywords = []
        total_score = 0.0
        
        text_lower = text.lower()
        
        for keyword, weight in keywords.items():
            if keyword.lower() in text_lower:
                matched_keywords.append(keyword)
                total_score += weight
        
        # 基础分：匹配词的权重和
        base_score = total_score
        
        #  bonus：如果匹配到 3 个以上关键词，给予额外加分
        if len(matched_keywords) >= 5:
            base_score *= 1.5
        elif len(matched_keywords) >= 3:
            base_score *= 1.3
        elif len(matched_keywords) >= 2:
            base_score *= 1.1
        
        return base_score, matched_keywords
    
    def _map_to_material_type(self, category: str) -> str:
        """
        将细分类别映射到素材大类
        
        Args:
            category: 细分类别
            
        Returns:
            素材大类
        """
        return self.type_mapping.get(category, '其他')
    
    def get_statistics(self, materials: List[Dict]) -> Dict:
        """
        统计分类结果
        
        Args:
            materials: 已分类的素材列表
            
        Returns:
            统计字典
        """
        stats = {
            'total': len(materials),
            'by_type': {},
            'by_category': {},
            'with_data': 0,
            'high_confidence': 0,  # 置信度>0.8 的数量
            'avg_confidence': 0
        }
        
        total_confidence = 0
        
        for m in materials:
            # 按类型统计
            mtype = m.get('material_type', '未分类')
            stats['by_type'][mtype] = stats['by_type'].get(mtype, 0) + 1
            
            # 按类别统计
            cat = m.get('category', '未分类')
            stats['by_category'][cat] = stats['by_category'].get(cat, 0) + 1
            
            # 含数据的素材数量
            if m.get('has_data', False):
                stats['with_data'] += 1
            
            # 高置信度统计
            confidence = m.get('category_confidence', 0)
            if confidence > 0.8:
                stats['high_confidence'] += 1
            total_confidence += confidence
        
        # 计算平均置信度
        if materials:
            stats['avg_confidence'] = round(total_confidence / len(materials), 2)
        
        return stats


if __name__ == '__main__':
    # 测试代码
    classifier = MaterialClassifier()
    
    test_material = {
        'title': '比亚迪 Q4 财报：营收增长 42%，净利润翻倍',
        'content': '比亚迪发布 2025 年第四季度财报，实现营业收入 2,150 亿元，同比增长 42%；净利润 185 亿元，同比增长 68%。毛利率提升至 22.5%。',
        'source': '财经日报'
    }
    
    result = classifier.classify(test_material)
    print(f"原始标题：{result['title']}")
    print(f"主分类：{result['category']}")
    print(f"素材类型：{result['material_type']}")
    print(f"包含数据：{result['has_data']}")
    print(f"置信度：{result['category_confidence']}")
    print(f"匹配关键词：{result['matched_keywords']}")
