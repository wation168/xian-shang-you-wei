# -*- coding: utf-8 -*-
import generate_tools_v2 as g

tests = [
    'bmi-calculator',
    'lawyer-fee',
    'clothing-size',
    'salary-raise',
    'pool-volume',
    'tuition-cost',
    'ivf-cost-calculator',
]

for s in tests:
    print(s, '->', g.get_cat(s))
