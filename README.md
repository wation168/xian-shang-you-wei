# 📊 Financial Calculators

Free, open-source financial calculator functions for Node.js and browser.

Zero dependencies. MIT licensed. Copy-paste ready.

## Calculators

| Calculator | Description | Live Demo |
|-----------|-------------|-----------|
| [RSI Calculator](./calculators/rsi-calculator.js) | Relative Strength Index from closing prices | [Try it →](https://softglow-ai.com/tools/en/rsi-calculator.html) |
| [Compound Interest](./calculators/compound-interest.js) | Future value with regular contributions | [Try it →](https://softglow-ai.com/tools/en/compound-interest.html) |
| [Position Size](./calculators/position-size.js) | Optimal shares based on risk management | [Try it →](https://softglow-ai.com/tools/en/position-size.html) |
| [Risk-Reward](./calculators/risk-reward.js) | R:R ratio and breakeven win rate | [Try it →](https://softglow-ai.com/tools/en/risk-reward.html) |
| [Stop-Loss](./calculators/stop-loss.js) | Stop-loss levels (%, fixed, ATR methods) | [Try it →](https://softglow-ai.com/tools/en/stop-loss.html) |

## Quick Start

### Node.js
```js
const { calculateRSI } = require('./calculators/rsi-calculator');

const closes = [44, 44.34, 44.09, 43.61, 44.33, 44.83, 45.10,
                45.42, 45.84, 46.08, 45.89, 46.03, 45.61, 46.28, 46.00];
console.log(calculateRSI(closes, 14));
// → { rsi: 66.25, avgGain: 0.2093, avgLoss: 0.1071 }
```

### Browser
```html
<script src="calculators/rsi-calculator.js"></script>
<script>
  const result = calculateRSI([44, 44.34, ...], 14);
  document.getElementById('rsi').textContent = result.rsi;
</script>
```

## Examples

### Position Sizing
```js
const { positionSize } = require('./calculators/position-size');

// $50,000 account, risk 2% per trade, buy at $150, stop at $142
const pos = positionSize({
  accountSize: 50000,
  riskPercent: 2,
  entryPrice: 150,
  stopLoss: 142,
  targetPrice: 170
});

console.log(`Buy ${pos.shares} shares`);        // 125
console.log(`Position: $${pos.positionValue}`);  // $18,750
console.log(`R:R = ${pos.riskRewardRatio}`);     // 2.5
```

### Risk-Reward Analysis
```js
const { riskReward } = require('./calculators/risk-reward');

const rr = riskReward(100, 95, 115);
console.log(`Ratio: ${rr.ratio}`);           // 3.0
console.log(`Breakeven: ${rr.breakevenWinRate}%`); // 25%
console.log(`Verdict: ${rr.verdict}`);       // favorable
```

## 323 Free Online Tools

These are just 5 of the 323 financial calculators available at [SoftGlow](https://softglow-ai.com/tools/en/). All tools are free, no login required, available in 10 languages.

**Categories include:** Investment, Health & Fitness, Real Estate, Tax, Insurance, Loans, E-commerce, Construction, Energy, Automotive, HR, Education, Legal, and more.

## License

MIT — use it however you want.

## Contributing

Found a bug or want to add a calculator? PRs welcome.
