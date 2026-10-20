# 八字命理评估数据集 (BaZi Fortune-Telling Evaluation Dataset)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📖 数据集简介

本项目及相关论文知识成果现已应用于[AuraMate灵伴](https://auramate.net/)玄学陪伴产品。相关论文见[论文链接](https://arxiv.org/abs/2602.12889)。

本数据集是用于评估大型语言模型（LLM）在中国传统八字命理推理能力的基准测试集。数据集包含真实人物的出生信息（年月日时）、性别、出生地点，以及由命理师出题、命主真实经历作答案的选择题。

数据集分为三个部分：
1. **Contest8 系列（2021–2026）**：香港青年術數家協會「全球算命師大賽」第 12–17 届真题，每年 8 位命主 × 5 题 = 40 题。2021–2025 为论文所用的原始基准；**2026 为本次新增**。
2. **历届真题（2010–2020，本次新增）**：同一比赛第 1–11 届的全部真题，共 315 题。早期赛制不同（3–8 个命例、部分题有 5 个选项），文件名为 `hkjfma_YYYY.json`。
3. **Celebrity50**：50 位名人的详细命理信息和人生事件。

> 至此「全球算命師大賽」2010–2026 年 **全部 17 届**都已收录，共 **555 道**真题。

## 📂 数据集结构

```
data/
├── contest8_2021.json … contest8_2025.json   # 第12–16届（论文基准，未改动）
├── contest8_2026.json                        # 第17届（新增）
├── hkjfma_2010.json … hkjfma_2020.json       # 第1–11届（新增）
└── celebrity50_zh.json                       # 50位名人数据集
sources/                                      # 原始网页文本、题目/答案图片、逐年出处（见 sources/README.md）
tools/
├── src/YYYY.md                               # 逐题转写稿（繁体原文 + 出处 + 答案）
└── build.py                                  # 转写稿 → data/*.json（简体）
```

## 📊 历届真题一览

| 年份 | 届 | 命例 | 题数 | 选项数 | 术数构成（题数） | 答案来源 | 人类冠军成绩 | 文件 |
|---|---|---|---|---|---|---|---|---|
| 2010 | 1 | 3 | 9 | 5 | 未注明 | 官方 | 6/9 | `hkjfma_2010.json` |
| 2011 | 2 | 3 | 15 | 5 | 未注明 | 官方 | 8/15 | `hkjfma_2011.json` |
| 2012 | 3 | 3 | 15 | 4 | 未注明 | 官方 | 8/15 | `hkjfma_2012.json` |
| 2013 | 4 | 4 | 16 | 4 | 未注明 15 · 奇门 1 | 官方 | 未存档 | `hkjfma_2013.json` |
| 2014 | 5 | 7 | 35 | 4 | 八字 20 · 紫微 10 · 奇门 5 | 转载 | 未存档 | `hkjfma_2014.json` |
| 2015 | 6 | 7 | 35 | 4 | 八字 25 · 紫微 10 | 官方 | 15/35（去高低后 12/25） | `hkjfma_2015.json` |
| 2016 | 7 | 7 | 35 | 4 | 八字 25 · 紫微 10 | 官方 | 23/35（去高低后 17/25） | `hkjfma_2016.json` |
| 2017 | 8 | 7 | 35 | 4 | 八字 30 · 紫微 5 | 转载 | 去高低后 12/25 | `hkjfma_2017.json` |
| 2018 | 9 | 8 | 40 | 4 | 八字 25 · 紫微 10 · 奇门 5 | 官方 | 19/40（15/30） | `hkjfma_2018.json` |
| 2019 | 10 | 8 | 40 | 4 | 八字 25 · 紫微 10 · 未注明 5 | 转载 | 20/40（15/30） | `hkjfma_2019.json` |
| 2020 | 11 | 8 | 40 | 4（第1命例为 5） | 八字 35 · 紫微 5 | 转载 | 17/40（13/30） | `hkjfma_2020.json` |
| 2021–2025 | 12–16 | 8 | 40×5 | 4 | — | 官方 | 2023: 21/40 · 2025: 32/40 | `contest8_202X.json` |
| 2026 | 17 | 8 | 40 | 4 | 八字 20 · 紫微 10 · 未注明 10 | 官方 | 31/40（23/30） | `contest8_2026.json` |

- **术数构成**：出题老师用哪门术数出题（子平八字、紫微斗数、奇门遁甲）。早期几届原文没写，标「未注明」。用纯八字方法评测时，可按 `setter.method` 过滤掉紫微、奇门命例。
- **答案来源**：「官方」= 主办方公布的答案；「转载」= 官方答案已无存档，取自转载站。该转载站与 10 个有官方答案年份的 283 题**逐题全部一致**，详见 [`sources/README.md`](sources/README.md)。只想用官方答案时，按 `answer_source` 过滤。
- **人类冠军成绩**：主办方公布的冠军答对题数。2014 年起采用「跳水式」计分（2014 年只去掉得分最高的命例，2015 年起最高、最低各去掉一个），括号内为去掉后的成绩。

### 题量汇总

| 部分 | 命主 | 题目 |
|---|---|---|
| 历届真题 2010–2020 | 68 | 315 |
| Contest8 2021–2025 | 41 | 200 |
| Contest8 2026 | 8 | 40 |
| Celebrity50 | 50 | 488 |
| **合计** | **167** | **1043** |

## 📋 数据格式

所有 `contest8_*.json` 与 `hkjfma_*.json` 结构相同：JSON 数组，第 0 个元素是比赛元信息，其后每个元素是一个命主。

### 比赛元信息（新增文件）

```json
{
  "contest_id": "hkjfma_2018",
  "current_year": "2018",
  "edition": 9,
  "title": "2018第九届全球算命师比赛",
  "description": "香港青年术数家协会「全球算命师大赛」第9届真题。…",
  "total_questions": 40,
  "num_charts": 9,
  "scoring": "像跳水评分，删除最高分及最低分的命例，以中间六个命例共 30 题为最后成绩",
  "answer_source": "official",
  "sources": {"questions": "https://hkjfma.org/?page_id=9264", "answers": "https://hkjfma.org/?page_id=9290（手写答案表图片…）"},
  "corrections": ["…原文笔误及改正…"]
}
```

### 命主（新增文件）

```json
{
  "person_id": "2018_C5_female_19401013",
  "name": "1940年台湾出生女性",
  "case_no": "5",
  "profile": {
    "birth": {
      "year": 1940, "month": 10, "day": 13,
      "hour": 14, "minute": 0,
      "place": "台湾",
      "approximate": true,
      "time_raw": "未时",
      "raw": "台湾出生女命:公历1940年10月13日 未时（命例问题提供:台湾 子平八字 陈开通师傅）"
    },
    "gender": "female"
  },
  "setter": {"name": "陈开通", "method": "子平八字"},
  "context": [],
  "notes": ["官网原文漏印此命例的出生资料…"],
  "categories": {"感情": [], "财富": [], "六亲": [], "事业": [], "健康": []},
  "questions": [
    {
      "question_id": "2018_C5_female_19401013-Q21",
      "question_no": 21,
      "question": "此命的出身家庭及学历文化?",
      "options": ["A. 出身富裕家庭, 大学毕业", "B. 出身富裕家庭, 中学未毕业", "C. 出身贫穷家庭, 大学毕业", "D. 出身贫穷家庭, 中学未毕业"],
      "answer": "D"
    }
  ]
}
```

### Celebrity50 格式

Celebrity50包含50位名人的详细信息：

```json
[
  {
    "person_id": "albert_ii_prince_of_monaco_P001",
    "name": "Albert II, Prince of Monaco",
    "profile": {
      "birth": {
        "year": 1958,
        "month": 3,
        "day": 14,
        "hour": 12,
        "minute": 0,
        "place": "Monaco, Monaco",
        "approximate": false
      },
      "gender": "male"
    },
    "categories": {
      "感情": ["详细的感情事件时间线..."],
      "财富": ["详细的财富事件时间线..."],
      "六亲": ["详细的家庭关系事件..."],
      "事业": ["详细的事业事件时间线..."],
      "健康": ["详细的健康事件..."]
    },
    "questions": [
      {
        "question_id": "albert_ii_prince_of_monaco_P001-Q1",
        "question": "此人在哪一年结婚？",
        "options": ["A. 2010", "B. 2011", "C. 2012", "D. 2013"],
        "answer": "B"
      }
    ]
  }
]
```


### 🔑 关键字段说明

**与 2021–2025 原有文件相同的字段**：`person_id`、`name`、`profile.birth.{year,month,day,hour,minute,place,raw}`、`profile.gender`、`categories`、`questions[].{question_id,question,options,answer}`。原有读取和评测代码不用改。

**新增文件多出的字段**：

| 字段 | 说明 |
|---|---|
| `edition` / `title` / `scoring` | 届次、官方赛名、当年计分规则 |
| `answer_source` | `official`（官方答案）或 `secondary`（转载站答案） |
| `sources` | 题目与答案的出处链接 |
| `corrections` | 转写时改正的原文笔误，逐条列出 |
| `case_no` | 命例编号。同一位老师给了两个出生资料时拆成 `7a`/`7b` 两个命主，按官方计分时应合并为一个命例 |
| `profile.birth.time_raw` | 原文的出生时间写法，如 `"申时"`、`"19:15"` |
| `profile.birth.approximate` | `true` 表示原文只给到时辰（或时间区间），`hour` 取该时辰的中点（子时=0、丑时=2 … 亥时=22）；`false` 表示原文给了具体时刻；`null` 表示时间未知 |
| `setter` | 出题老师与其所用术数（原文未写则为 `null`） |
| `context` | 出题老师随题附上的已知信息（如定盘资料、生平事件），作答时应一并提供给模型 |
| `notes` | 整理者备注（如生辰补录的依据） |
| `questions[].question_no` | 当年题号（1–40），与官方答案表一致 |
| `questions[].accepted_answers` | 官方认可多个答案时出现（目前只有 2015 年第 18 题：B 或 D） |

### 需要特别处理的题目

- **2013 年第 16 题**：给出生日期和一串生平事件，反推出生时辰，所以该命主 `hour` 为 `null`，事件写在 `context`。
- **2019 年第 8 命例**：两位同年同月同日同时出生、一在香港一在广东中山的女性，题目问「此命两人」。
- **2017 年第 7 命例、2020 年第 8 命例、2018 年第 1 命例**：一位老师给了两个出生资料，拆成 `a`/`b` 两个命主。
- **2010、2011 年全部题目和 2020 年第 1–5 题**有 5 个选项（A–E），随机猜中率是 20% 而不是 25%。

## 💡 使用示例

### Python 读取全部真题

```python
import json, glob

def load(path):
    data = json.load(open(path, encoding='utf-8'))
    return data[0], data[1:]          # 元信息, 命主列表

files = sorted(glob.glob('data/hkjfma_*.json')) + sorted(glob.glob('data/contest8_*.json'))
for f in files:
    meta, persons = load(f)
    n = sum(len(p['questions']) for p in persons)
    print(meta['current_year'], meta.get('answer_source', 'official'), n, '题')
```

### 评估示例

```python
def is_correct(question, model_answer):
    """官方认可多个答案时，accepted_answers 里任何一个都算对。"""
    accepted = question.get('accepted_answers', [question['answer']])
    return model_answer.upper() in accepted

def evaluate(persons, model_answers):
    """model_answers: {question_id: 'A'|'B'|...}；返回原始准确率与官方式去高低分成绩。"""
    per_case = {}
    total = correct = 0
    for p in persons:
        case = str(p.get('case_no', p['person_id'])).rstrip('ab')   # 7a/7b 合并成一个命例
        for q in p['questions']:
            ok = is_correct(q, model_answers.get(q['question_id'], ''))
            total += 1
            correct += ok
            per_case[case] = per_case.get(case, 0) + ok
    scores = sorted(per_case.values())
    trimmed = sum(scores[1:-1]) if len(scores) > 2 else sum(scores)   # 去掉最高、最低命例（2015 年起的赛制）
    return correct / total, trimmed
```

> 计分规则逐年不同：2014 年只去掉最高分命例，2015–2017 年去掉最高和最低（剩 5 个命例），2018 年起去掉最高和最低（剩 6 个命例共 30 题）。每年的规则写在元信息的 `scoring` 字段。

### 重新生成数据

`data/hkjfma_*.json` 和 `data/contest8_2026.json` 由 `tools/src/YYYY.md`（逐题转写稿，繁体）生成：

```bash
pip install opencc
python tools/build.py data
```

## 📈 基准性能

使用本数据集评估的模型性能（Contest8 2021-2025平均，不去除极值）：

| 模型 | 方法 | 平均准确率 |
|------|------|-----------|
| DeepSeek-Chat-v3 | Multi-turn | 36.70% |
| DeepSeek-Chat-v3 | Structured | 38.00% |
| DeepSeek-R1 | Multi-turn | 34.10% |
| DeepSeek-R1 | Structured | 35.00% |
| GPT-5.1-Chat | Multi-turn | 32.50% |
| Gemini-3-Pro | Multi-turn | 32.10% |
| Gemini-2.5-Flash | Multi-turn | 32.40% |

*注：详细评估方法和结果请参考相关论文。*

## 🎯 数据集特点

### ✅ 优势

1. **真实性**：所有命主为真实人物，事件经过验证
2. **标准化**：统一的JSON格式，易于解析和处理
3. **多样性**：涵盖不同年代、性别、地区的命主
4. **专业性**：问题由专业命理师设计和审核
5. **可重复**：固定的测试集，便于模型对比

### ⚠️ 局限性

1. 样本量有限（167 个出生资料，1043 题）；2014、2017、2019、2020 四年的答案来自转载站
2. 主要为中文语境，可能存在文化特异性
3. 选择题格式，可能无法全面评估推理能力
4. 缺少推理过程的标注

## 🔬 研究用途

本数据集适用于以下研究方向：

- 大型语言模型的领域知识评估
- 传统文化知识的AI理解能力
- 多步推理和因果推理能力测试
- 中文自然语言理解
- Few-shot学习和In-context学习

## 📄 引用

如果您在研究中使用了本数据集，请引用：

```bibtex
@dataset{bazi_QA,
  title={BaZi Fortune-Telling QA Dataset},
  author={Jiangxi Chen},
  year={2025},
  publisher={GitHub},
  url={https://github.com/ChenJiangxi/BaziQA}
}
```

## 📜 许可证

本数据集采用 **MIT License** 开源协议。

您可以自由地：
- ✅ 使用：用于商业或非商业目的
- ✅ 修改：改编和修改数据集
- ✅ 分发：分享给他人
- ✅ 私用：用于私人项目

但需要：
- ⚠️ 保留版权声明和许可证声明
- ⚠️ 声明是否进行了修改

详见 [LICENSE](../LICENSE) 文件。

## ⚠️ 免责声明

1. **科研用途**：本数据集仅用于学术研究和AI评估，不构成任何形式的命理建议。
2. **隐私保护**：名人信息来自公开资料，其他命主已进行匿名化处理。
3. **文化尊重**：八字命理为中国传统文化的一部分，使用时请尊重文化传统。
4. **结果解释**：AI模型的预测结果不应被视为专业的命理咨询。

## 🤝 贡献

欢迎贡献！如果您发现数据错误或有改进建议，请：

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

或直接在 [Issues](https://github.com/Chenjiangxi/BaziQA/issues) 页面报告问题。

## 📧 联系方式

如有疑问或建议，请通过以下方式联系：

- **GitHub Issues**: [提交Issue](https://github.com/Chenjiangxi/BaziQA/issues)

## 🔗 相关资源

- [AuraMate灵伴 项目主页](https://auramate.net/)
- [论文链接](https://arxiv.org/abs/2602.12889)

## 📊 更新日志

### v2.0.0 (2026-10-20)
- ✅ 新增「全球算命師大賽」第 1–11 届（2010–2020）全部真题 315 题：`data/hkjfma_2010.json` – `hkjfma_2020.json`
- ✅ 新增第 17 届（2026）40 题及官方答案：`data/contest8_2026.json`
- ✅ 新增 `sources/`：原始网页文本、题目/答案图片和逐年出处说明；新增 `tools/`：逐题转写稿与生成脚本
- ✅ 新增字段：`answer_source`、`sources`、`corrections`、`case_no`、`setter`、`context`、`time_raw`、`accepted_answers`
- ℹ️ 2021–2025 年文件未改动
- 📝 更正文档数字：Celebrity50 实际为 488 题（v1.0.0 文档写成 250）；contest8_2021 含 9 个出生资料

### v1.0.0 (2025-02)
- 🎉 初始发布
- ✅ 包含Contest8 2021-2025数据（40题/年 × 5年 = 200题）
- ✅ 包含Celebrity50数据集（50人 × 5题 = 250题）
- ✅ 提供完整的元数据和文档

---

**最后更新**: 2026年10月20日
