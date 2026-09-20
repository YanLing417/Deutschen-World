# -*- coding: utf-8 -*-
"""
待定项决策报告生成器
运行： python tools/build_pending.py

输出：
  data/pending_decisions.json
  docs/pending_decisions.md
  docs/pending_checklist.md   （供用户逐条勾选裁定的清单）
"""
import json
import os
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
DOCS = os.path.join(ROOT, "docs")
sys.path.insert(0, HERE)

import kb_pending as P  # noqa: E402
import kb_data as D  # noqa: E402


def md_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for r in rows:
        out.append("| " + " | ".join(
            "" if c is None else str(c).replace("|", "\\|").replace("\n", "<br>") for c in r) + " |")
    return "\n".join(out)


def main():
    items = P.PENDING
    by_pri = defaultdict(list)
    for it in items:
        by_pri[it["priority"]].append(it)

    doc = {
        "meta": {
            **D.META,
            "task": "待定项优先级与方案分析",
            "total": len(items),
            "by_priority": {k: len(v) for k, v in sorted(by_pri.items())},
        },
        "priority_legend": P.PRIORITY_LABEL,
        "items": items,
        "resolved_by_later_docs": P.RESOLVED_BY_LATER_DOCS,
    }
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, "pending_decisions.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
        f.write("\n")

    # ================= 主报告 =================
    md = ["# 待定项决策报告", "",
          f"> 共 **{len(items)}** 条待定项，按优先级排序，并为每条给出可选方案与利弊。",
          "> 处理方式：**采纳**（存在最新设定集补充）→ **生成方案** → **利弊分析** → **推荐** → **等待裁定**。",
          ""]

    md.append("## 优先级图例")
    md.append("")
    md.append(md_table(["级别", "含义"], [[k, v] for k, v in P.PRIORITY_LABEL.items()]))
    md.append("")

    md.append("## 总览")
    md.append("")
    md.append(md_table(["优先级", "条数", "条目"],
                       [[k, len(by_pri[k]), "；".join(i["topic"][:26] + ("…" if len(i["topic"]) > 26 else "")
                                                     for i in by_pri[k])]
                        for k in sorted(by_pri)]))
    md.append("")

    md.append("## 已被后续设定集完全解决的条目")
    md.append("")
    md.append("以下条目在 S2 中列为待定，但已被 S3 敲定，**不再计入待定清单**：")
    md.append("")
    md.append(md_table(["条目", "原出处", "解决于", "裁定内容"],
                       [[r["topic"], "、".join(r["src"]), r["resolved_by"], r["resolution"]]
                        for r in P.RESOLVED_BY_LATER_DOCS]))
    md.append("")
    md.append("---")
    md.append("")

    for pri in sorted(by_pri):
        md.append(f"# {P.PRIORITY_LABEL[pri]}")
        md.append("")
        for it in by_pri[pri]:
            md.append(f"## `{it['id']}`　{it['topic']}")
            md.append("")
            md.append(f"- **出处**：{'、'.join(it['src'])}")
            md.append(f"- **状态**：{it['status']}")
            if it.get("adopted"):
                md.append(f"- **已采纳内容**：{it['adopted']}")
            if it.get("why_blocking"):
                md.append(f"- **为何阻塞**：{it['why_blocking']}")
            md.append("")

            md.append("### 可选方案")
            md.append("")
            for o in it["options"]:
                star = "　★ **推荐**" if o["name"] == it["recommend"] else ""
                md.append(f"#### {o['name']}{star}")
                md.append("")
                md.append(f"{o['desc']}")
                md.append("")
                md.append(f"- **利**：{'；'.join(o['pros'])}")
                md.append(f"- **弊**：{'；'.join(o['cons'])}")
                md.append("")

            md.append("### 推荐与理由")
            md.append("")
            md.append(f"**推荐：{it['recommend']}**")
            md.append("")
            md.append(it["rationale"])
            md.append("")
            md.append(f"> **裁定状态**：{'用户已选：' + str(it['user_choice']) if it.get('user_choice') else '⏳ 等待用户裁定'}")
            md.append("")
            md.append("---")
            md.append("")

    md.append("## 出处代号")
    md.append("")
    for s in D.META["source_documents"]:
        md.append(f"- **{s['id']}** = `{s['file']}`（{s['title']}）")

    os.makedirs(DOCS, exist_ok=True)
    with open(os.path.join(DOCS, "pending_decisions.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(md))

    # ================= 勾选清单 =================
    ck = ["# 待定项裁定清单", "",
          "> 用途：逐条勾选。在每条的 `[ ]` 中填 `x` 表示采纳对应方案。",
          "> 若采用推荐方案，勾「推荐」；若选其他方案，勾该方案；若要另拟，填在「自定义」处。",
          ""]
    for pri in sorted(by_pri):
        ck.append(f"## {P.PRIORITY_LABEL[pri]}")
        ck.append("")
        for it in by_pri[pri]:
            ck.append(f"### {it['id']}　{it['topic'][:70]}")
            ck.append("")
            for o in it["options"]:
                mark = " ← 推荐" if o["name"] == it["recommend"] else ""
                ck.append(f"- [ ] {o['name']}{mark}")
            ck.append(f"- [ ] 自定义：______________________")
            ck.append("")
            ck.append(f"  推荐理由摘要：{it['rationale'][:200]}…")
            ck.append("")
    with open(os.path.join(DOCS, "pending_checklist.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(ck))

    print(f"待定项决策报告已生成：{len(items)} 条")
    for k in sorted(by_pri):
        print(f"  {k}: {len(by_pri[k])} 条")
    print("  → data/pending_decisions.json")
    print("  → docs/pending_decisions.md")
    print("  → docs/pending_checklist.md")


if __name__ == "__main__":
    main()
