"""
exporter.py - 素材导出器模块

负责将采集的素材导出为多种格式（Markdown、JSON、CSV、Word）
支持生成引用清单、写作灵感提示和素材评估表
"""

import json
import csv
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path


class MaterialExporter:
    """素材导出器 - 支持多格式输出"""
    
    def __init__(self, output_dir: str = "./output"):
        self.output_dir = output_dir
    
    def export_to_markdown(self, materials: List[Dict[str, Any]], 
                          topic: str = "未命名主题") -> str:
        """
        导出为 Markdown 格式的素材报告
        
        Args:
            materials: 素材列表
            topic: 文章主题
            
        Returns:
            Markdown 内容字符串
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        md_content = f"""# 📚 {topic} - 素材采集报告

**生成时间：** {timestamp}  
**素材总数：** {len(materials)} 条  
**本报告由 ResearchMate 自动生成**

---

## 📊 素材概览

"""
        
        # 统计各类素材数量
        category_stats = {}
        for mat in materials:
            cat = mat.get('category', '未分类')
            category_stats[cat] = category_stats.get(cat, 0) + 1
        
        md_content += "| 素材类型 | 数量 |\n"
        md_content += "|----------|------|\n"
        for cat, count in sorted(category_stats.items()):
            md_content += f"| {cat} | {count} |\n"
        
        md_content += "\n---\n\n"
        
        # 详细素材卡片
        md_content += "## 📝 详细素材卡片\n\n"
        
        for idx, mat in enumerate(materials, 1):
            md_content += f"### 素材 #{idx}\n\n"
            md_content += f"**标题：** {mat.get('title', '无标题')}\n\n"
            md_content += f"**类型：** {mat.get('category', '未分类')}\n\n"
            md_content += f"**来源：** [{mat.get('source', '未知')}]({mat.get('url', '#')})\n\n"
            md_content += f"**采集时间：** {mat.get('collected_at', '未知')}\n\n"
            
            if mat.get('quality_score'):
                md_content += f"**质量评分：** ⭐ {mat['quality_score']}/100\n\n"
            
            md_content += f"**核心内容：**\n\n"
            md_content += f"> {mat.get('content', '无内容')}\n\n"
            
            if mat.get('tags'):
                md_content += f"**标签：** {', '.join(mat['tags'])}\n\n"
            
            if mat.get('writing_hints'):
                md_content += f"**💡 写作灵感：**\n\n{mat['writing_hints']}\n\n"
            
            md_content += "---\n\n"
        
        # 引用清单
        md_content += "## 🔗 完整引用清单\n\n"
        md_content += "| 序号 | 标题 | 来源 | URL |\n"
        md_content += "|------|------|------|-----|\n"
        for idx, mat in enumerate(materials, 1):
            title = mat.get('title', '无标题')[:30] + "..." if len(mat.get('title', '')) > 30 else mat.get('title', '无标题')
            md_content += f"| {idx} | {title} | {mat.get('source', '未知')} | [链接]({mat.get('url', '#')}) |\n"
        
        return md_content
    
    def export_to_json(self, materials: List[Dict[str, Any]], 
                      topic: str = "未命名主题") -> str:
        """
        导出为 JSON 格式（结构化数据）
        
        Args:
            materials: 素材列表
            topic: 文章主题
            
        Returns:
            JSON 字符串
        """
        export_data = {
            "metadata": {
                "topic": topic,
                "generated_at": datetime.now().isoformat(),
                "total_materials": len(materials),
                "tool": "ResearchMate",
                "version": "0.1.0"
            },
            "materials": materials,
            "statistics": self._generate_statistics(materials)
        }
        
        return json.dumps(export_data, ensure_ascii=False, indent=2)
    
    def export_to_csv(self, materials: List[Dict[str, Any]]) -> str:
        """
        导出为 CSV 格式（适合导入 Excel 分析）
        
        Args:
            materials: 素材列表
            
        Returns:
            CSV 字符串
        """
        if not materials:
            return ""
        
        # 定义 CSV 列
        fieldnames = ['id', 'title', 'category', 'source', 'url', 
                     'content', 'quality_score', 'collected_at', 'tags']
        
        import io
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        
        writer.writeheader()
        for idx, mat in enumerate(materials, 1):
            row = {k: mat.get(k, '') for k in fieldnames}
            row['id'] = idx
            row['tags'] = ', '.join(row['tags']) if isinstance(row['tags'], list) else row['tags']
            writer.writerow(row)
        
        return output.getvalue()
    
    def _generate_statistics(self, materials: List[Dict[str, Any]]) -> Dict[str, Any]:
        """生成素材统计信息"""
        if not materials:
            return {}
        
        # 分类统计
        category_stats = {}
        quality_scores = []
        
        for mat in materials:
            cat = mat.get('category', '未分类')
            category_stats[cat] = category_stats.get(cat, 0) + 1
            
            if mat.get('quality_score'):
                quality_scores.append(mat['quality_score'])
        
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        return {
            "by_category": category_stats,
            "average_quality_score": round(avg_quality, 2),
            "high_quality_count": len([s for s in quality_scores if s >= 80]),
            "medium_quality_count": len([s for s in quality_scores if 60 <= s < 80]),
            "low_quality_count": len([s for s in quality_scores if s < 60])
        }
    
    def generate_writing_prompts(self, materials: List[Dict[str, Any]]) -> str:
        """
        基于素材生成写作灵感提示
        
        Args:
            materials: 素材列表
            
        Returns:
            写作灵感文本
        """
        if not materials:
            return "暂无足够素材生成写作灵感。"
        
        prompts = []
        
        # 识别热点话题
        all_tags = []
        for mat in materials:
            if mat.get('tags'):
                all_tags.extend(mat['tags'])
        
        tag_freq = {}
        for tag in all_tags:
            tag_freq[tag] = tag_freq.get(tag, 0) + 1
        
        top_tags = sorted(tag_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        
        if top_tags:
            prompts.append(f"🔥 **高频话题 TOP5**: {', '.join([t[0] for t in top_tags])}")
        
        # 识别数据支撑点
        data_materials = [m for m in materials if m.get('category') == '事实数据']
        if data_materials:
            prompts.append(f"\n📈 **可用数据支撑**: 共 {len(data_materials)} 条财务/市场数据，可用于论证观点")
        
        # 识别典型案例
        case_materials = [m for m in materials if m.get('category') == '典型案例']
        if case_materials:
            prompts.append(f"\n💼 **典型案例**: 共 {len(case_materials)} 个企业案例，建议选取 2-3 个做深度对比分析")
        
        # 识别专家观点
        expert_materials = [m for m in materials if m.get('category') == '专家观点']
        if expert_materials:
            prompts.append(f"\n🎯 **权威背书**: 共 {len(expert_materials)} 条投资人/CEO/分析师观点，可增强文章说服力")
        
        # 识别竞品动态
        competitor_materials = [m for m in materials if m.get('category') == '竞品动态']
        if competitor_materials:
            prompts.append(f"\n⚔️ **竞争格局**: 共 {len(competitor_materials)} 条竞品动态，建议分析行业集中度与差异化机会")
        
        # 交叉验证提示
        high_quality = [m for m in materials if m.get('quality_score', 0) >= 85]
        if len(high_quality) < len(materials) * 0.3:
            prompts.append(f"\n⚠️ **质量提醒**: 高质量素材（≥85 分）占比不足 30%，建议补充更多一手信源")
        
        return "\n\n".join(prompts)


# 使用示例
if __name__ == "__main__":
    # 测试数据
    test_materials = [
        {
            "title": "某科技公司 2025 年 Q4 财报亮点",
            "category": "事实数据",
            "source": "巨潮资讯网",
            "url": "https://example.com/report",
            "content": "营收同比增长 45%，净利润率提升至 18%",
            "quality_score": 92,
            "collected_at": "2026-04-07 15:30",
            "tags": ["财报", "增长", "利润率"],
            "writing_hints": "可用于论证行业高景气度"
        }
    ]
    
    exporter = MaterialExporter()
    
    # 导出 Markdown
    md_report = exporter.export_to_markdown(test_materials, "AI 行业分析")
    print("=== Markdown 预览 ===")
    print(md_report[:500] + "...")
    
    # 生成写作灵感
    prompts = exporter.generate_writing_prompts(test_materials)
    print("\n=== 写作灵感 ===")
    print(prompts)
