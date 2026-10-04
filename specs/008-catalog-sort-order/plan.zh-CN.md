# 实现计划：目录排序

**分支**：`008-catalog-sort-order` | **日期**：2026-10-04 | **规格**：[spec.md](./spec.md)

> 英文权威版：[plan.md](./plan.md)。执行 Spec Kit 时忽略本中文版。

## 摘要

在游戏级与脚本 manifest 上增加可选整数 `sort_order`。发现结果：有显式顺序的项按升序排在前，未写的排在后；并列与未写组内按文件夹名字典序。校验仍严格（未知键失败；非整数 `sort_order` 整次目录失败）。UI 目录树使用发现顺序；无操作者改序、不写入本机设置。

## 技术上下文

**语言/版本**：Python 3.11+  
**主要依赖**：既有 `nge_studio.catalog`（不改 UI 工具包）  
**存储**：`game_scripts/` 下作者编写的 JSON manifest（打包目录）；非本机设置  
**测试**：pytest 对校验与发现顺序的单元测试  
**目标平台**：Windows 桌面（NGE-STUDIO）  
**项目类型**：desktop-app  
**性能目标**：目录规模很小；排序开销可忽略  
**约束**：文件夹 ID 仍为身份；无 UI 改序；打包后需重建才能改已发布顺序  
**规模**：`catalog/models.py`、`validate.py`、`discover.py`、单元测试、manifest 契约、仓库样例可选写入 `sort_order`

## 宪章检查

通过 — 桌面产品优先（目录体验）；打包脚本目录（顺序在 manifest，重建后交付）；不改 NGE2 API；计划/研究/数据模型/契约/快速开始双语；目录逻辑有自动化测试。

设计后：仍通过。

## 项目结构

同英文 `plan.md`。

## 复杂度跟踪

不适用
