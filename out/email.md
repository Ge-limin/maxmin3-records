To: erichfriedman68@gmail.com
Subject: Minimizing the Ratio of Max to Min Distance in 3 Dimensions: extension to n=31-50

Dear Erich,

I would like to extend "Minimizing the Ratio of Maximum to Minimum Distance in 3 Dimensions" from n=30 up to n=50. For each n the attached picture is named mmN.gif in the style of the existing ones (minimum distances blue, maximum distances red), and the values below are r^2, rounded up at the 5th decimal. None of them has a known closed form.

31. r^2 = 8.20049
32. r^2 = 8.48158
33. r^2 = 8.76741
34. r^2 = 8.96990
35. r^2 = 9.19359
36. r^2 = 9.43180
37. r^2 = 9.68132
38. r^2 = 9.83038
39. r^2 = 10.09466
40. r^2 = 10.30844
41. r^2 = 10.52897
42. r^2 = 10.69509
43. r^2 = 10.90193
44. r^2 = 11.07871
45. r^2 = 11.24595
46. r^2 = 11.45054
47. r^2 = 11.71449
48. r^2 = 11.86624
49. r^2 = 12.02541
50. r^2 = 12.25012

Method: the configurations were found by numerical optimization written and run with the help of Claude (Anthropic's AI model): many random starts of a constrained local optimizer (SLSQP; minimize t subject to 1 <= |xi-xj|^2 <= t), then basin hopping that also seeds each n from the best n-1 and n+1 configurations. As a sanity check, the same code reproduces your current records for n=12, 13 and 30. Each value was checked exactly: the coordinates were rounded to a 10^-12 grid and the ratio of max to min squared distance computed as an exact fraction. The coordinates are attached (coords_nN.txt, one point per line).

Please credit {{FULL NAME}}.

Best regards,
{{FULL NAME}}
