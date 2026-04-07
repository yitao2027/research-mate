#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ResearchMate - 商业文章素材采集助手

主程序入口
提供命令行接口，支持单主题采集、批量采集和测试模式
"""

import argparse
import os
import sys
import re
from datetime import datetime
from pathlib import Path

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from collector import MaterialCollector
    from classifier import MaterialClassifier
    from evaluator import QualityEvaluator
    from exporter_enhanced import EnhancedMaterialExporter
except ImportError as e:
    print(f"⚠️  导入模块失败：{e}")
    print("请确保已安装依赖：pip install -r requirements.txt")
    sys.exit(1)


def print_banner():
    """打印欢迎横幅"""
    banner = """
    ╔══════════════════════════════════════════════════════════╗
    ║           ResearchMate - 商业文章素材采集助手            ║
    ║              Research Material Collection Assistant      ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print(banner)


def load_config(config_path: str = None) -> dict:
    """加载配置文件"""
    import yaml
    
    if config_path is None:
        # 默认查找当前目录的配置文件
        if os.path.exists('config.yaml'):
            config_path = 'config.yaml'
        elif os.path.exists('config.example.yaml'):
            config_path = 'config.example.yaml'
        else:
            return get_default_config()
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            print(f"✅ 已加载配置文件：{config_path}")
            return config
    except Exception as e:
        print(f"⚠️  加载配置文件失败：{e}，使用默认配置")
        return get_default_config()


def get_default_config() -> dict:
    """返回默认配置"""
    return {
        'sources': {
            'industry_reports': True,
            'tech_media': True,
            'company_filings': False,
            'social_media': True
        },
        'output': {
            'format': 'markdown',
            'include_citations': True,
            'auto_tag': True
        },
        'filters': {
            'min_credibility_score': 0.7,
            'max_age_days': 30,
            'require_data_points': True
        }
    }


def run_test_mode():
    """运行测试模式"""
    print("\n🧪 进入测试模式...\n")
    
    # 测试各个模块
    print("1. 测试采集器模块...")
    try:
        collector = MaterialCollector()
        print("   ✅ 采集器初始化成功")
    except Exception as e:
        print(f"   ❌ 采集器测试失败：{e}")
    
    print("\n2. 测试分类器模块...")
    try:
        classifier = MaterialClassifier()
        print("   ✅ 分类器初始化成功")
    except Exception as e:
        print(f"   ❌ 分类器测试失败：{e}")
    
    print("\n3. 测试评估器模块...")
    try:
        evaluator = QualityEvaluator()
        print("   ✅ 评估器初始化成功")
    except Exception as e:
        print(f"   ❌ 评估器测试失败：{e}")
    
    print("\n4. 测试导出器模块...")
    try:
        exporter = MaterialExporter()
        print("   ✅ 导出器初始化成功")
    except Exception as e:
        print(f"   ❌ 导出器测试失败：{e}")
    
    print("\n✅ 所有模块测试完成！")
    print("\n💡 提示：如果看到 ❌ 错误，请检查依赖安装和配置文件")
    return True


def ask_human(topic: str = None, keywords: list = None, target_words: int = None):
    """向用户提问收集关键信息"""
    
    print("\n" + "=" * 60)
    print("📋 ResearchMate 素材采集助手")
    print("=" * 60)
    
    # 问题 1：选题描述
    if not topic:
        topic = input("\n❓ 请描述您的选题（想写什么主题的文章）：").strip()
        while not topic:
            print("   ⚠️  选题不能为空，请重新输入")
            topic = input("\n❓ 请描述您的选题：").strip()
    
    # 问题 2：关键实体（产品/企业/人物/事件）
    if not keywords:
        print("\n💡 为了更精准地采集素材，请提供以下信息：")
        keywords_input = input("   关键词（产品名称、企业名称、人物姓名或事件名称，多个用逗号分隔）：").strip()
        
        if keywords_input:
            # 支持中英文逗号
            keywords = [k.strip() for k in re.split(r'[,,]', keywords_input) if k.strip()]
        else:
            # 从选题中自动提取关键词（简化版）
            keywords = [topic]
            print(f"   ℹ️  未提供关键词，将使用选题作为关键词：{keywords}")
    
    # 问题 3：目标字数
    if not target_words:
        target_words_input = input("\n📝 您计划写多少字的内容？（例如：3000）：").strip()
        
        try:
            target_words = int(target_words_input)
            if target_words < 500:
                print("   ⚠️  字数过少，已调整为最低 500 字")
                target_words = 500
            elif target_words > 100000:
                print("   ⚠️  字数过多，已调整为最高 100000 字")
                target_words = 100000
        except ValueError:
            print(f"   ⚠️  无效输入，使用默认值 3000 字")
            target_words = 3000
    
    # 计算需要采集的素材字数（8-10 倍）
    min_material_words = target_words * 8
    max_material_words = target_words * 10
    
    print("\n" + "-" * 60)
    print("✅ 已确认采集需求：")
    print(f"   📌 选题：{topic}")
    print(f"   🔑 关键词：{', '.join(keywords)}")
    print(f"   📊 目标字数：{target_words} 字")
    print(f"   📚 预计采集素材：{min_material_words}-{max_material_words} 字（{target_words}字的 8-10 倍）")
    print("-" * 60)
    
    return {
        'topic': topic,
        'keywords': keywords,
        'target_words': target_words,
        'material_words_range': (min_material_words, max_material_words)
    }


def collect_materials(topic: str, days_back: int = 7, config: dict = None, keywords: list = None, target_words: int = None):
    """执行素材采集流程（增强版）"""
    
    print(f"\n🎯 开始采集主题：【{topic}】")
    print(f"🔑 关键词：{', '.join(keywords) if keywords else topic}")
    print(f"📅 时间范围：过去 {days_back} 天")
    print(f"📊 目标字数：{target_words} 字")
    print("-" * 60)
    
    # 初始化各模块
    collector = MaterialCollector(config)
    classifier = MaterialClassifier()
    evaluator = QualityEvaluator(config)
    exporter = EnhancedMaterialExporter()
    
    # Step 1: 采集原始素材
    print("\n📥 Step 1: 采集原始素材...")
    raw_materials = collector.collect(topic, days_back=days_back)
    print(f"   采集到 {len(raw_materials)} 条原始素材")
    
    if not raw_materials:
        print("   ⚠️  未找到相关素材，请尝试调整关键词或扩大时间范围")
        return []
    
    # Step 2: 智能分类
    print("\n🏷️  Step 2: 智能分类...")
    classified_materials = classifier.classify_batch(raw_materials)
    
    # 统计各类别数量
    category_count = {}
    for m in classified_materials:
        cat = m.get('category', '未分类')
        category_count[cat] = category_count.get(cat, 0) + 1
    
    for cat, count in sorted(category_count.items(), key=lambda x: x[1], reverse=True):
        print(f"   {cat}: {count} 条")
    
    # Step 3: 质量评估
    print("\n⭐ Step 3: 质量评估...")
    evaluated_materials = evaluator.evaluate_batch(classified_materials)
    
    # 过滤低质量素材
    min_score = config.get('filters', {}).get('min_credibility_score', 0.7)
    high_quality = [m for m in evaluated_materials if m.get('score', 0) >= min_score]
    
    print(f"   高质量素材：{len(high_quality)} 条 (≥{min_score})")
    print(f"   已过滤：{len(evaluated_materials) - len(high_quality)} 条")
    
    # Step 4: 生成提纲和总结
    print("\n📋 Step 4: 生成文章提纲和总结...")
    outline, summary = exporter.generate_outline_and_summary(evaluated_materials, topic)
    print("   ✅ 已生成文章提纲")
    print("   ✅ 已生成核心总结")
    
    # Step 5: 导出 Word 报告
    print("\n📄 Step 5: 导出 Word 素材报告...")
    word_report_path = exporter.export_to_word(
        evaluated_materials, 
        topic, 
        outline, 
        summary,
        target_words
    )
    print(f"   ✅ Word 报告：{word_report_path}")
    
    # Step 6: 生成素材评估表
    print("\n📊 Step 6: 生成素材评估表...")
    assessment_csv_path = exporter.generate_assessment_form(evaluated_materials, topic)
    print(f"   ✅ 评估表：{assessment_csv_path}")
    
    # Step 7: 收集用户反馈
    print("\n💬 Step 7: 收集素材反馈...")
    feedback = exporter.collect_feedback(evaluated_materials)
    
    if feedback['need_more']:
        print(f"\n📌 用户需要补充的素材方向：")
        for suggestion in feedback['need_more']:
            print(f"   - {suggestion}")
        
        # 询问是否重新采集
        retry_input = input("\n❓ 是否需要针对这些方向重新采集素材？(y/n)：").strip().lower()
        
        if retry_input == 'y':
            print("\n🔄 启动补充采集流程...")
            # TODO: 实现补充采集逻辑
    
    # 输出最终报告
    print("\n" + "=" * 60)
    print("🎉 素材采集完成！")
    print("=" * 60)
    print(f"📁 Word 报告：{word_report_path}")
    print(f"📊 评估表格：{assessment_csv_path}")
    print(f"✅ 高质量素材：{len(evaluated_materials)} 条")
    print(f"⭐ 满意素材：{feedback['satisfied_count']} 条")
    print("=" * 60)
    
    return evaluated_materials


def main():
    """主函数（增强交互版）"""
    parser = argparse.ArgumentParser(
        description='ResearchMate - 商业文章素材采集助手（增强版）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python main.py                          # 交互模式
  python main.py --topic "新能源汽车行业"  # 指定主题
  python main.py --topic "人工智能" --days 14
  python main.py --test                   # 测试模式
        """
    )
    
    parser.add_argument('--topic', '-t', type=str, help='采集主题（单个）')
    parser.add_argument('--keywords', '-k', type=str, help='关键词（逗号分隔）')
    parser.add_argument('--words', '-w', type=int, help='目标字数')
    parser.add_argument('--days', '-d', type=int, default=7, help='采集过去 N 天的素材（默认：7）')
    parser.add_argument('--output', '-o', type=str, default='materials/', help='输出目录（默认：materials/）')
    parser.add_argument('--config', '-c', type=str, help='配置文件路径（默认：config.yaml）')
    parser.add_argument('--test', action='store_true', help='运行测试模式')
    
    args = parser.parse_args()
    
    # 打印欢迎信息
    print_banner()
    
    # 加载配置
    config = load_config(args.config)
    
    # 测试模式
    if args.test:
        run_test_mode()
        return
    
    # 交互式提问收集需求
    topic = args.topic
    keywords = args.keywords.split(',') if args.keywords else None
    target_words = args.words
    
    requirements = ask_human(topic, keywords, target_words)
    
    topic = requirements['topic']
    keywords = requirements['keywords']
    target_words = requirements['target_words']
    
    # 执行采集
    collect_materials(
        topic, 
        days_back=args.days, 
        config=config,
        keywords=keywords,
        target_words=target_words
    )


if __name__ == '__main__':
    main()
