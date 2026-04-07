"""
sample_usage.py - ResearchMate 使用示例
演示如何使用素材采集技能完成一次完整的素材采集任务
"""

import sys
sys.path.insert(0, '..')

from src.collector import MaterialCollector
from src.classifier import MaterialClassifier
from src.evaluator import MaterialEvaluator
from src.exporter import MaterialExporter


def demo_full_workflow():
    """演示完整工作流程"""
    
    print("=" * 60)
    print("📚 ResearchMate 素材采集演示")
    print("=" * 60)
    
    # Step 1: 初始化各模块
    print("\n[Step 1] 初始化采集器...")
    collector = MaterialCollector()
    classifier = MaterialClassifier()
    evaluator = MaterialEvaluator()
    exporter = MaterialExporter()
    
    # Step 2: 模拟采集一些素材（实际使用时会调用真实 API）
    print("[Step 2] 采集素材...")
    topic = "新能源汽车行业分析"
    
    # 这里用模拟数据演示，实际使用时替换为真实采集
    raw_materials = [
        {
            "title": "比亚迪 2025 年销量突破 300 万辆",
            "content": "比亚迪宣布 2025 年全年新能源汽车销量达到 302.4 万辆，同比增长 38%，全球市场份额提升至 18%",
            "url": "https://example.com/byd-sales-2025",
            "source": "汽车之家",
            "collected_at": "2026-04-07 10:30"
        },
        {
            "title": "宁德时代发布新一代固态电池技术",
            "content": "能量密度突破 500Wh/kg，续航可达 1000km，预计 2027 年量产装车",
            "url": "https://example.com/catl-solid-state",
            "source": "36 氪",
            "collected_at": "2026-04-07 11:15"
        },
        {
            "title": "投资人观点：新能源赛道下半场竞争加剧",
            "content": "高瓴资本合伙人表示，行业从'电动化'转向'智能化'，软件能力成为核心竞争力",
            "url": "https://example.com/investor-view",
            "source": "晚点 LatePost",
            "collected_at": "2026-04-07 12:00"
        },
        {
            "title": "特斯拉中国 Q1 市场份额下滑至 8.2%",
            "content": "面临比亚迪、理想、蔚来等本土品牌激烈竞争，Model Y 降价应对",
            "url": "https://example.com/tesla-market-share",
            "source": "彭博社",
            "collected_at": "2026-04-07 13:20"
        }
    ]
    
    print(f"✓ 采集到 {len(raw_materials)} 条原始素材")
    
    # Step 3: 智能分类
    print("\n[Step 3] 智能分类...")
    classified_materials = []
    for mat in raw_materials:
        classified = classifier.classify(mat)
        classified_materials.append(classified)
        print(f"  • {classified['title'][:20]}... → {classified['category']}")
    
    # Step 4: 质量评估
    print("\n[Step 4] 质量评估...")
    for mat in classified_materials:
        evaluation = evaluator.evaluate(mat)
        mat.update(evaluation)
        score = mat.get('quality_score', 0)
        level = "⭐⭐⭐" if score >= 85 else "⭐⭐" if score >= 70 else "⭐"
        print(f"  • {mat['title'][:20]}... → {score}分 {level}")
    
    # Step 5: 导出报告
    print("\n[Step 5] 生成素材报告...")
    md_report = exporter.export_to_markdown(classified_materials, topic)
    
    # 保存文件
    output_file = f"./output/{topic}_素材报告.md"
    import os
    os.makedirs("./output", exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(md_report)
    
    print(f"✓ 报告已保存到：{output_file}")
    
    # Step 6: 生成写作灵感
    print("\n[Step 6] 写作灵感提示...")
    prompts = exporter.generate_writing_prompts(classified_materials)
    print(prompts)
    
    print("\n" + "=" * 60)
    print("✅ 演示完成！")
    print("=" * 60)
    
    return classified_materials


def demo_quick_collect():
    """演示快速采集模式（单函数调用）"""
    
    from src.collector import MaterialCollector
    
    print("\n🚀 快速采集模式演示\n")
    
    collector = MaterialCollector()
    
    # 一行代码完成采集 + 分类 + 评估
    materials = collector.quick_collect(
        topic="AI 大模型应用",
        sources=["tech_news", "industry_reports"],
        min_quality=70
    )
    
    print(f"\n✓ 采集完成：共 {len(materials)} 条高质量素材")
    
    return materials


if __name__ == "__main__":
    # 运行完整演示
    demo_full_workflow()
    
    # 运行快速演示
    # demo_quick_collect()
