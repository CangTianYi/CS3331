# 校园咸鱼 V1.0 

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Framework](https://img.shields.io/badge/Framework-PyQt6-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)

“校园咸鱼”是一个轻量级的桌面应用程序，旨在帮助大学生快速发布和查找校内闲置物品。

## V1.0 核心功能 (PRD 2.0)

本项目已实现 PRD V1.0 的核心功能闭环：**发布 -> 浏览 -> 查找 -> 联系**。

* **FR-001: 物品列表展示**：
    * 主界面以表格形式展示所有物品（名称、描述、联系方式）。
    * 列表在添加或删除后自动刷新。
* **FR-002: 添加物品信息**：
    * 通过模式对话框 (QDialog) 添加新物品。
    * 包含必填项校验（物品名称、联系信息）。
* **FR-003: 删除物品信息**：
    * 选中主列表中的物品。
    * 通过“删除”按钮并经过安全确认 (QMessageBox) 后，永久删除数据。
* **FR-004: 查找物品信息**：
    * 在主界面提供搜索框。
    * 支持对“物品名称”和“物品描述”进行关键词模糊匹配。
    * 支持清除搜索结果，恢复显示所有物品。

## 技术栈与架构 (PRD 4.0)

* **语言**: Python 3.x
* **GUI 框架**: PyQt6 (可轻松兼容 PyQt5)
* **数据存储**: 本地 `items.csv` 文件 (V1.0 方案，使用 `uuid` 作为唯一ID)
* **核心架构**: MVC (Model-View-Controller) 模式

## 项目结构 (PRD 4.3)

本项目严格按照 MVC 模式进行功能拆分，确保了数据逻辑与 UI 视图的分离。
