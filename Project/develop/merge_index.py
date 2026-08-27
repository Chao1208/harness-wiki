#!/usr/bin/env python3
"""合并 raw/papers/index_fragments/*.yaml 到 raw/papers/index.yaml，按 arXiv id 去重并核对本地文件。"""
import re, glob, os, sys, yaml

ROOT = "/Volumes/baseH/wiki-hub/harness-wiki"
PAPERS = os.path.join(ROOT, "raw/papers")

def arxiv_id(entry):
    for k in ("pdf", "url"):
        m = re.search(r"arxiv\.org/(?:abs|pdf)/([0-9]{4}\.[0-9]{4,5})", entry.get(k, "") or "")
        if m:
            return m.group(1)
    return None

merged, by_arxiv, dup_report = [], {}, []
for frag in sorted(glob.glob(os.path.join(PAPERS, "index_fragments/*.yaml"))):
    data = yaml.safe_load(open(frag))
    entries = (data.get("papers") or []) + (data.get("referenced") or [])
    for e in entries:
        aid = arxiv_id(e)
        key = aid or e["id"]
        if key in by_arxiv:
            kept = by_arxiv[key]
            dup_report.append((e["id"], kept["id"], key))
            # 异名重复：删除后登记的本地副本，保留先登记的
            if e["id"] != kept["id"]:
                p = os.path.join(PAPERS, e["id"] + ".pdf")
                if os.path.exists(p) and os.path.exists(os.path.join(PAPERS, kept["id"] + ".pdf")):
                    os.remove(p)
                    print(f"删除异名重复副本: {e['id']}.pdf (保留 {kept['id']}.pdf)")
            continue
        by_arxiv[key] = e
        merged.append(e)

merged.sort(key=lambda x: (x.get("year", 0), x["id"]))

missing = [e["id"] for e in merged if not os.path.exists(os.path.join(PAPERS, e["id"] + ".pdf"))]
indexed = {e["id"] + ".pdf" for e in merged}
orphans = [f for f in os.listdir(PAPERS) if f.endswith(".pdf") and f not in indexed]

header = """# 论文索引：PDF 只存本地，远端仓库仅保留本索引（下载链接）
# 每次下载论文后必须在此登记；字段：id/title/authors/year/url/pdf/added/agent
# 本文件由四个分支片段合并生成（change-001），按 arXiv id 去重。
"""
with open(os.path.join(PAPERS, "index.yaml"), "w") as f:
    f.write(header)
    yaml.safe_dump({"papers": merged}, f, allow_unicode=True, sort_keys=False, width=200)

print(f"合并条目: {len(merged)}")
print(f"跨分支重复(已去重): {len(dup_report)}")
for d in dup_report:
    print("  dup:", d)
print(f"索引缺本地文件: {missing or '无'}")
print(f"本地有文件但未入索引(孤儿): {orphans or '无'}")
