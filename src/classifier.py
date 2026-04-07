#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
素材分类器模块

使用规则匹配和关键词分析对素材进行智能分类
支持事实数据、典型案例、专家观点、竞品动态等类别
"""

from typing import List, Dict
import re


class MaterialClassifier:
    """素材分类器类"""
    
    def __init__(self):
        """初始化分类器"""
        
        # 定义各类别的关键词库
        self.category_keywords = {
            '财务数据': [
                '营收', '收入', '利润', '净利润', '毛利率', '净利率', '每股收益', 'EPS',
                '资产负债', '现金流', 'ROE', 'ROA', '同比增长', '环比增长', '财报', '季报', '年报'
            ],
            '市场数据': [
                '市场份额', '市场规模', '占有率', '用户数', 'DAU', 'MAU', '渗透率',
                '增长率', 'CAGR', '销量', '交付量', '订单量', 'GMV', '客单价'
            ],
            '运营数据': [
                '留存率', '复购率', '转化率', '获客成本', 'LTV', 'CAC', '付费率',
                '活跃度', '使用时长', '日活', '月活', '装机量', '下载量'
            ],
            '融资数据': [
                '融资', '投资', '估值', 'IPO', '上市', '轮次', '天使轮', 'A 轮', 'B 轮',
                'C 轮', 'D 轮', 'Pre-IPO', '战略投资', '并购', '收购', '金额', '亿美元', '亿元'
            ],
            '产品创新': [
                '发布', '推出', '上线', '新品', '新产品', '迭代', '版本更新', '功能升级',
                '技术创新', '专利', '研发', '自研', '首发', '全球首款', '行业首创'
            ],
            '企业战略': [
                '战略', '布局', '转型', '调整', '重组', '架构优化', '业务聚焦',
                '扩张', '收缩', '出海', '国际化', '本土化', '生态建设', '合作伙伴'
            ],
            '高管言论': [
                '表示', '指出', '强调', '认为', '预测', '预计', '透露', '宣布',
                '采访', '访谈', '演讲', '发言', 'CEO', '创始人', '董事长', '总裁',
                '副总裁', 'CFO', 'CTO', '高管', '管理层'
            ],
            '行业政策': [
                '政策', '规定', '办法', '通知', '指导意见', '监管', '合规', '审批',
                '牌照', '准入', '标准', '规范', '发改委', '工信部', '证监会', '国务院'
            ],
            '竞争动态': [
                '竞争', '对手', '竞品', '对标', '超越', '领先', '落后', '差距',
                '价格战', '营销战', '人才争夺', '挖角', '挖人', '跳槽'
            ],
            '风险事件': [
                '风险', '危机', '诉讼', '处罚', '罚款', '调查', '召回', '投诉',
                '负面', '亏损', '下滑', '下跌', '裁员', '倒闭', '破产', '暴雷'
            ]
        }
        
        # 定义数据类型标识词
        self.data_indicators = [
            '%', '％', '亿元', '万元', '亿美元', '百万', '千万', '亿', '万',
            '倍', '倍', '个百分点', 'pct', 'bps', '同比', '环比', '增长', '下降',
            '达到', '突破', '超过', '低于', '高于', '约', '左右', '近', '超'
        ]
    
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
        
        # 计算与各分类的匹配度
        category_scores = {}
        for category, keywords in self.category_keywords.items():
            score = self._calculate_match_score(text, keywords)
            if score > 0:
                category_scores[category] = score
        
        # 确定主分类和子分类
        if category_scores:
            sorted_categories = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)
            primary_category = sorted_categories[0][0]
            secondary_category = sorted_categories[1][0] if len(sorted_categories) > 1 else None
        else:
            primary_category = '其他'
            secondary_category = None
        
        # 映射到更高层级的类型
        material_type = self._map_to_material_type(primary_category)
        
        # 添加分类结果
        material['category'] = primary_category
        material['sub_category'] = secondary_category
        material['material_type'] = material_type
        material['has_data'] = has_data
        material['category_confidence'] = category_scores.get(primary_category, 0)
        
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
        for indicator in self.data_indicators:
            if indicator in text:
                return True
        
        # 检测数字模式（如 123.45, 1,234,567 等）
        number_pattern = r'\d+[,.]?\d*'
        if re.search(number_pattern, text):
            return True
        
        return False
    
    def _calculate_match_score(self, text: str, keywords: List[str]) -> float:
        """
        计算文本与关键词列表的匹配分数
        
        Args:
            text: 待分析文本
            keywords: 关键词列表
            
        Returns:
            匹配分数 (0-1)
        """
        if not keywords:
            return 0.0
        
        matches = 0
        for keyword in keywords:
            if keyword.lower() in text.lower():
                matches += 1
        
        # 归一化到 0-1 范围
        score = matches / len(keywords)
        
        # 加权：如果匹配到 3 个以上关键词，给予额外加分
        if matches >= 3:
            score *= 1.5
        elif matches >= 2:
            score *= 1.2
        
        return min(score, 1.0)  # 上限为 1.0
    
    def _map_to_material_type(self, category: str) -> str:
        """
        将细分类别映射到素材大类
        
        Args:
            category: 细分类别
            
        Returns:
            素材大类
        """
        type_mapping = {
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
        
        return type_mapping.get(category, '其他')
    
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
            'with_data': 0
        }
        
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
