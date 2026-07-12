# 線上有位 — K棒與型態教學頁 開發規格

> 用途：開發參考文件，含內容架構、4語言對照、頁面規格、勝率數據
> 更新：補完K棒構造篇 + 單根K棒擴充至18種，總計50+項目

---

## 頁面定位

| 項目 | 內容 |
|------|------|
| 路由 | `/learn/patterns` |
| 目標用戶 | 新手到中階投資人 |
| 核心目的 | 降低付費門檻、建立專業信任感、SEO 長尾關鍵字 |
| 語言 | 繁中 / English / 日本語 / 한국어 |
| AdSense 價值 | 財經教學類 CPM 是一般頁面 3~5 倍，免費內容頁是廣告主力 |

---

## 頁面結構總覽

```
/learn/patterns
├── Hero
├── Section 1：K棒構造基礎（8個概念）
├── Section 2：單根K棒型態（18種）
├── Section 3：組合型態（12種）
├── Section 4：頭肩型態（2種）
├── Section 5：整理型態（11種）
├── Section 6：量價關係
└── Section 7：實戰注意事項 + 勝率統計表
```

---

## Section 1：K棒構造基礎（8個概念）

| 概念 | 說明 |
|------|------|
| 開盤價（Open） | 當日第一筆成交價 |
| 收盤價（Close） | 當日最後一筆成交價 |
| 最高價（High） | 當日最高成交價，形成上影線頂端 |
| 最低價（Low） | 當日最低成交價，形成下影線底端 |
| 實體（Body） | 開盤價到收盤價的區間，紅K=收>開，黑K=收<開 |
| 上影線（Upper Shadow） | 實體頂端到最高價，代表高點賣壓 |
| 下影線（Lower Shadow） | 實體底端到最低價，代表低點買盤 |
| 量價關係 | 成交量放大代表市場共識，縮量代表觀望，型態必須配合量能才有效 |

### 4語言對照

| Key | 繁中 | English | 日本語 | 한국어 |
|-----|------|---------|--------|--------|
| `basics.open` | 開盤價 | Open | 始値 | 시가 |
| `basics.close` | 收盤價 | Close | 終値 | 종가 |
| `basics.high` | 最高價 | High | 高値 | 고가 |
| `basics.low` | 最低價 | Low | 安値 | 저가 |
| `basics.body` | 實體 | Body | 実体 | 몸통 |
| `basics.upperShadow` | 上影線 | Upper Shadow | 上ひげ | 윗꼬리 |
| `basics.lowerShadow` | 下影線 | Lower Shadow | 下ひげ | 아랫꼬리 |
| `basics.volume` | 量價關係 | Volume & Price | 出来高と価格 | 거래량과 가격 |

---

## Section 2：單根K棒型態（18種）

### 基本型

| # | 型態 | 信號 | 勝率 | 說明 |
|---|------|------|------|------|
| 1 | 大陽線（Big Bullish） | 多頭 | 68% | 實體長，幾乎無影線，強烈買盤 |
| 2 | 大陰線（Big Bearish） | 空頭 | 71% | 實體長，幾乎無影線，強烈賣壓 |
| 3 | 禿頭陽線（Bullish Marubozu） | 強多頭 | 74% | 無影線紅K，開盤即買到收盤 |
| 4 | 禿頭陰線（Bearish Marubozu） | 強空頭 | 73% | 無影線黑K，開盤即賣到收盤 |
| 5 | 紡錘線（Spinning Top） | 中性 | 54% | 小實體，上下影線均長，多空拉鋸 |

### 十字線系列

| # | 型態 | 信號 | 勝率 | 說明 |
|---|------|------|------|------|
| 6 | 標準十字（Doji） | 反轉/不確定 | 54% | 開收盤相同，多空平衡，後續方向待確認 |
| 7 | 長腳十字（Long-legged Doji） | 強烈不確定 | 52% | 上下影線均很長，市場極度猶豫 |
| 8 | 墓碑十字（Gravestone Doji） | 空頭反轉 | 62% | 只有上影線，收盤等於開盤等於最低價，高點被打回 |
| 9 | 蜻蜓十字（Dragonfly Doji） | 多頭反轉 | 64% | 只有下影線，收盤等於開盤等於最高價，低點被撐回 |
| 10 | 四價同值（Four Price Doji） | 極端不確定 | 50% | 開高低收全部相同，幾乎無成交，流動性極低 |

### 錘子線系列

| # | 型態 | 信號 | 勝率 | 說明 |
|---|------|------|------|------|
| 11 | 錘子線（Hammer） | 多頭反轉 | 60% | 下跌後出現，小實體在上，長下影線，低點買盤強 |
| 12 | 倒錘線（Inverted Hammer） | 多頭反轉 | 57% | 下跌後出現，小實體在下，長上影線，需次日確認 |
| 13 | 上吊線（Hanging Man） | 空頭反轉 | 59% | 上漲後出現，形狀同錘子，但位置在高點，是警訊 |
| 14 | 流星線（Shooting Star） | 空頭反轉 | 66% | 上漲後出現，小實體在下，長上影線，高點賣壓強 |

### 影線特殊型

| # | 型態 | 信號 | 勝率 | 說明 |
|---|------|------|------|------|
| 15 | 長上影陽線 | 偏空 | 55% | 紅K但上影線極長，高點有大賣壓，漲勢受阻 |
| 16 | 長下影陰線 | 偏多 | 57% | 黑K但下影線極長，低點有大買盤，跌勢受撐 |
| 17 | 跳空高開K棒（Gap Up） | 多頭延續/過熱 | 65% | 開盤跳空高開，代表買氣旺，但過熱需注意回檔 |
| 18 | 跳空低開K棒（Gap Down） | 空頭延續/超跌 | 63% | 開盤跳空低開，代表賣壓重，但超跌可能反彈 |

---

## Section 3：組合型態（12種）

| # | 型態 | 信號 | 勝率 | 平均幅度 | 說明 |
|---|------|------|------|----------|------|
| 1 | 多頭吞噬（Bullish Engulfing） | 多頭反轉 | 63% | +8.5% | 第二根紅K完全包住第一根黑K |
| 2 | 空頭吞噬（Bearish Engulfing） | 空頭反轉 | 61% | -8.1% | 第二根黑K完全包住第一根紅K |
| 3 | 晨星（Morning Star） | 多頭反轉 | 72% | +10.2% | 黑K＋小實體（跳空）＋紅K，底部三根 |
| 4 | 暮星（Evening Star） | 空頭反轉 | 69% | -9.8% | 紅K＋小實體（跳空）＋黑K，頂部三根 |
| 5 | 穿刺線（Piercing Line） | 多頭反轉 | 64% | +7.3% | 黑K後紅K開低但收超過黑K實體中點 |
| 6 | 烏雲蓋頂（Dark Cloud Cover） | 空頭反轉 | 62% | -7.6% | 紅K後黑K開高但收低於紅K實體中點 |
| 7 | 孕線多頭（Bullish Harami） | 多頭反轉 | 53% | +5.1% | 大黑K後小紅K完全在其實體內 |
| 8 | 孕線空頭（Bearish Harami） | 空頭反轉 | 55% | -5.3% | 大紅K後小黑K完全在其實體內 |
| 9 | 三白兵（Three White Soldiers） | 多頭延續 | 78% | +12.4% | 連續三根紅K，每根收盤比前一根高 |
| 10 | 三黑鴉（Three Black Crows） | 空頭延續 | 76% | -11.9% | 連續三根黑K，每根收盤比前一根低 |
| 11 | 向上跳空並列陽線 | 多頭延續 | 67% | +9.1% | 跳空後連續兩根相似紅K，強勢整理 |
| 12 | 向下跳空並列陰線 | 空頭延續 | 66% | -8.7% | 跳空後連續兩根相似黑K，弱勢整理 |

---

## Section 4：頭肩型態（2種）

| # | 型態 | 信號 | 勝率 | 平均目標幅度 | 說明 |
|---|------|------|------|------------|------|
| 1 | 頭肩頂（Head & Shoulders Top） | 空頭反轉 | 83% | -22% | 左肩→頭（新高）→右肩，頸線跌破確認 |
| 2 | 頭肩底（Inverse H&S） | 多頭反轉 | 89% | +38% | 左肩→頭（新低）→右肩，頸線突破確認 |

---

## Section 5：整理型態（11種）

| # | 型態 | 信號 | 勝率 | 平均目標幅度 | 說明 |
|---|------|------|------|------------|------|
| 1 | 雙頂 M頭（Double Top） | 空頭反轉 | 72% | -18% | 兩次衝高失敗，頸線跌破確認 |
| 2 | 雙底 W底（Double Bottom） | 多頭反轉 | 78% | +26% | 兩次測底成功，頸線突破確認 |
| 3 | 三重頂（Triple Top） | 空頭反轉 | 79% | -20% | 三次衝高均失敗，比雙頂更強的賣壓 |
| 4 | 三重底（Triple Bottom） | 多頭反轉 | 82% | +28% | 三次測底均守住，比雙底更強的買盤 |
| 5 | 上升三角（Ascending Triangle） | 多頭延續 | 72% | +28% | 水平壓力線 + 上升支撐線，向上突破 |
| 6 | 下降三角（Descending Triangle） | 空頭延續 | 73% | -16% | 水平支撐線 + 下降壓力線，向下跌破 |
| 7 | 對稱三角（Symmetrical Triangle） | 不確定 | 54% | ±12% | 高點越來越低，低點越來越高，待方向確認 |
| 8 | 多頭旗形（Bull Flag） | 多頭延續 | 68% | +23% | 急漲後小幅回調整理，再度突破繼續漲 |
| 9 | 空頭旗形（Bear Flag） | 空頭延續 | 67% | -19% | 急跌後小幅反彈整理，再度跌破繼續跌 |
| 10 | 上升楔形（Rising Wedge） | 空頭反轉 | 66% | -14% | 漲勢收斂，高點低點均上升但幅度縮小，最終跌破 |
| 11 | 下降楔形（Falling Wedge） | 多頭反轉 | 69% | +32% | 跌勢收斂，高點低點均下降但幅度縮小，最終突破 |

---

## Section 6：量價關係（4個核心概念）

| 概念 | 說明 | 意義 |
|------|------|------|
| 價漲量增 | 上漲配合成交量放大 | 健康上漲，趨勢可信 |
| 價漲量縮 | 上漲但成交量萎縮 | 上漲動能不足，小心反轉 |
| 價跌量增 | 下跌配合成交量放大 | 恐慌性賣出，可能近底部 |
| 價跌量縮 | 下跌但成交量萎縮 | 下跌動能不足，可能止跌 |

---

## 4語言 i18n Key 完整對照

### 頁面標題 & 說明

| Key | 繁中 | English | 日本語 | 한국어 |
|-----|------|---------|--------|--------|
| `page.title` | K棒與型態完全解析 | Complete Guide to Candlestick Patterns | ローソク足・チャートパターン完全解説 | 캔들스틱 패턴 완전 가이드 |
| `page.subtitle` | 從K棒基礎到50+型態，附實戰勝率統計 | From candlestick basics to 50+ patterns with win-rate statistics | ローソク足の基礎から50以上のパターンまで、実際の勝率統計付き | 캔들 기초부터 50+ 패턴까지, 실전 승률 통계 포함 |
| `page.badge` | 技術分析教學 | Technical Analysis Guide | テクニカル分析ガイド | 기술적 분석 가이드 |
| `page.count` | 50+ 個型態完整解析 | 50+ Patterns Explained | 50以上のパターンを解説 | 50+ 패턴 완전 해설 |

### 章節標題

| Key | 繁中 | English | 日本語 | 한국어 |
|-----|------|---------|--------|--------|
| `section.basics` | K棒構造基礎 | Candlestick Basics | ローソク足の基礎 | 캔들스틱 기초 |
| `section.single` | 單根K棒型態 | Single Candlestick Patterns | 単一ローソク足パターン | 단일 캔들 패턴 |
| `section.combo` | 組合型態 | Combination Patterns | 組み合わせパターン | 조합 패턴 |
| `section.reversal` | 頭肩型態 | Head & Shoulders | ヘッドアンドショルダー | 헤드앤숄더 |
| `section.continuation` | 整理型態 | Continuation Patterns | 継続パターン | 지속 패턴 |
| `section.volumePrice` | 量價關係 | Volume & Price | 出来高と価格の関係 | 거래량과 가격 관계 |
| `section.tips` | 實戰注意事項 | Trading Tips | 実戦での注意点 | 실전 주의사항 |

### 型態名稱完整對照

| Key | 繁中 | English | 日本語 | 한국어 |
|-----|------|---------|--------|--------|
| `pattern.bigBullish` | 大陽線 | Big Bullish Candle | 大陽線 | 대양선 |
| `pattern.bigBearish` | 大陰線 | Big Bearish Candle | 大陰線 | 대음선 |
| `pattern.bullishMarubozu` | 禿頭陽線 | Bullish Marubozu | 陽の丸坊主 | 강세 마루보주 |
| `pattern.bearishMarubozu` | 禿頭陰線 | Bearish Marubozu | 陰の丸坊主 | 약세 마루보주 |
| `pattern.spinningTop` | 紡錘線 | Spinning Top | コマ | 팽이형 |
| `pattern.doji` | 標準十字 | Doji | 十字線 | 도지 |
| `pattern.longLeggedDoji` | 長腳十字 | Long-legged Doji | 長い十字線 | 장다리 도지 |
| `pattern.gravestoneDoji` | 墓碑十字 | Gravestone Doji | 墓石十字線 | 비석형 도지 |
| `pattern.dragonflyDoji` | 蜻蜓十字 | Dragonfly Doji | トンボ | 잠자리형 도지 |
| `pattern.fourPriceDoji` | 四價同值 | Four Price Doji | 四値同値 | 사가 동일 도지 |
| `pattern.hammer` | 錘子線 | Hammer | ハンマー | 해머 |
| `pattern.invertedHammer` | 倒錘線 | Inverted Hammer | 逆ハンマー | 역해머 |
| `pattern.hangingMan` | 上吊線 | Hanging Man | 首吊り線 | 행잉맨 |
| `pattern.shootingStar` | 流星線 | Shooting Star | 流れ星 | 슈팅스타 |
| `pattern.longUpperShadowBull` | 長上影陽線 | Long Upper Shadow Bull | 上ひげ陽線 | 긴 윗꼬리 양선 |
| `pattern.longLowerShadowBear` | 長下影陰線 | Long Lower Shadow Bear | 下ひげ陰線 | 긴 아랫꼬리 음선 |
| `pattern.gapUp` | 跳空高開 | Gap Up | 窓開け上昇 | 갭 상승 |
| `pattern.gapDown` | 跳空低開 | Gap Down | 窓開け下落 | 갭 하락 |
| `pattern.bullishEngulfing` | 多頭吞噬 | Bullish Engulfing | 陽の包み足 | 강세 장악형 |
| `pattern.bearishEngulfing` | 空頭吞噬 | Bearish Engulfing | 陰の包み足 | 약세 장악형 |
| `pattern.morningStar` | 晨星 | Morning Star | 明けの明星 | 모닝스타 |
| `pattern.eveningStar` | 暮星 | Evening Star | 宵の明星 | 이브닝스타 |
| `pattern.piercingLine` | 穿刺線 | Piercing Line | 切り込み線 | 피어싱 라인 |
| `pattern.darkCloud` | 烏雲蓋頂 | Dark Cloud Cover | 被せ線 | 먹구름형 |
| `pattern.bullishHarami` | 孕線多頭 | Bullish Harami | 陽の孕み | 강세 잉태형 |
| `pattern.bearishHarami` | 孕線空頭 | Bearish Harami | 陰の孕み | 약세 잉태형 |
| `pattern.threeWhiteSoldiers` | 三白兵 | Three White Soldiers | 赤三兵 | 적삼병 |
| `pattern.threeBlackCrows` | 三黑鴉 | Three Black Crows | 黒三兵 | 흑삼병 |
| `pattern.gapBullishParallel` | 向上跳空並列陽線 | Upward Gap Parallel Lines | 上放れ並び赤 | 상향 갭 병렬 양선 |
| `pattern.gapBearishParallel` | 向下跳空並列陰線 | Downward Gap Parallel Lines | 下放れ並び黒 | 하향 갭 병렬 음선 |
| `pattern.headAndShoulders` | 頭肩頂 | Head & Shoulders Top | ヘッドアンドショルダーズトップ | 헤드앤숄더 천정 |
| `pattern.inverseHS` | 頭肩底 | Inverse Head & Shoulders | 逆ヘッドアンドショルダーズ | 역 헤드앤숄더 |
| `pattern.doubleTop` | 雙頂 M頭 | Double Top | ダブルトップ | 더블탑 |
| `pattern.doubleBottom` | 雙底 W底 | Double Bottom | ダブルボトム | 더블바텀 |
| `pattern.tripleTop` | 三重頂 | Triple Top | トリプルトップ | 트리플탑 |
| `pattern.tripleBottom` | 三重底 | Triple Bottom | トリプルボトム | 트리플바텀 |
| `pattern.ascendingTriangle` | 上升三角 | Ascending Triangle | 上昇三角形 | 상승 삼각형 |
| `pattern.descendingTriangle` | 下降三角 | Descending Triangle | 下降三角形 | 하강 삼각형 |
| `pattern.symmetricalTriangle` | 對稱三角 | Symmetrical Triangle | 対称三角形 | 대칭 삼각형 |
| `pattern.bullFlag` | 多頭旗形 | Bull Flag | 上昇フラッグ | 강세 깃발형 |
| `pattern.bearFlag` | 空頭旗形 | Bear Flag | 下降フラッグ | 약세 깃발형 |
| `pattern.risingWedge` | 上升楔形 | Rising Wedge | 上昇ウェッジ | 상승 쐐기형 |
| `pattern.fallingWedge` | 下降楔形 | Falling Wedge | 下降ウェッジ | 하강 쐐기형 |

### 共用標籤

| Key | 繁中 | English | 日本語 | 한국어 |
|-----|------|---------|--------|--------|
| `label.signal` | 信號方向 | Signal | シグナル | 신호 |
| `label.bullish` | 多頭 | Bullish | 強気 | 강세 |
| `label.bearish` | 空頭 | Bearish | 弱気 | 약세 |
| `label.neutral` | 中性 | Neutral | 中立 | 중립 |
| `label.reversal` | 反轉 | Reversal | 反転 | 반전 |
| `label.continuation` | 延續 | Continuation | 継続 | 지속 |
| `label.winRate` | 勝率 | Win Rate | 勝率 | 승률 |
| `label.avgMove` | 平均幅度 | Avg. Move | 平均変動幅 | 평균 변동폭 |
| `label.target` | 目標幅度 | Target | 目標幅 | 목표 폭 |
| `label.bestUsed` | 最佳時機 | Best Used When | 最適な使用場面 | 최적 사용 시점 |
| `label.caution` | 注意事項 | Caution | 注意点 | 주의사항 |
| `label.example` | 實戰範例 | Example | 実例 | 실전 예시 |
| `label.volumeRequired` | 需配合量能 | Confirm with Volume | 出来高で確認 | 거래량 확인 필요 |
| `label.reliability.high` | 可信度高 | High Reliability | 信頼性高 | 신뢰도 높음 |
| `label.reliability.medium` | 可信度中 | Medium Reliability | 信頼性中 | 신뢰도 보통 |
| `label.reliability.low` | 可信度低 | Low Reliability | 信頼性低 | 신뢰도 낮음 |
| `label.free` | 免費 | Free | 無料 | 무료 |
| `label.premium` | 付費會員 | Premium | プレミアム | 프리미엄 |

---

## 技術規格

### 路由結構（Next.js App Router）

```
src/app/
└── [locale]/
    └── learn/
        └── patterns/
            └── page.tsx   ← 主頁，所有型態 + 篩選
```

### K棒 SVG 動態繪製

不用圖片，用 SVG 程式繪製，優點：動畫、深色模式、動態換色

```tsx
interface CandleProps {
  open: number;    // 0-100 相對位置
  high: number;
  low: number;
  close: number;
  color?: 'bullish' | 'bearish' | 'neutral';
  animated?: boolean;
  width?: number;
  height?: number;
}
```

### 型態資料結構

```typescript
interface Pattern {
  id: string;
  key: string;                    // i18n key
  type: 'basic' | 'single' | 'combo' | 'reversal' | 'continuation';
  signal: 'bullish' | 'bearish' | 'neutral';
  winRate: number;                // 0-100
  avgMove?: number;               // 百分比，正=漲 負=跌
  candles: CandleProps[];         // SVG 繪製用
  reliability: 'high' | 'medium' | 'low';
  volumeRequired: boolean;
  isPremium: boolean;             // 付費牆控制
}
```

### ISR 設定

```typescript
export const revalidate = 86400; // 教學內容每天更新一次
```

---



| 內容 | 開放狀態 | 理由 |
|------|----------|------|
| K棒構造基礎 | 免費 | 吸引新手，SEO 流量 |
| 單根K棒 18種 | 前10種免費，後8種付費 | 讓用戶嚐到甜頭 |
| 組合型態 12種 | 付費 | 核心價值內容 |
| 頭肩型態 | 付費 | 進階內容 |
| 整理型態 | 付費 | 進階內容 |
| 勝率統計表 | 付費 | 數據是差異化優勢 |
| 台股實際案例 | 付費 | 最高價值內容 |

---

## UI 設計建議

- 型態卡片 Grid，每卡：SVG圖解 + 型態名 + 信號badge + 勝率
- 勝率色碼：≥70% 綠色 / 50-69% 黃色 / <50% 紅色
- 信號 badge：多頭（綠）/ 空頭（紅）/ 中性（灰）
- 篩選器：多頭/空頭/中性、單根/組合/型態
- 付費內容用模糊遮罩 + 解鎖提示

---

## AdSense 審核通過要求

**所有頁面全部免費開放**，220頁全部可放廣告。

每個型態詳細頁必須包含以下內容才能通過 AdSense 審核：

| 欄位 | 最低要求 | 說明 |
|------|----------|------|
| 型態定義 | 3~5句 | 說明構成條件 |
| 形成原因 | 3~5句 | 市場心理解釋，為什麼會出現這個型態 |
| 實戰應用 | 3~5句 | 什麼時候用、怎麼搭配其他指標 |
| 注意事項 | 2~3句 | 常見誤判情況 |
| SVG 圖解 | 1個 | 程式動態繪製 |
| 勝率統計 | 顯示數字 | 來自規格內的數據 |

> ✅ 每頁自然超過 300 字，Google 判定為高品質財經教學內容，審核通過率高
> ✅ 4語言版本要有自然語言品質，不能只是機器直翻
> ✅ 網站必須有 `/about` 和 `/privacy-policy` 頁面
> ✅ 財經類關鍵字 CPC 是一般頁面 3~5 倍，220頁全開放廣告收益最大化

---

## 開發優先順序

```
Phase 1（基礎，先上線讓 Google 爬）
├── K棒構造基礎頁面
├── 單根K棒 18種（SVG圖解 + 完整說明文字）
└── 4語言 i18n

Phase 2（內容補完）
├── 組合型態 12種
├── 頭肩 & 整理型態 13種
└── 勝率統計表

Phase 3（進階，差異化）
├── K棒動畫（展示型態形成過程）
└── 台股實際案例（接 FinMind）
```

---

## SEO 關鍵字

| 語言 | 主要關鍵字 |
|------|----------|
| 繁中 | K棒型態、K線技術分析、頭肩頂怎麼看、台股技術分析教學、K棒教學 |
| English | candlestick patterns, technical analysis guide, head and shoulders pattern, doji candle |
| 日本語 | ローソク足パターン、チャート分析、テクニカル分析入門 |
| 한국어 | 캔들스틱 패턴, 기술적 분석, 차트 패턴 분석 |
