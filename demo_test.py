#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ResearchMate 功能演示脚本

测试完整的素材采集、分类、评估和导出流程
"""

import sys
from pathlib import Path
from datetime import datetime

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from collector import MaterialCollector
from classifier import MaterialClassifier
from evaluator import QualityEvaluator
from exporter import MaterialExporter


def test_full_pipeline():
    """测试完整采集流程"""
    
    print("=" * 60)
    print("🚀 ResearchMate 功能演示")
    print("=" * 60)
    print()
    
    # 1. 初始化各模块
    print("📦 初始化模块...")
    config = {
        'sources': {
            'tech_media': {'enabled': True},
            'industry_reports': {'enabled': True},
            'social_media': {'enabled': False}
        }
    }
    
    collector = MaterialCollector(config)
    classifier = MaterialClassifier()
    evaluator = QualityEvaluator()
    exporter = MaterialExporter()
    
    print("   ✓ 采集器已就绪")
    print("   ✓ 分类器已就绪")
    print("   ✓ 评估器已就绪")
    print("   ✓ 导出器已就绪")
    print()
    
    # 2. 执行素材采集
    topic = "人工智能"
    days_back = 7
    print(f"🔍 开始采集素材 - 主题：{topic}，时间范围：过去{days_back}天")
    print("-" * 60)
    
    materials = collector.collect(topic, days_back)
    print(f"\n✅ 采集完成！共获取 {len(materials)} 条素材")
    print()
    
    # 3. 展示采集结果
    print("📋 采集到的素材列表:")
    print("-" * 60)
    for i, m in enumerate(materials, 1):
        print(f"{i}. {m['title']}")
        print(f"   来源：{m['source_type']} | 日期：{m['publish_date']}")
        print(f"   关键词：{', '.join(m.get('keywords', [])[:3])}")
        print()
    
    # 4. 素材分类
    print("🏷️  执行智能分类...")
    print("-" * 60)
    
    classified_results = []
    for material in materials:
        result = classifier.classify(material)
        classified_results.append(result)
        print(f"✓ {result['title'][:30]}... → {result['category']} (置信度：{result['category_confidence']:.2f})")
    
    print()
    
    # 5. 质量评估
    print("⭐ 执行质量评估...")
    print("-" * 60)
    
    evaluated_results = []
    for material in classified_results:
        result = evaluator.evaluate(material)
        evaluated_results.append(result)
        score_breakdown = result['score_breakdown']
        total_score = (
            score_breakdown['credibility'] * 0.40 +
            score_breakdown['timeliness'] * 0.25 +
            score_breakdown['completeness'] * 0.20 +
            score_breakdown['verification'] * 0.15
        )
        print(f"✓ {result['title'][:30]}... → 评分：{total_score:.1f}/100 | 等级：{result['rating']}")
    
    print()
    
    # 6. 生成统计报告
    print("📊 生成统计报告...")
    print("-" * 60)
    
    # 手动计算统计信息
    total_materials = len(evaluated_results)
    rating_dist = {}
    for m in evaluated_results:
        rating = m['rating']
        rating_dist[rating] = rating_dist.get(rating, 0) + 1
    
    avg_score = sum(m['score'] for m in evaluated_results) / total_materials if total_materials > 0 else 0
    
    stats = {
        'total_materials': total_materials,
        'average_quality_score': avg_score,
        'rating_distribution': rating_dist
    }
    
    print(f"素材总数：{stats['total_materials']}")
    print(f"平均质量分：{stats['average_quality_score']:.1f}/100")
    print(f"S 级素材：{stats['rating_distribution'].get('S', 0)} 条")
    print(f"A 级素材：{stats['rating_distribution'].get('A', 0)} 条")
    print(f"B 级素材：{stats['rating_distribution'].get('B', 0)} 条")
    print()
    
    # 7. 导出 Markdown 报告
    print("📄 生成 Markdown 报告...")
    print("-" * 60)
    
    md_content = exporter.export_to_markdown(evaluated_results, topic)
    
    # 保存到文件（简化版直接返回内容）
    print(f"✓ 报告已生成（{len(md_content)} 字符）")
    print()
    
    # 展示报告预览
    print("📖 报告预览（前 80 行）:")
    print("-" * 60)
    
    lines = md_content.split('\n')[:80]
    print('\n'.join(lines))
    
    print()
    print("=" * 60)
    print("✅ 功能演示完成！")
    print("=" * 60)
    
    return {
        'materials_count': len(materials),
        'report_preview': md_content[:500],
        'stats': stats
    }


if __name__ == '__main__':
    try:
        result = test_full_pipeline()
        print(f"\n📌 测试结果摘要:")
        print(f"   - 采集素材数：{result['materials_count']} 条")
        print(f"   - 平均质量分：{result['stats']['average_quality_score']:.1f}/100")
        print(f"   - 报告预览：{len(result['report_preview'])} 字符")
        print("\n✅ 所有功能测试完成！")
    except Exception as e:
        print(f"\n❌ 测试失败：{str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
