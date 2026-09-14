# -*- coding: utf-8 -*-
from pathlib import Path
p = Path(r"D:\xian-shang-you-wei\backend\frontend\index.html")
t = p.read_text(encoding="utf-8")
old = '''    } else if(sumOv){ sumOv.style.display = 'none'; }
  }
}'''
new = '''    } else if(sumOv){ sumOv.style.display = 'none'; }
  }

  // B2：型態細節／DEEP 完整 — 非 premium 一律鎖，與 daily_credit 無關
  const deepLocked = !_hasPremium();
  const deepSec = document.getElementById('deepSection');
  if(deepSec){
    deepSec.style.position = 'relative';
    let dov = deepSec.querySelector('.lock-ov.lock-ov-deep');
    if(deepLocked){
      if(!dov){ dov = document.createElement('div'); dov.className = 'lock-ov lock-ov-deep'; deepSec.appendChild(dov); }
      dov.innerHTML = `<div class="lock-ov-msg">${_authUser ? '升級後查看型態細節與深度分析' : '登入並升級後查看深度分析'}</div>`;
      dov.style.display = 'flex';
      dov.onclick = _authUser ? showUpgradeModal : showLoginModal;
    } else if(dov){ dov.style.display = 'none'; }
  }
}'''
n = t.count(old)
if n != 1:
    raise SystemExit("mask tail count=%s" % n)
p.write_text(t.replace(old, new, 1), encoding="utf-8")
print("OK deep lock B2")
