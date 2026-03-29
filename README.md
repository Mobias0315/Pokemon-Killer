# 🧟 Pokemon Killer

A 2D Roguelike survival game.

---

## 🎮 Gameplay

* 使用方向鍵控制角色移動
* 角色會依照當前方向**自動攻擊**
* 擊敗敵人獲得經驗並升級，強化角色能力

---

## 🔁 Core Mechanics (Roguelike)

* **Infinite Map（無限地圖）**：遊戲場景可持續延伸與探索
* **Progression System（成長系統）**：升級時可強化數值或選擇武器升級
* **Weapon Evolution（武器進化）**：近戰與遠程武器可進化至更高階形態
* **Permadeath（死亡重來）**：死亡後需重新開始遊戲

---

## ⚔️ Combat System

* 支援**近戰**與**遠程攻擊**
* 實作**子彈系統（Projectile System）**
* 敵人強度會隨時間逐步提升

---

## 🎯 Objective

* 在不斷增強的敵人壓力下生存
* 撐過指定時間後擊敗 Boss

---

## 🛠️ Tech Stack

* **Language**: Python
* **Library**: Pygame
* **Game Engine**: None (Built from scratch)

---

## ⚙️ Technical Highlights

* **Random Spawn System**：限制敵人數量並進行隨機生成
* **Advanced Enemy Spawning**：依條件產生特殊敵人
* **Projectile System**：處理遠程攻擊與彈道邏輯
* **Infinite Map System**：支援無限延伸地圖
* **Boss Mechanics**：實作 Boss 特殊攻擊模式

---

## ▶️ How to Run

### Option 1: Run Executable (Recommended)

請確認以下檔案位於同一資料夾：

* `寶可夢大屠殺.exe`
* `img/`
* `Cubic_11_1.010_R.ttf`
* `Pixel.ttf`
* `prstart.ttf`

然後直接執行：

```bash
寶可夢大屠殺.exe
```

---

### Option 2: Run from Source

1. 安裝 Python 3.x

2. 安裝套件：

```bash
pip install pygame
```

3. 執行遊戲：

```bash
python main.py
```

> ※ 請確認所有資源檔案與程式位於同一目錄

---

## 🚧 Project Status

* 核心玩法已完成
* 專案可遊玩

### 未來可能優化

* 遊戲平衡調整
* 更多武器與敵人種類
* 系統優化

---

## 👤 Author

**Mobias0315**

---
