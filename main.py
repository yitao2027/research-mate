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
from datetime import datetime
from pathlib import Path

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from collector import MaterialCollector
    from classifier import MaterialClassifier
    from evaluator import QualityEvaluator
    from exporter import MaterialExporter
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


def collect_materials(topic: str, days_back: int = 7, config: dict = None):
    """执行素材采集流程"""
    
    print(f"\n🎯 开始采集主题：【{topic}】")
    print(f"📅 时间范围：过去 {days_back} 天")
    print("-" * 60)
    
    # 初始化各模块
    collector = MaterialCollector(config)
    classifier = MaterialClassifier()
    evaluator = QualityEvaluator(config)
    exporter = MaterialExporter()
    
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
    
    # Step 4: 导出结果
    print("\n📤 Step 4: 导出素材...")
    timestamp = datetime.now().strftime("%Y-%m-%d")
    safe_topic = topic.replace("/", "_").replace("\\", "_")
    output_dir = f"materials/{timestamp}_{safe_topic}"
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 导出素材卡片
    materials_md = exporter.export_to_markdown(high_quality, output_dir)
    print(f"   ✅ 素材卡片：{materials_md}")
    
    # 导出引用清单
    citations_csv = exporter.export_citations(high_quality, output_dir)
    print(f"   ✅ 引用清单：{citations_csv}")
    
    # 生成写作灵感
    inspiration_md = exporter.generate_inspiration(high_quality, output_dir)
    print(f"   ✅ 写作灵感：{inspiration_md}")
    
    print("\n" + "=" * 60)
    print(f"🎉 采集完成！共处理 {len(high_quality)} 条高质量素材")
    print(f"📁 输出目录：{output_dir}/")
    print("=" * 60)
    
    return high_quality


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='ResearchMate - 商业文章素材采集助手',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python main.py --topic "新能源汽车行业"
  python main.py --topic "人工智能" --days 14
  python main.py --topics-file topics.txt --output batch_output/
  python main.py --test
        """
    )
    
    parser.add_argument('--topic', '-t', type=str, help='采集主题（单个）')
    parser.add_argument('--topics-file', '-f', type=str, help='包含多个主题的文本文件')
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
    
    # 单主题采集
    if args.topic:
        collect_materials(args.topic, days_back=args.days, config=config)
        return
    
    # 批量主题采集
    if args.topics_file:
        if not os.path.exists(args.topics_file):
            print(f"❌ 文件不存在：{args.topics_file}")
            return
        
        with open(args.topics_file, 'r', encoding='utf-8') as f:
            topics = [line.strip() for line in f if line.strip()]
        
        print(f"\n📋 检测到 {len(topics)} 个主题，开始批量采集...")
        
        all_materials = []
        for i, topic in enumerate(topics, 1):
            print(f"\n[{i}/{len(topics)}] 处理主题：{topic}")
            materials = collect_materials(topic, days_back=args.days, config=config)
            all_materials.extend(materials)
        
        print(f"\n🎊 批量采集完成！共获得 {len(all_materials)} 条素材")
        return
    
    # 无参数时显示帮助
    parser.print_help()


if __name__ == '__main__':
    main()
