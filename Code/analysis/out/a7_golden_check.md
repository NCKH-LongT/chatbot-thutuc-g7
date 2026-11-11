# A7 - team-written (golden) blind set: runs, exclusions, identity

Source: Code/eval/hard/results/regress/golden_*.json; script analysis/a7_golden_check.py.

- off_original: stamp 7e78438-dirty, excluded {'dev': 80, 'holdout-used': 21, 'blind': 35}, scored blind 518 {'answer': 384, 'clarify': 76, 'apologize': 58}, answer rows with a gold code 381, behavior 400, top-1 274, correct refusals 52
- A_original: stamp 7e78438-dirty, excluded {'dev': 80, 'holdout-used': 21, 'blind': 35}, scored blind 518 {'answer': 384, 'clarify': 76, 'apologize': 58}, answer rows with a gold code 381, behavior 400, top-1 275, correct refusals 55
- off_rerun: stamp 92b0d6e-dirty, excluded {'dev': 80, 'holdout-used': 21, 'blind': 35}, scored blind 518 {'answer': 384, 'clarify': 76, 'apologize': 58}, answer rows with a gold code 381, behavior 400, top-1 274, correct refusals 52
- A_rerun: stamp 92b0d6e-dirty, excluded {'dev': 80, 'holdout-used': 21, 'blind': 35}, scored blind 518 {'answer': 384, 'clarify': 76, 'apologize': 58}, answer rows with a gold code 381, behavior 400, top-1 275, correct refusals 55
- blind questions before exclusion: 553
- identical decisions original vs rerun: off 518/518, A 518/518
- base -> A on the 518: +4/-4 (p 1.000)
- refuse share: {'of_518': 0.112, 'of_553_if_no_exclusion': 0.1049}

