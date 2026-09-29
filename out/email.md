To: erichfriedman68@gmail.com
Subject: Minimizing the Ratio of Max to Min Distance in 3 Dimensions: extension to n=31-50

Dear Erich,

I would like to extend "Minimizing the Ratio of Maximum to Minimum Distance in 3 Dimensions" from n=30 up to n=50. For each n the attached picture is named mmN.gif in the style of the existing ones (minimum distances blue, maximum distances red). The values below are r^2 truncated at the 5th decimal, as on the page; none of them has a known closed form.

31. r^2 = 8.20048+ (asymmetric)
32. r^2 = 8.48157+ (3-fold rotational symmetry)
33. r^2 = 8.76740+ (asymmetric)
34. r^2 = 8.96989+ (asymmetric)
35. r^2 = 9.19358+ (asymmetric)
36. r^2 = 9.43179+ (asymmetric)
37. r^2 = 9.68131+ (asymmetric)
38. r^2 = 9.83037+ (asymmetric)
39. r^2 = 10.09465+ (asymmetric)
40. r^2 = 10.30843+ (asymmetric)
41. r^2 = 10.52896+ (asymmetric)
42. r^2 = 10.69508+ (asymmetric)
43. r^2 = 10.90192+ (asymmetric)
44. r^2 = 11.07870+ (asymmetric)
45. r^2 = 11.24594+ (asymmetric)
46. r^2 = 11.45053+ (asymmetric)
47. r^2 = 11.71448+ (asymmetric)
48. r^2 = 11.86623+ (asymmetric)
49. r^2 = 12.02540+ (3-fold rotational symmetry)
50. r^2 = 12.25011+ (asymmetric)

In n=37 (point 12 in coords_n37.txt); n=42 (point 30 in coords_n42.txt); n=44 (point 32 in coords_n44.txt); n=46 (point 18 in coords_n46.txt), one point touches neither a shortest nor a longest pair, so it can move slightly without changing r and appears in the picture as a dot with no rods.

Method: the configurations were found by numerical optimization written and run with the help of Claude (Anthropic's AI model): many random starts of a constrained local optimizer (SLSQP; minimize t subject to 1 <= |xi-xj|^2 <= t), then basin hopping that also seeds each n from the best n-1 and n+1 configurations. As a sanity check, the same code reproduces your current values for n=12, 13 and 30. Each value was checked exactly: the coordinates were rounded to a 10^-12 grid and the ratio of max to min squared distance computed as an exact fraction. All files are in the attached maxmin3.zip, in one folder for this page: the pictures mmN.gif and the coordinates coords_nN.txt (one point per line, with the exact ratio in the header).

Please credit Limin Ge.

Best regards,
Limin Ge
