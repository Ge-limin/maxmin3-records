To: erichfriedman68@gmail.com
Subject: Minimizing the Ratio of Max to Min Distance in 3 Dimensions: extension to n=31-50

Dear Erich,

I would like to extend "Minimizing the Ratio of Maximum to Minimum Distance in 3 Dimensions" from n=30 up to n=50. For each n the attached picture is named mmN.gif in the style of the existing ones (minimum distances blue, maximum distances red). The values below are r^2 truncated at the 5th decimal, as on the page; none of them has a known closed form.

{{TABLE}}

{{FREE}}

Method: the configurations were found by numerical optimization written and run with the help of Claude (Anthropic's AI model): many random starts of a constrained local optimizer (SLSQP; minimize t subject to 1 <= |xi-xj|^2 <= t), then basin hopping that also seeds each n from the best n-1 and n+1 configurations. As a sanity check, the same code reproduces your current values for n=12, 13 and 30. Each value was checked exactly: the coordinates were rounded to a 10^-12 grid and the ratio of max to min squared distance computed as an exact fraction. All files are in the attached maxmin3.zip, in one folder for this page: the pictures mmN.gif and the coordinates coords_nN.txt (one point per line, with the exact ratio in the header).

Please credit Limin Ge.

Best regards,
Limin Ge
