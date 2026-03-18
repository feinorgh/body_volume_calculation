# Human Body Volume Calculation (Mostly for Cataclysm: Dark Days Ahead)

This repository contains a script that uses six different models to estimate the volume of a human body.

There is no guarantee that the results are accurate, or can be relied upon in any medical context, or even useful in a gaming context.

Also, this has been an unreasonable amount of work just to prove a point, and is unnecessarily detailed.

Anyway, To run the script, you need Python3 and matplotlib (just comment out the plotting business, if you
don't want to install matplotlib)

# Models

There are a couple of assumptions here:

* Volume = Weight / Density
* The larger the BMI of a human body, the larger ratio of fat to other components

The material composition of average humans is roughly (based on the Brozek et al. 1963 reference body):

* 12% fat
* 62% water
* 17% protein
* 6% mineral (bone and dissolved minerals)
* 3% other stuff

The densities of each respective material are assumed to be

* Fat: 0.9 g/cm³ (kg/L)
* Water: 1.0 g/cm³ (kg/L)
* Protein: 1.34 g/cm³ (kg/L)
* Mineral: 3.0 g/cm³ (kg/L)
* Other: 1.0 g/cm³ (kg/L)

The body density model uses the physically correct harmonic-mean formula for
mixture density: `1/D = Σ(f_i / d_i)` where `f_i` are mass fractions that sum
to 1.0 and `d_i` are the component densities.  This avoids the normalisation
error that would arise from an arithmetic weighted average, and the inclusion
of the mineral compartment brings the implied fat-free-mass density to ~1.10
kg/L, consistent with the literature (Siri 1961, Brozek et al. 1963).

There are six models provided:

## CDDA Original

The original volume calculation from https://github.com/CleverRaven/Cataclysm-DDA/pull/74162)

This model only takes into account the height of the character to produce a volume.

## CDDA Simple

A proposed volume calculation model based on an online tool, found in https://github.com/CleverRaven/Cataclysm-DDA/pull/74348.

This model takes into account the weight and height of the character to produce a volume, with a calculation based on average human body density.

## BMI Model

Uses the calculations for producing body fat ratio from BMI, and then applying the average body density based on lipids, water, and protein onto the weight.

This model also adjusts for the proportions of each component (fat, water, protein, etc.) and adjusts the volume calculation accordingly, i.e. the more fat, the less density, the larger the volume.

This model also can account for age and gender, although the differences I've tested so far are minimal.

## Brozek Model

Uses the Brozek formula for body fat ratio, estimated from BMI. The Brozek model reputedly has ±1% accuracy against empirical methods such as water immersion.

This model also takes the proportion of fat vs. other components into account.

Where this model breaks down (outside of normal human heights/weights) the calculations are clamped either to zero for negative results, or to double the weight for huge volumes.

## Siri Model

An older model that used to be used in the same manner as the Brozek model, reputely has ±10% accuracy compared to empirical methods.

This model also takes the proportion of fat vs. other components into account, and uses the same clamping strategy as above.

## Two-Compartment (Siri 1961) Model

Uses the standard two-compartment density model (Siri 1961) together with
the Deurenberg et al. (1998) BMI-to-body-fat conversion.  The body is
treated as two compartments — fat mass (density 0.9007 kg/L) and fat-free
mass (density 1.1000 kg/L):

    D = 1 / (BF / d_fat  +  (1 - BF) / d_ffm)

Unlike the Brozek and Siri pipeline functions (which pass density through a
second body-fat formula and back), this model applies the two-compartment
physics equation directly, avoiding compounding error.  This is the density
model most widely used in body-composition research.

# Graph over relations between models and parameters

![3D Plot](Figure_1.png)

The green lines are the original CDDA volume calculation (independent of weight) results for various heighs.

The red lines are the BMI model results.

The blue lines are the Brozek model results.

The yellow lines are the Siri model results.

The magenta lines are the Two-Compartment (Siri) model results.

You can examine this graph better if you run the script yourself, where you can rotate and zoom in.

The graph shows (mostly) that the more sensitive the model is for weight, the larger the difference
between low and high body weight.

The BMI based models (including Brozek and Siri) all seem to produce volumes that are inflated (*drum fill*) at
lower heights, the "BMI Model" less so.

It also shows that something weird is going on with the Brozek models and Siri models outside the normal
human size ranges.

# References

* https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2286542/
* https://pubmed.ncbi.nlm.nih.gov/2596420/
* https://en.wikipedia.org/wiki/Body_fat_percentage
* https://en.wikipedia.org/wiki/Body_mass_index
* https://calculator.academy/body-volume-calculator/
* https://pubmed.ncbi.nlm.nih.gov/21085903/
* Siri WE. Body composition from fluid spaces and density: analysis of methods. In: Brozek J, Henschel A, editors. Techniques for Measuring Body Composition. Washington, DC: National Academy of Sciences; 1961. p. 223-44.
* Brozek J, Grande F, Anderson JT, Keys A. Densitometric analysis of body composition: revision of some quantitative assumptions. Ann N Y Acad Sci. 1963;110:113-40.
* Deurenberg P, Yap M, van Staveren WA. Body mass index and percent body fat: a meta analysis among different ethnic groups. Int J Obes Relat Metab Disord. 1998;22(12):1164-71.

# Results

Out of these models, the "Two-Compartment" model (applying the standard Siri 1961 density equation directly) and the "BMI Model" seem to give the most reasonable results. The Two-Compartment model avoids the circular density→BF%→density pipeline used by the Brozek and Siri models.

The "Brozek" and "Siri" models break down when values are way outside normal human weights and heights (other models must be used for infants, dissoluted devourers, and blobs, supposedly).

The classification is not meant to fat or thin shame anyone (real or imagined characters), but is the standard
classification that WHO uses (see https://en.wikipedia.org/wiki/Body_mass_index#Categories).

For the BMI, Brozek and Siri models, the estimated proportions of fat/water/protein/mineral/other are included.

Outside "normal" ranges for humans, some of the formulas that calculate BMI give strange results, regarding
fat content. Currently the ratio of fat to other substances is clamped between 0 and 1, to not give non-sensical
results.

| m(kg) | h(m) | CDDA(L) | Simple(L) | BMI(L) | Brozek(L) | Siri(L) | 2Comp(L) | Category          |
|-------|------|---------|-----------|--------|-----------|---------|----------|-------------------|
|    25 | 0.55 |    2.17 |     23.18 |  27.78 |     27.45 |   27.78 |    27.76 | Obese (Class III) |
|    25 | 0.70 |    4.48 |     23.22 |  25.54 |     25.34 |   25.50 |    25.56 | Obese (Class III) |
|    25 | 1.00 |   13.06 |     23.30 |  23.68 |     23.59 |   23.60 |    23.74 |    Overweight     |
|    25 | 1.22 |   23.72 |     23.37 |  23.09 |     23.04 |   23.01 |    23.17 | Moderate thinness |
|    25 | 1.50 |   44.08 |     23.44 |  22.68 |     22.66 |   22.64 |    22.77 |  Severe thinness  |
|    25 | 1.62 |   55.53 |     23.48 |  22.64 |     22.64 |   22.64 |    22.73 |  Severe thinness  |
|    25 | 1.75 |   70.00 |     23.51 |  22.64 |     22.64 |   22.64 |    22.73 |  Severe thinness  |
|    25 | 2.00 |  104.49 |     23.59 |  22.64 |     22.64 |   22.64 |    22.73 |  Severe thinness  |
|    25 | 2.27 |  152.78 |     23.66 |  22.64 |     22.64 |   22.64 |    22.73 |  Severe thinness  |
|    25 | 2.72 |  262.84 |     23.79 |  22.64 |     22.64 |   22.64 |    22.73 |  Severe thinness  |
|    25 | 2.80 |  286.72 |     23.82 |  22.64 |     22.64 |   22.64 |    22.73 |  Severe thinness  |

| m(kg) | h(m) | CDDA(L) | Simple(L) | BMI(L) | Brozek(L) | Siri(L) | 2Comp(L) | Category          |
|-------|------|---------|-----------|--------|-----------|---------|----------|-------------------|
|    40 | 0.55 |    2.17 |     37.31 |  44.44 |     43.92 |   44.44 |    44.41 | Obese (Class III) |
|    40 | 0.70 |    4.48 |     37.38 |  44.36 |     43.83 |   44.35 |    44.32 | Obese (Class III) |
|    40 | 1.00 |   13.06 |     37.51 |  39.60 |     39.36 |   39.51 |    39.67 | Obese (Class III) |
|    40 | 1.22 |   23.72 |     37.61 |  38.10 |     37.95 |   37.99 |    38.20 |    Overweight     |
|    40 | 1.50 |   44.08 |     37.74 |  37.06 |     36.98 |   36.93 |    37.18 |   Mild thinness   |
|    40 | 1.62 |   55.53 |     37.80 |  36.77 |     36.70 |   36.63 |    36.90 |  Severe thinness  |
|    40 | 1.75 |   70.00 |     37.86 |  36.52 |     36.47 |   36.38 |    36.65 |  Severe thinness  |
|    40 | 2.00 |  104.49 |     37.97 |  36.22 |     36.22 |   36.22 |    36.36 |  Severe thinness  |
|    40 | 2.27 |  152.78 |     38.10 |  36.22 |     36.22 |   36.22 |    36.36 |  Severe thinness  |
|    40 | 2.72 |  262.84 |     38.31 |  36.22 |     36.22 |   36.22 |    36.36 |  Severe thinness  |
|    40 | 2.80 |  286.72 |     38.34 |  36.22 |     36.22 |   36.22 |    36.36 |  Severe thinness  |

| m(kg) | h(m) | CDDA(L) | Simple(L) | BMI(L) | Brozek(L) | Siri(L) | 2Comp(L) | Category          |
|-------|------|---------|-----------|--------|-----------|---------|----------|-------------------|
|    55 | 0.55 |    2.17 |     51.60 |  61.11 |     60.38 |   61.11 |    61.06 | Obese (Class III) |
|    55 | 0.70 |    4.48 |     51.70 |  61.11 |     60.38 |   61.11 |    61.06 | Obese (Class III) |
|    55 | 1.00 |   13.06 |     51.89 |  56.80 |     56.34 |   56.73 |    56.85 | Obese (Class III) |
|    55 | 1.22 |   23.72 |     52.02 |  53.97 |     53.67 |   53.84 |    54.07 | Obese (Class II)  |
|    55 | 1.50 |   44.08 |     52.20 |  52.00 |     51.83 |   51.84 |    52.15 |      Normal       |
|    55 | 1.62 |   55.53 |     52.28 |  51.45 |     51.31 |   51.28 |    51.61 |      Normal       |
|    55 | 1.75 |   70.00 |     52.36 |  50.98 |     50.87 |   50.80 |    51.15 |   Mild thinness   |
|    55 | 2.00 |  104.49 |     52.52 |  50.32 |     50.25 |   50.13 |    50.51 |  Severe thinness  |
|    55 | 2.27 |  152.78 |     52.70 |  49.84 |     49.80 |   49.80 |    50.03 |  Severe thinness  |
|    55 | 2.72 |  262.84 |     52.99 |  49.80 |     49.80 |   49.80 |    50.00 |  Severe thinness  |
|    55 | 2.80 |  286.72 |     53.04 |  49.80 |     49.80 |   49.80 |    50.00 |  Severe thinness  |

| m(kg) | h(m) | CDDA(L) | Simple(L) | BMI(L) | Brozek(L) | Siri(L) | 2Comp(L) | Category          |
|-------|------|---------|-----------|--------|-----------|---------|----------|-------------------|
|    70 | 0.55 |    2.17 |     66.05 |  77.78 |     76.85 |   77.78 |    77.72 | Obese (Class III) |
|    70 | 0.70 |    4.48 |     66.17 |  77.78 |     76.85 |   77.78 |    77.72 | Obese (Class III) |
|    70 | 1.00 |   13.06 |     66.41 |  75.30 |     74.52 |   75.25 |    75.29 | Obese (Class III) |
|    70 | 1.22 |   23.72 |     66.59 |  70.70 |     70.21 |   70.58 |    70.79 | Obese (Class III) |
|    70 | 1.50 |   44.08 |     66.82 |  67.52 |     67.21 |   67.34 |    67.68 |  Obese (Class I)  |
|    70 | 1.62 |   55.53 |     66.92 |  66.63 |     66.38 |   66.43 |    66.81 |    Overweight     |
|    70 | 1.75 |   70.00 |     67.02 |  65.87 |     65.66 |   65.66 |    66.06 |      Normal       |
|    70 | 2.00 |  104.49 |     67.23 |  64.80 |     64.66 |   64.57 |    65.01 |   Mild thinness   |
|    70 | 2.27 |  152.78 |     67.45 |  64.01 |     63.92 |   63.77 |    64.25 |  Severe thinness  |
|    70 | 2.72 |  262.84 |     67.83 |  63.39 |     63.39 |   63.39 |    63.64 |  Severe thinness  |
|    70 | 2.80 |  286.72 |     67.90 |  63.39 |     63.39 |   63.39 |    63.64 |  Severe thinness  |

| m(kg) | h(m) | CDDA(L) | Simple(L) | BMI(L) | Brozek(L) | Siri(L) | 2Comp(L) | Category          |
|-------|------|---------|-----------|--------|-----------|---------|----------|-------------------|
|    85 | 0.55 |    2.17 |     80.64 |  94.44 |     93.32 |   94.44 |    94.37 | Obese (Class III) |
|    85 | 0.70 |    4.48 |     80.79 |  94.44 |     93.32 |   94.44 |    94.37 | Obese (Class III) |
|    85 | 1.00 |   13.06 |     81.08 |  94.44 |     93.32 |   94.44 |    94.37 | Obese (Class III) |
|    85 | 1.22 |   23.72 |     81.30 |  88.30 |     87.55 |   88.19 |    88.36 | Obese (Class III) |
|    85 | 1.50 |   44.08 |     81.58 |  83.61 |     83.14 |   83.41 |    83.77 | Obese (Class II)  |
|    85 | 1.62 |   55.53 |     81.70 |  82.30 |     81.91 |   82.08 |    82.48 |  Obese (Class I)  |
|    85 | 1.75 |   70.00 |     81.84 |  81.17 |     80.85 |   80.94 |    81.38 |    Overweight     |
|    85 | 2.00 |  104.49 |     82.09 |  79.59 |     79.37 |   79.33 |    79.84 |      Normal       |
|    85 | 2.27 |  152.78 |     82.36 |  78.44 |     78.28 |   78.15 |    78.71 | Moderate thinness |
|    85 | 2.72 |  262.84 |     82.83 |  77.22 |     77.14 |   76.97 |    77.52 |  Severe thinness  |
|    85 | 2.80 |  286.72 |     82.91 |  77.06 |     76.99 |   76.97 |    77.36 |  Severe thinness  |

| m(kg) | h(m) | CDDA(L) | Simple(L) | BMI(L) | Brozek(L) | Siri(L) | 2Comp(L) | Category          |
|-------|------|---------|-----------|--------|-----------|---------|----------|-------------------|
|   100 | 0.55 |    2.17 |     95.37 | 111.11 |    109.79 |  111.11 |   111.02 | Obese (Class III) |
|   100 | 0.70 |    4.48 |     95.54 | 111.11 |    109.79 |  111.11 |   111.02 | Obese (Class III) |
|   100 | 1.00 |   13.06 |     95.90 | 111.11 |    109.79 |  111.11 |   111.02 | Obese (Class III) |
|   100 | 1.22 |   23.72 |     96.16 | 106.76 |    105.71 |  106.69 |   106.77 | Obese (Class III) |
|   100 | 1.50 |   44.08 |     96.49 | 100.26 |     99.60 |  100.07 |   100.41 | Obese (Class III) |
|   100 | 1.62 |   55.53 |     96.63 |  98.45 |     97.90 |   98.23 |    98.64 | Obese (Class II)  |
|   100 | 1.75 |   70.00 |     96.79 |  96.89 |     96.43 |   96.64 |    97.11 |  Obese (Class I)  |
|   100 | 2.00 |  104.49 |     97.09 |  94.71 |     94.38 |   94.42 |    94.97 |    Overweight     |
|   100 | 2.27 |  152.78 |     97.42 |  93.11 |     92.88 |   92.79 |    93.41 |      Normal       |
|   100 | 2.72 |  262.84 |     97.97 |  91.43 |     91.30 |   91.08 |    91.76 |  Severe thinness  |
|   100 | 2.80 |  286.72 |     98.07 |  91.21 |     91.09 |   90.86 |    91.55 |  Severe thinness  |

| m(kg) | h(m) | CDDA(L) | Simple(L) | BMI(L) | Brozek(L) | Siri(L) | 2Comp(L) | Category          |
|-------|------|---------|-----------|--------|-----------|---------|----------|-------------------|
|   115 | 0.55 |    2.17 |    110.22 | 127.78 |    126.26 |  127.78 |   127.68 | Obese (Class III) |
|   115 | 0.70 |    4.48 |    110.43 | 127.78 |    126.26 |  127.78 |   127.68 | Obese (Class III) |
|   115 | 1.00 |   13.06 |    110.84 | 127.78 |    126.26 |  127.78 |   127.68 | Obese (Class III) |
|   115 | 1.22 |   23.72 |    111.14 | 126.09 |    124.67 |  126.06 |   126.03 | Obese (Class III) |
|   115 | 1.50 |   44.08 |    111.53 | 117.49 |    116.60 |  117.31 |   117.62 | Obese (Class III) |
|   115 | 1.62 |   55.53 |    111.69 | 115.10 |    114.35 |  114.87 |   115.27 | Obese (Class III) |
|   115 | 1.75 |   70.00 |    111.87 | 113.04 |    112.41 |  112.78 |   113.26 | Obese (Class II)  |
|   115 | 2.00 |  104.49 |    112.22 | 110.15 |    109.69 |  109.84 |   110.43 |    Overweight     |
|   115 | 2.27 |  152.78 |    112.60 | 108.03 |    107.71 |  107.68 |   108.36 |      Normal       |
|   115 | 2.72 |  262.84 |    113.25 | 105.81 |    105.62 |  105.42 |   106.18 |  Severe thinness  |
|   115 | 2.80 |  286.72 |    113.36 | 105.52 |    105.35 |  105.13 |   105.90 |  Severe thinness  |

| m(kg) | h(m) | CDDA(L) | Simple(L) | BMI(L) | Brozek(L) | Siri(L) | 2Comp(L) | Category          |
|-------|------|---------|-----------|--------|-----------|---------|----------|-------------------|
|   130 | 0.55 |    2.17 |    125.20 | 144.44 |    142.73 |  144.44 |   144.33 | Obese (Class III) |
|   130 | 0.70 |    4.48 |    125.43 | 144.44 |    142.73 |  144.44 |   144.33 | Obese (Class III) |
|   130 | 1.00 |   13.06 |    125.90 | 144.44 |    142.73 |  144.44 |   144.33 | Obese (Class III) |
|   130 | 1.22 |   23.72 |    126.24 | 144.44 |    142.73 |  144.44 |   144.33 | Obese (Class III) |
|   130 | 1.50 |   44.08 |    126.69 | 135.30 |    134.13 |  135.14 |   135.38 | Obese (Class III) |
|   130 | 1.62 |   55.53 |    126.88 | 132.23 |    131.26 |  132.02 |   132.39 | Obese (Class III) |
|   130 | 1.75 |   70.00 |    127.08 | 129.60 |    128.78 |  129.34 |   129.81 | Obese (Class III) |
|   130 | 2.00 |  104.49 |    127.48 | 125.91 |    125.31 |  125.58 |   126.19 |  Obese (Class I)  |
|   130 | 2.27 |  152.78 |    127.92 | 123.20 |    122.77 |  122.83 |   123.55 |    Overweight     |
|   130 | 2.72 |  262.84 |    128.65 | 120.36 |    120.10 |  119.94 |   120.77 |   Mild thinness   |
|   130 | 2.80 |  286.72 |    128.78 | 119.99 |    119.76 |  119.56 |   120.41 | Moderate thinness |

| m(kg) | h(m) | CDDA(L) | Simple(L) | BMI(L) | Brozek(L) | Siri(L) | 2Comp(L) | Category          |
|-------|------|---------|-----------|--------|-----------|---------|----------|-------------------|
|   145 | 0.55 |    2.17 |    140.28 | 161.11 |    159.20 |  161.11 |   160.99 | Obese (Class III) |
|   145 | 0.70 |    4.48 |    140.55 | 161.11 |    159.20 |  161.11 |   160.99 | Obese (Class III) |
|   145 | 1.00 |   13.06 |    141.07 | 161.11 |    159.20 |  161.11 |   160.99 | Obese (Class III) |
|   145 | 1.22 |   23.72 |    141.46 | 161.11 |    159.20 |  161.11 |   160.99 | Obese (Class III) |
|   145 | 1.50 |   44.08 |    141.96 | 153.67 |    152.21 |  153.54 |   153.70 | Obese (Class III) |
|   145 | 1.62 |   55.53 |    142.17 | 149.86 |    148.63 |  149.66 |   149.98 | Obese (Class III) |
|   145 | 1.75 |   70.00 |    142.41 | 146.59 |    145.55 |  146.33 |   146.77 | Obese (Class III) |
|   145 | 2.00 |  104.49 |    142.86 | 141.99 |    141.23 |  141.65 |   142.27 | Obese (Class II)  |
|   145 | 2.27 |  152.78 |    143.34 | 138.63 |    138.07 |  138.23 |   138.99 |    Overweight     |
|   145 | 2.72 |  262.84 |    144.17 | 135.09 |    134.75 |  134.63 |   135.52 |      Normal       |
|   145 | 2.80 |  286.72 |    144.31 | 134.63 |    134.32 |  134.16 |   135.08 |   Mild thinness   |

| m(kg) | h(m) | CDDA(L) | Simple(L) | BMI(L) | Brozek(L) | Siri(L) | 2Comp(L) | Category          |
|-------|------|---------|-----------|--------|-----------|---------|----------|-------------------|
|   160 | 0.55 |    2.17 |    155.47 | 177.78 |    175.67 |  177.78 |   177.64 | Obese (Class III) |
|   160 | 0.70 |    4.48 |    155.76 | 177.78 |    175.67 |  177.78 |   177.64 | Obese (Class III) |
|   160 | 1.00 |   13.06 |    156.35 | 177.78 |    175.67 |  177.78 |   177.64 | Obese (Class III) |
|   160 | 1.22 |   23.72 |    156.78 | 177.78 |    175.67 |  177.78 |   177.64 | Obese (Class III) |
|   160 | 1.50 |   44.08 |    157.33 | 172.62 |    170.81 |  172.52 |   172.59 | Obese (Class III) |
|   160 | 1.62 |   55.53 |    157.57 | 167.98 |    166.46 |  167.80 |   168.05 | Obese (Class III) |
|   160 | 1.75 |   70.00 |    157.83 | 163.99 |    162.71 |  163.75 |   164.15 | Obese (Class III) |
|   160 | 2.00 |  104.49 |    158.33 | 158.39 |    157.45 |  158.05 |   158.67 | Obese (Class III) |
|   160 | 2.27 |  152.78 |    158.88 | 154.30 |    153.61 |  153.88 |   154.67 |  Obese (Class I)  |
|   160 | 2.72 |  262.84 |    159.79 | 149.99 |    149.56 |  149.50 |   150.45 |      Normal       |
|   160 | 2.80 |  286.72 |    159.96 | 149.43 |    149.04 |  148.93 |   149.90 |      Normal       |

| m(kg) | h(m) | CDDA(L) | Simple(L) | BMI(L) | Brozek(L) | Siri(L) | 2Comp(L) | Category          |
|-------|------|---------|-----------|--------|-----------|---------|----------|-------------------|
|   175 | 0.55 |    2.17 |    170.75 | 194.44 |    192.13 |  194.44 |   194.29 | Obese (Class III) |
|   175 | 0.70 |    4.48 |    171.07 | 194.44 |    192.13 |  194.44 |   194.29 | Obese (Class III) |
|   175 | 1.00 |   13.06 |    171.72 | 194.44 |    192.13 |  194.44 |   194.29 | Obese (Class III) |
|   175 | 1.22 |   23.72 |    172.19 | 194.44 |    192.13 |  194.44 |   194.29 | Obese (Class III) |
|   175 | 1.50 |   44.08 |    172.80 | 192.13 |    189.96 |  192.09 |   192.03 | Obese (Class III) |
|   175 | 1.62 |   55.53 |    173.07 | 186.58 |    184.75 |  186.44 |   186.60 | Obese (Class III) |
|   175 | 1.75 |   70.00 |    173.35 | 181.81 |    180.27 |  181.59 |   181.93 | Obese (Class III) |
|   175 | 2.00 |  104.49 |    173.91 | 175.11 |    173.97 |  174.77 |   175.38 | Obese (Class III) |
|   175 | 2.27 |  152.78 |    174.51 | 170.22 |    169.37 |  169.79 |   170.59 |  Obese (Class I)  |
|   175 | 2.72 |  262.84 |    175.52 | 165.07 |    164.53 |  164.55 |   165.55 |      Normal       |
|   175 | 2.80 |  286.72 |    175.70 | 164.40 |    163.91 |  163.87 |   164.89 |      Normal       |

| m(kg) | h(m) | CDDA(L) | Simple(L) | BMI(L) | Brozek(L) | Siri(L) | 2Comp(L) | Category          |
|-------|------|---------|-----------|--------|-----------|---------|----------|-------------------|
|   190 | 0.55 |    2.17 |    186.11 | 211.11 |    208.60 |  211.11 |   210.95 | Obese (Class III) |
|   190 | 0.70 |    4.48 |    186.46 | 211.11 |    208.60 |  211.11 |   210.95 | Obese (Class III) |
|   190 | 1.00 |   13.06 |    187.17 | 211.11 |    208.60 |  211.11 |   210.95 | Obese (Class III) |
|   190 | 1.22 |   23.72 |    187.69 | 211.11 |    208.60 |  211.11 |   210.95 | Obese (Class III) |
|   190 | 1.50 |   44.08 |    188.36 | 211.11 |    208.60 |  211.11 |   210.95 | Obese (Class III) |
|   190 | 1.62 |   55.53 |    188.64 | 205.68 |    203.50 |  205.58 |   205.63 | Obese (Class III) |
|   190 | 1.75 |   70.00 |    188.96 | 200.06 |    198.22 |  199.86 |   200.13 | Obese (Class III) |
|   190 | 2.00 |  104.49 |    189.56 | 192.16 |    190.80 |  191.83 |   192.40 | Obese (Class III) |
|   190 | 2.27 |  152.78 |    190.22 | 186.39 |    185.38 |  185.95 |   186.76 | Obese (Class II)  |
|   190 | 2.72 |  262.84 |    191.32 | 180.31 |    179.67 |  179.77 |   180.81 |    Overweight     |
|   190 | 2.80 |  286.72 |    191.52 | 179.53 |    178.93 |  178.97 |   180.04 |      Normal       |

| m(kg) | h(m) | CDDA(L) | Simple(L) | BMI(L) | Brozek(L) | Siri(L) | 2Comp(L) | Category          |
|-------|------|---------|-----------|--------|-----------|---------|----------|-------------------|
|   205 | 0.55 |    2.17 |    201.54 | 227.78 |    225.07 |  227.78 |   227.60 | Obese (Class III) |
|   205 | 0.70 |    4.48 |    201.92 | 227.78 |    225.07 |  227.78 |   227.60 | Obese (Class III) |
|   205 | 1.00 |   13.06 |    202.69 | 227.78 |    225.07 |  227.78 |   227.60 | Obese (Class III) |
|   205 | 1.22 |   23.72 |    203.25 | 227.78 |    225.07 |  227.78 |   227.60 | Obese (Class III) |
|   205 | 1.50 |   44.08 |    203.98 | 227.78 |    225.07 |  227.78 |   227.60 | Obese (Class III) |
|   205 | 1.62 |   55.53 |    204.29 | 225.26 |    222.71 |  225.22 |   225.14 | Obese (Class III) |
|   205 | 1.75 |   70.00 |    204.63 | 218.72 |    216.56 |  218.56 |   218.74 | Obese (Class III) |
|   205 | 2.00 |  104.49 |    205.29 | 209.53 |    207.93 |  209.21 |   209.74 | Obese (Class III) |
|   205 | 2.27 |  152.78 |    206.00 | 202.81 |    201.61 |  202.37 |   203.17 | Obese (Class II)  |
|   205 | 2.72 |  262.84 |    207.21 | 195.74 |    194.97 |  195.17 |   196.25 |    Overweight     |
|   205 | 2.80 |  286.72 |    207.42 | 194.82 |    194.11 |  194.24 |   195.36 |    Overweight     |

