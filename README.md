# Human Body Volume Calculation (Mostly for Cataclysm: Dark Days Ahead)

This repository contains a script that uses five different models to estimate the volume of a human body.

There is no guarantee that the results are accurate, or can be relied upon in any medical context, or even useful in a gaming context.

Also, this has been an unreasonable amount of work just to prove a point, and is unnecessarily detailed.

Anyway, To run the script, you need Python3 and matplotlib (just comment out the plotting business, if you
don't want to install matplotlib)

# Models

There are a couple of assumptions here:

* Volume = Weight / Density
* The larger the BMI of a human body, the larger ratio of fat to other components

The material composition of average humans is roughly

* 12% fat
* 65% water
* 20% protein
* 3% other stuff

The densities of each respective material are assumed to be

* Fat: 0.9 g/cm³ (kg/L)
* Water: 1.0 g/cm³ (kg/L)
* Protein: 1.35 g/cm³ (kg/L)
* Other: 1.0 g/cm³ (kg/L)

There are five models provided:

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

This model also takes the proportion of fat vs. other components into account, and uses the same capping strategy as above.

# Graph over relations between models and parameters

![3D Plot](Figure_1.png)

The green lines are the original CDDA volume calculation (independent of weight) results for various heighs.

The red lines are the BMI model results.

The blue lines are the Brozek model results.

The yellow lines are the Siri model results.

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

# Results

Out of these models, the pure "BMI Model" seems to give reasonable results, with some strange results at the
extremes, depending on the density calculations assuming most of the body then consists of fat.

The "Brozek" and "Siri" models break down when values are way outside normal human weights and heights (other models must be used for infants, dissoluted devourers, and blobs, supposedly).

The classification is not meant to fat or thin shame anyone (real or imagined characters), but is the standard
classification that WHO uses (see https://en.wikipedia.org/wiki/Body_mass_index#Categories).

For the BMI, Brozek and Siri models, the estimated proportions of fat/water/protein/other are included. As quickly becomes obvious the formula for calculating this is not normalized to
give results within | 0 < > 1 |, which may be a source for the nonsensical results at the extremes.

| m(kg) | h(m) | CDDA(L) | Simple(L) | BMI(L) | BMI(P) fat/water/protein/other | Brozek(L) | Brozek(P) fat/water/protein/other | Siri(L) | Siri(P) fat/water/protein/other | Category          |
|-------|------|---------|-----------|--------|--------------------------------|-----------|-----------------------------------|---------|---------------------------------|-------------------|
|    25 | 0.55 |    2.17 |     23.18 |  27.79 | L:1.00 W:-0.00 P:-0.00 O:-0.00 |     27.48 |    L:0.94 W:0.04 P:0.01 O:0.00    |   27.79 | L:1.00 W:-0.00 P:-0.00 O:-0.00  | Obese (Class III) |
|    25 | 0.70 |    4.48 |     23.22 |  25.70 |  L:0.56 W:0.28 P:0.09 O:0.01   |     25.67 |    L:0.56 W:0.29 P:0.09 O:0.01    |   25.82 |   L:0.59 W:0.27 P:0.08 O:0.01   | Obese (Class III) |
|    25 | 1.00 |   13.06 |     23.30 |  24.05 |  L:0.20 W:0.52 P:0.16 O:0.02   |     24.29 |    L:0.25 W:0.48 P:0.15 O:0.02    |   24.32 |   L:0.26 W:0.48 P:0.15 O:0.02   |    Overweight     |
|    25 | 1.22 |   23.72 |     23.37 |  23.55 |  L:0.09 W:0.59 P:0.18 O:0.03   |     23.87 |    L:0.16 W:0.54 P:0.17 O:0.03    |   23.87 |   L:0.16 W:0.54 P:0.17 O:0.03   | Moderate thinness |
|    25 | 1.50 |   44.08 |     23.44 |  23.20 |  L:0.01 W:0.64 P:0.20 O:0.03   |     23.59 |    L:0.10 W:0.59 P:0.18 O:0.03    |   23.57 |   L:0.09 W:0.59 P:0.18 O:0.03   |  Severe thinness  |
|    25 | 1.62 |   55.53 |     23.48 |  23.10 |  L:-0.01 W:0.66 P:0.20 O:0.03  |     23.51 |    L:0.08 W:0.60 P:0.18 O:0.03    |   23.48 |   L:0.07 W:0.60 P:0.19 O:0.03   |  Severe thinness  |
|    25 | 1.75 |   70.00 |     23.51 |  23.02 |  L:-0.03 W:0.67 P:0.21 O:0.03  |     23.45 |    L:0.07 W:0.61 P:0.19 O:0.03    |   23.41 |   L:0.06 W:0.61 P:0.19 O:0.03   |  Severe thinness  |
|    25 | 2.00 |  104.49 |     23.59 |  22.90 |  L:-0.06 W:0.69 P:0.21 O:0.03  |     23.35 |    L:0.04 W:0.62 P:0.19 O:0.03    |   23.31 |   L:0.03 W:0.63 P:0.19 O:0.03   |  Severe thinness  |
|    25 | 2.27 |  152.78 |     23.66 |  22.82 |  L:-0.08 W:0.70 P:0.22 O:0.03  |     23.29 |    L:0.03 W:0.63 P:0.19 O:0.03    |   23.24 |   L:0.02 W:0.64 P:0.20 O:0.03   |  Severe thinness  |
|    25 | 2.72 |  262.84 |     23.79 |  22.73 |  L:-0.10 W:0.71 P:0.22 O:0.03  |     23.21 |    L:0.01 W:0.64 P:0.20 O:0.03    |   23.16 |   L:0.00 W:0.65 P:0.20 O:0.03   |  Severe thinness  |
|    25 | 2.80 |  286.72 |     23.82 |  22.72 |  L:-0.10 W:0.72 P:0.22 O:0.03  |     23.21 |    L:0.01 W:0.64 P:0.20 O:0.03    |   23.15 |  L:-0.00 W:0.65 P:0.20 O:0.03   |  Severe thinness  |

| m(kg) | h(m) | CDDA(L) | Simple(L) | BMI(L) | BMI(P) fat/water/protein/other | Brozek(L) | Brozek(P) fat/water/protein/other | Siri(L) | Siri(P) fat/water/protein/other | Category          |
|-------|------|---------|-----------|--------|--------------------------------|-----------|-----------------------------------|---------|---------------------------------|-------------------|
|    40 | 0.55 |    2.17 |     37.31 |  50.06 | L:1.69 W:-0.45 P:-0.14 O:-0.02 |     49.10 |  L:1.58 W:-0.38 P:-0.12 O:-0.02   |   50.09 | L:1.70 W:-0.45 P:-0.14 O:-0.02  | Obese (Class III) |
|    40 | 0.70 |    4.48 |     37.38 |  44.36 |  L:0.99 W:0.01 P:0.00 O:0.00   |     43.87 |    L:0.93 W:0.05 P:0.01 O:0.00    |   44.36 |   L:0.99 W:0.01 P:0.00 O:0.00   | Obese (Class III) |
|    40 | 1.00 |   13.06 |     37.51 |  39.99 |  L:0.41 W:0.38 P:0.12 O:0.02   |     40.11 |    L:0.43 W:0.37 P:0.11 O:0.02    |   40.27 |   L:0.45 W:0.36 P:0.11 O:0.02   | Obese (Class III) |
|    40 | 1.22 |   23.72 |     37.61 |  38.67 |  L:0.23 W:0.50 P:0.15 O:0.02   |     39.01 |    L:0.28 W:0.47 P:0.14 O:0.02    |   39.08 |   L:0.29 W:0.46 P:0.14 O:0.02   |    Overweight     |
|    40 | 1.50 |   44.08 |     37.74 |  37.77 |  L:0.10 W:0.58 P:0.18 O:0.03   |     38.28 |    L:0.17 W:0.54 P:0.17 O:0.02    |   38.28 |   L:0.17 W:0.54 P:0.17 O:0.02   |   Mild thinness   |
|    40 | 1.62 |   55.53 |     37.80 |  37.52 |  L:0.07 W:0.61 P:0.19 O:0.03   |     38.07 |    L:0.14 W:0.56 P:0.17 O:0.03    |   38.06 |   L:0.14 W:0.56 P:0.17 O:0.03   |  Severe thinness  |
|    40 | 1.75 |   70.00 |     37.86 |  37.31 |  L:0.04 W:0.63 P:0.19 O:0.03   |     37.90 |    L:0.12 W:0.57 P:0.18 O:0.03    |   37.87 |   L:0.12 W:0.57 P:0.18 O:0.03   |  Severe thinness  |
|    40 | 2.00 |  104.49 |     37.97 |  37.01 |  L:-0.01 W:0.65 P:0.20 O:0.03  |     37.66 |    L:0.09 W:0.59 P:0.18 O:0.03    |   37.61 |   L:0.08 W:0.60 P:0.18 O:0.03   |  Severe thinness  |
|    40 | 2.27 |  152.78 |     38.10 |  36.79 |  L:-0.04 W:0.67 P:0.21 O:0.03  |     37.48 |    L:0.06 W:0.61 P:0.19 O:0.03    |   37.42 |   L:0.05 W:0.62 P:0.19 O:0.03   |  Severe thinness  |
|    40 | 2.72 |  262.84 |     38.31 |  36.56 |  L:-0.07 W:0.70 P:0.21 O:0.03  |     37.30 |    L:0.04 W:0.63 P:0.19 O:0.03    |   37.23 |   L:0.02 W:0.63 P:0.20 O:0.03   |  Severe thinness  |
|    40 | 2.80 |  286.72 |     38.34 |  36.53 |  L:-0.07 W:0.70 P:0.21 O:0.03  |     37.28 |    L:0.03 W:0.63 P:0.19 O:0.03    |   37.20 |   L:0.02 W:0.64 P:0.20 O:0.03   |  Severe thinness  |

| m(kg) | h(m) | CDDA(L) | Simple(L) | BMI(L) | BMI(P) fat/water/protein/other | Brozek(L) | Brozek(P) fat/water/protein/other | Siri(L) | Siri(P) fat/water/protein/other | Category          |
|-------|------|---------|-----------|--------|--------------------------------|-----------|-----------------------------------|---------|---------------------------------|-------------------|
|    55 | 0.55 |    2.17 |     51.60 |  77.17 | L:2.38 W:-0.90 P:-0.28 O:-0.04 |     75.77 |  L:2.27 W:-0.83 P:-0.25 O:-0.04   |   77.97 | L:2.45 W:-0.94 P:-0.29 O:-0.04  | Obese (Class III) |
|    55 | 0.70 |    4.48 |     51.70 |  65.67 | L:1.41 W:-0.27 P:-0.08 O:-0.01 |     64.54 |  L:1.31 W:-0.20 P:-0.06 O:-0.01   |   65.61 | L:1.41 W:-0.27 P:-0.08 O:-0.01  | Obese (Class III) |
|    55 | 1.00 |   13.06 |     51.89 |  57.11 |  L:0.62 W:0.25 P:0.08 O:0.01   |     56.95 |    L:0.60 W:0.26 P:0.08 O:0.01    |   57.32 |   L:0.64 W:0.23 P:0.07 O:0.01   | Obese (Class III) |
|    55 | 1.22 |   23.72 |     52.02 |  54.56 |  L:0.37 W:0.41 P:0.13 O:0.02   |     54.80 |    L:0.39 W:0.40 P:0.12 O:0.02    |   54.99 |   L:0.41 W:0.38 P:0.12 O:0.02   | Obese (Class II)  |
|    55 | 1.50 |   44.08 |     52.20 |  52.84 |  L:0.19 W:0.52 P:0.16 O:0.02   |     53.37 |    L:0.25 W:0.49 P:0.15 O:0.02    |   53.44 |   L:0.26 W:0.48 P:0.15 O:0.02   |      Normal       |
|    55 | 1.62 |   55.53 |     52.28 |  52.36 |  L:0.15 W:0.56 P:0.17 O:0.03   |     52.98 |    L:0.21 W:0.51 P:0.16 O:0.02    |   53.02 |   L:0.21 W:0.51 P:0.16 O:0.02   |      Normal       |
|    55 | 1.75 |   70.00 |     52.36 |  51.96 |  L:0.10 W:0.58 P:0.18 O:0.03   |     52.65 |    L:0.18 W:0.54 P:0.16 O:0.02    |   52.66 |   L:0.18 W:0.54 P:0.16 O:0.02   |   Mild thinness   |
|    55 | 2.00 |  104.49 |     52.52 |  51.39 |  L:0.05 W:0.62 P:0.19 O:0.03   |     52.19 |    L:0.13 W:0.57 P:0.17 O:0.03    |   52.16 |   L:0.12 W:0.57 P:0.18 O:0.03   |  Severe thinness  |
|    55 | 2.27 |  152.78 |     52.70 |  50.98 |  L:0.00 W:0.65 P:0.20 O:0.03   |     51.85 |    L:0.09 W:0.59 P:0.18 O:0.03    |   51.80 |   L:0.09 W:0.59 P:0.18 O:0.03   |  Severe thinness  |
|    55 | 2.72 |  262.84 |     52.99 |  50.54 |  L:-0.04 W:0.68 P:0.21 O:0.03  |     51.50 |    L:0.06 W:0.61 P:0.19 O:0.03    |   51.42 |   L:0.05 W:0.62 P:0.19 O:0.03   |  Severe thinness  |
|    55 | 2.80 |  286.72 |     53.04 |  50.49 |  L:-0.05 W:0.68 P:0.21 O:0.03  |     51.46 |    L:0.05 W:0.62 P:0.19 O:0.03    |   51.37 |   L:0.04 W:0.62 P:0.19 O:0.03   |  Severe thinness  |

| m(kg) | h(m) | CDDA(L) | Simple(L) | BMI(L) | BMI(P) fat/water/protein/other | Brozek(L) | Brozek(P) fat/water/protein/other | Siri(L) | Siri(P) fat/water/protein/other | Category          |
|-------|------|---------|-----------|--------|--------------------------------|-----------|-----------------------------------|---------|---------------------------------|-------------------|
|    70 | 0.55 |    2.17 |     66.05 | 109.73 | L:3.07 W:-1.35 P:-0.41 O:-0.06 |    108.88 |  L:3.02 W:-1.31 P:-0.40 O:-0.06   |  113.06 | L:3.26 W:-1.47 P:-0.45 O:-0.07  | Obese (Class III) |
|    70 | 0.70 |    4.48 |     66.17 |  89.81 | L:1.84 W:-0.55 P:-0.17 O:-0.03 |     88.04 |  L:1.72 W:-0.47 P:-0.14 O:-0.02   |   89.98 | L:1.85 W:-0.55 P:-0.17 O:-0.03  | Obese (Class III) |
|    70 | 1.00 |   13.06 |     66.41 |  75.45 |  L:0.83 W:0.11 P:0.03 O:0.01   |     74.86 |    L:0.78 W:0.14 P:0.04 O:0.01    |   75.55 |   L:0.84 W:0.11 P:0.03 O:0.00   | Obese (Class III) |
|    70 | 1.22 |   23.72 |     66.59 |  71.24 |  L:0.51 W:0.32 P:0.10 O:0.01   |     71.25 |    L:0.51 W:0.32 P:0.10 O:0.01    |   71.63 |   L:0.54 W:0.30 P:0.09 O:0.01   | Obese (Class III) |
|    70 | 1.50 |   44.08 |     66.82 |  68.41 |  L:0.29 W:0.46 P:0.14 O:0.02   |     68.89 |    L:0.32 W:0.44 P:0.14 O:0.02    |   69.06 |   L:0.34 W:0.43 P:0.13 O:0.02   |  Obese (Class I)  |
|    70 | 1.62 |   55.53 |     66.92 |  67.64 |  L:0.23 W:0.50 P:0.15 O:0.02   |     68.25 |    L:0.27 W:0.47 P:0.15 O:0.02    |   68.36 |   L:0.28 W:0.47 P:0.14 O:0.02   |    Overweight     |
|    70 | 1.75 |   70.00 |     67.02 |  66.97 |  L:0.17 W:0.54 P:0.17 O:0.02   |     67.70 |    L:0.23 W:0.50 P:0.15 O:0.02    |   67.77 |   L:0.24 W:0.50 P:0.15 O:0.02   |      Normal       |
|    70 | 2.00 |  104.49 |     67.23 |  66.05 |  L:0.10 W:0.59 P:0.18 O:0.03   |     66.94 |    L:0.17 W:0.54 P:0.17 O:0.02    |   66.95 |   L:0.17 W:0.54 P:0.17 O:0.02   |   Mild thinness   |
|    70 | 2.27 |  152.78 |     67.45 |  65.38 |  L:0.04 W:0.62 P:0.19 O:0.03   |     66.40 |    L:0.13 W:0.57 P:0.17 O:0.03    |   66.36 |   L:0.12 W:0.57 P:0.18 O:0.03   |  Severe thinness  |
|    70 | 2.72 |  262.84 |     67.83 |  64.67 |  L:-0.01 W:0.66 P:0.20 O:0.03  |     65.83 |    L:0.08 W:0.60 P:0.18 O:0.03    |   65.74 |   L:0.07 W:0.60 P:0.19 O:0.03   |  Severe thinness  |
|    70 | 2.80 |  286.72 |     67.90 |  64.58 |  L:-0.02 W:0.66 P:0.20 O:0.03  |     65.76 |    L:0.07 W:0.60 P:0.19 O:0.03    |   65.66 |   L:0.07 W:0.61 P:0.19 O:0.03   |  Severe thinness  |

| m(kg) | h(m) | CDDA(L) | Simple(L) | BMI(L) | BMI(P) fat/water/protein/other | Brozek(L) | Brozek(P) fat/water/protein/other | Siri(L) | Siri(P) fat/water/protein/other | Category          |
|-------|------|---------|-----------|--------|--------------------------------|-----------|-----------------------------------|---------|---------------------------------|-------------------|
|    85 | 0.55 |    2.17 |     80.64 | 148.50 | L:3.76 W:-1.79 P:-0.55 O:-0.08 |    150.40 |  L:3.84 W:-1.85 P:-0.57 O:-0.09   |  157.70 | L:4.15 W:-2.05 P:-0.63 O:-0.09  | Obese (Class III) |
|    85 | 0.70 |    4.48 |     80.79 | 117.02 | L:2.27 W:-0.82 P:-0.25 O:-0.04 |    114.80 |  L:2.15 W:-0.75 P:-0.23 O:-0.03   |  117.96 | L:2.31 W:-0.85 P:-0.26 O:-0.04  | Obese (Class III) |
|    85 | 1.00 |   13.06 |     81.08 |  95.04 | L:1.04 W:-0.02 P:-0.01 O:-0.00 |     93.92 |    L:0.97 W:0.02 P:0.01 O:0.00    |   95.02 | L:1.03 W:-0.02 P:-0.01 O:-0.00  | Obese (Class III) |
|    85 | 1.22 |   23.72 |     81.30 |  88.73 |  L:0.65 W:0.23 P:0.07 O:0.01   |     88.41 |    L:0.63 W:0.24 P:0.07 O:0.01    |   89.02 |   L:0.67 W:0.22 P:0.07 O:0.01   | Obese (Class III) |
|    85 | 1.50 |   44.08 |     81.58 |  84.50 |  L:0.38 W:0.40 P:0.12 O:0.02   |     84.84 |    L:0.40 W:0.39 P:0.12 O:0.02    |   85.14 |   L:0.42 W:0.38 P:0.12 O:0.02   | Obese (Class II)  |
|    85 | 1.62 |   55.53 |     81.70 |  83.35 |  L:0.30 W:0.45 P:0.14 O:0.02   |     83.87 |    L:0.34 W:0.43 P:0.13 O:0.02    |   84.10 |   L:0.35 W:0.42 P:0.13 O:0.02   |  Obese (Class I)  |
|    85 | 1.75 |   70.00 |     81.84 |  82.36 |  L:0.24 W:0.49 P:0.15 O:0.02   |     83.06 |    L:0.29 W:0.46 P:0.14 O:0.02    |   83.22 |   L:0.30 W:0.46 P:0.14 O:0.02   |    Overweight     |
|    85 | 2.00 |  104.49 |     82.09 |  80.99 |  L:0.15 W:0.55 P:0.17 O:0.03   |     81.93 |    L:0.21 W:0.51 P:0.16 O:0.02    |   81.99 |   L:0.22 W:0.51 P:0.16 O:0.02   |      Normal       |
|    85 | 2.27 |  152.78 |     82.36 |  79.99 |  L:0.08 W:0.60 P:0.18 O:0.03   |     81.12 |    L:0.16 W:0.55 P:0.17 O:0.03    |   81.11 |   L:0.16 W:0.55 P:0.17 O:0.03   | Moderate thinness |
|    85 | 2.72 |  262.84 |     82.83 |  78.95 |  L:0.01 W:0.64 P:0.20 O:0.03   |     80.27 |    L:0.10 W:0.58 P:0.18 O:0.03    |   80.20 |   L:0.10 W:0.59 P:0.18 O:0.03   |  Severe thinness  |
|    85 | 2.80 |  286.72 |     82.91 |  78.82 |  L:0.01 W:0.65 P:0.20 O:0.03   |     80.17 |    L:0.10 W:0.59 P:0.18 O:0.03    |   80.08 |   L:0.09 W:0.59 P:0.18 O:0.03   |  Severe thinness  |

| m(kg) | h(m) | CDDA(L) | Simple(L) | BMI(L) | BMI(P) fat/water/protein/other | Brozek(L) | Brozek(P) fat/water/protein/other | Siri(L) | Siri(P) fat/water/protein/other | Category          |
|-------|------|---------|-----------|--------|--------------------------------|-----------|-----------------------------------|---------|---------------------------------|-------------------|
|   100 | 0.55 |    2.17 |     95.37 | 194.35 | L:4.45 W:-2.24 P:-0.69 O:-0.10 |      0.00 |  L:4.74 W:-2.43 P:-0.75 O:-0.11   |    0.00 | L:5.12 W:-2.68 P:-0.82 O:-0.12  | Obese (Class III) |
|   100 | 0.70 |    4.48 |     95.54 | 147.52 | L:2.69 W:-1.10 P:-0.34 O:-0.05 |    145.36 |  L:2.60 W:-1.04 P:-0.32 O:-0.05   |  150.18 | L:2.80 W:-1.17 P:-0.36 O:-0.05  | Obese (Class III) |
|   100 | 1.00 |   13.06 |     95.90 | 115.95 | L:1.24 W:-0.16 P:-0.05 O:-0.01 |    114.20 |  L:1.16 W:-0.10 P:-0.03 O:-0.00   |  115.84 | L:1.24 W:-0.16 P:-0.05 O:-0.01  | Obese (Class III) |
|   100 | 1.22 |   23.72 |     96.16 | 107.03 |  L:0.79 W:0.14 P:0.04 O:0.01   |    106.29 |    L:0.75 W:0.16 P:0.05 O:0.01    |  107.22 |   L:0.80 W:0.13 P:0.04 O:0.01   | Obese (Class III) |
|   100 | 1.50 |   44.08 |     96.49 | 101.11 |  L:0.47 W:0.34 P:0.11 O:0.02   |    101.23 |    L:0.48 W:0.34 P:0.10 O:0.02    |  101.72 |   L:0.51 W:0.32 P:0.10 O:0.01   | Obese (Class III) |
|   100 | 1.62 |   55.53 |     96.63 |  99.50 |  L:0.38 W:0.40 P:0.12 O:0.02   |     99.88 |    L:0.41 W:0.39 P:0.12 O:0.02    |  100.24 |   L:0.43 W:0.37 P:0.11 O:0.02   | Obese (Class II)  |
|   100 | 1.75 |   70.00 |     96.79 |  98.12 |  L:0.31 W:0.45 P:0.14 O:0.02   |     98.73 |    L:0.34 W:0.43 P:0.13 O:0.02    |   99.00 |   L:0.36 W:0.42 P:0.13 O:0.02   |  Obese (Class I)  |
|   100 | 2.00 |  104.49 |     97.09 |  96.21 |  L:0.20 W:0.52 P:0.16 O:0.02   |     97.15 |    L:0.25 W:0.48 P:0.15 O:0.02    |   97.29 |   L:0.26 W:0.48 P:0.15 O:0.02   |    Overweight     |
|   100 | 2.27 |  152.78 |     97.42 |  94.82 |  L:0.12 W:0.57 P:0.18 O:0.03   |     96.02 |    L:0.19 W:0.53 P:0.16 O:0.02    |   96.06 |   L:0.19 W:0.52 P:0.16 O:0.02   |      Normal       |
|   100 | 2.72 |  262.84 |     97.97 |  93.38 |  L:0.04 W:0.62 P:0.19 O:0.03   |     94.84 |    L:0.13 W:0.57 P:0.17 O:0.03    |   94.78 |   L:0.12 W:0.57 P:0.18 O:0.03   |  Severe thinness  |
|   100 | 2.80 |  286.72 |     98.07 |  93.19 |  L:0.03 W:0.63 P:0.19 O:0.03   |     94.69 |    L:0.12 W:0.57 P:0.18 O:0.03    |   94.62 |   L:0.11 W:0.58 P:0.18 O:0.03   |  Severe thinness  |

| m(kg) | h(m) | CDDA(L) | Simple(L) | BMI(L) | BMI(P) fat/water/protein/other | Brozek(L) | Brozek(P) fat/water/protein/other | Siri(L) | Siri(P) fat/water/protein/other | Category          |
|-------|------|---------|-----------|--------|--------------------------------|-----------|-----------------------------------|---------|---------------------------------|-------------------|
|   115 | 0.55 |    2.17 |    110.22 |   0.00 | L:5.14 W:-2.69 P:-0.83 O:-0.12 |      0.00 |  L:5.73 W:-3.07 P:-0.95 O:-0.14   |    0.00 | L:6.19 W:-3.37 P:-1.04 O:-0.16  | Obese (Class III) |
|   115 | 0.70 |    4.48 |    110.43 | 181.59 | L:3.12 W:-1.38 P:-0.42 O:-0.06 |    180.37 |  L:3.07 W:-1.35 P:-0.41 O:-0.06   |  187.41 | L:3.32 W:-1.51 P:-0.46 O:-0.07  | Obese (Class III) |
|   115 | 1.00 |   13.06 |    110.84 | 138.20 | L:1.45 W:-0.29 P:-0.09 O:-0.01 |    135.79 |  L:1.35 W:-0.23 P:-0.07 O:-0.01   |  138.10 | L:1.45 W:-0.29 P:-0.09 O:-0.01  | Obese (Class III) |
|   115 | 1.22 |   23.72 |    111.14 | 126.18 |  L:0.93 W:0.05 P:0.01 O:0.00   |    124.93 |    L:0.87 W:0.08 P:0.03 O:0.00    |  126.24 |   L:0.93 W:0.04 P:0.01 O:0.00   | Obese (Class III) |
|   115 | 1.50 |   44.08 |    111.53 | 118.25 |  L:0.57 W:0.28 P:0.09 O:0.01   |    118.08 |    L:0.56 W:0.29 P:0.09 O:0.01    |  118.78 |   L:0.59 W:0.27 P:0.08 O:0.01   | Obese (Class III) |
|   115 | 1.62 |   55.53 |    111.69 | 116.10 |  L:0.46 W:0.35 P:0.11 O:0.02   |    116.26 |    L:0.47 W:0.34 P:0.11 O:0.02    |  116.80 |   L:0.50 W:0.33 P:0.10 O:0.02   | Obese (Class III) |
|   115 | 1.75 |   70.00 |    111.87 | 114.26 |  L:0.38 W:0.41 P:0.12 O:0.02   |    114.72 |    L:0.40 W:0.39 P:0.12 O:0.02    |  115.14 |   L:0.42 W:0.38 P:0.12 O:0.02   | Obese (Class II)  |
|   115 | 2.00 |  104.49 |    112.22 | 111.71 |  L:0.25 W:0.48 P:0.15 O:0.02   |    112.61 |    L:0.30 W:0.46 P:0.14 O:0.02    |  112.84 |   L:0.31 W:0.45 P:0.14 O:0.02   |    Overweight     |
|   115 | 2.27 |  152.78 |    112.60 | 109.87 |  L:0.16 W:0.54 P:0.17 O:0.03   |    111.10 |    L:0.22 W:0.50 P:0.16 O:0.02    |  111.20 |   L:0.23 W:0.50 P:0.15 O:0.02   |      Normal       |
|   115 | 2.72 |  262.84 |    113.25 | 107.95 |  L:0.07 W:0.60 P:0.19 O:0.03   |    109.53 |    L:0.15 W:0.55 P:0.17 O:0.03    |  109.50 |   L:0.15 W:0.55 P:0.17 O:0.03   |  Severe thinness  |
|   115 | 2.80 |  286.72 |    113.36 | 107.71 |  L:0.06 W:0.61 P:0.19 O:0.03   |    109.33 |    L:0.14 W:0.56 P:0.17 O:0.03    |  109.29 |   L:0.14 W:0.56 P:0.17 O:0.03   |  Severe thinness  |

| m(kg) | h(m) | CDDA(L) | Simple(L) | BMI(L) | BMI(P) fat/water/protein/other | Brozek(L) | Brozek(P) fat/water/protein/other | Siri(L) | Siri(P) fat/water/protein/other | Category          |
|-------|------|---------|-----------|--------|--------------------------------|-----------|-----------------------------------|---------|---------------------------------|-------------------|
|   130 | 0.55 |    2.17 |    125.20 |   0.00 | L:5.83 W:-3.14 P:-0.97 O:-0.14 |      0.00 |  L:6.82 W:-3.78 P:-1.16 O:-0.17   |    0.00 | L:7.37 W:-4.14 P:-1.27 O:-0.19  | Obese (Class III) |
|   130 | 0.70 |    4.48 |    125.43 | 219.52 | L:3.54 W:-1.65 P:-0.51 O:-0.08 |    220.64 |  L:3.57 W:-1.67 P:-0.51 O:-0.08   |  230.62 | L:3.86 W:-1.86 P:-0.57 O:-0.09  | Obese (Class III) |
|   130 | 1.00 |   13.06 |    125.90 | 161.86 | L:1.66 W:-0.43 P:-0.13 O:-0.02 |    158.78 |  L:1.55 W:-0.36 P:-0.11 O:-0.02   |  161.90 | L:1.66 W:-0.43 P:-0.13 O:-0.02  | Obese (Class III) |
|   130 | 1.22 |   23.72 |    126.24 | 146.19 | L:1.07 W:-0.04 P:-0.01 O:-0.00 |    144.37 |    L:1.00 W:0.00 P:0.00 O:0.00    |  146.14 | L:1.07 W:-0.04 P:-0.01 O:-0.00  | Obese (Class III) |
|   130 | 1.50 |   44.08 |    126.69 | 135.93 |  L:0.66 W:0.22 P:0.07 O:0.01   |    135.41 |    L:0.64 W:0.24 P:0.07 O:0.01    |  136.37 |   L:0.68 W:0.21 P:0.06 O:0.01   | Obese (Class III) |
|   130 | 1.62 |   55.53 |    126.88 | 133.15 |  L:0.54 W:0.30 P:0.09 O:0.01   |    133.04 |    L:0.54 W:0.30 P:0.09 O:0.01    |  133.79 |   L:0.57 W:0.28 P:0.09 O:0.01   | Obese (Class III) |
|   130 | 1.75 |   70.00 |    127.08 | 130.78 |  L:0.44 W:0.36 P:0.11 O:0.02   |    131.04 |    L:0.46 W:0.35 P:0.11 O:0.02    |  131.62 |   L:0.48 W:0.34 P:0.10 O:0.02   | Obese (Class III) |
|   130 | 2.00 |  104.49 |    127.48 | 127.51 |  L:0.31 W:0.45 P:0.14 O:0.02   |    128.31 |    L:0.34 W:0.43 P:0.13 O:0.02    |  128.66 |   L:0.36 W:0.42 P:0.13 O:0.02   |  Obese (Class I)  |
|   130 | 2.27 |  152.78 |    127.92 | 125.14 |  L:0.21 W:0.52 P:0.16 O:0.02   |    126.36 |    L:0.26 W:0.48 P:0.15 O:0.02    |  126.54 |   L:0.27 W:0.48 P:0.15 O:0.02   |    Overweight     |
|   130 | 2.72 |  262.84 |    128.65 | 122.68 |  L:0.10 W:0.59 P:0.18 O:0.03   |    124.34 |    L:0.17 W:0.54 P:0.17 O:0.02    |  124.36 |   L:0.17 W:0.54 P:0.17 O:0.02   |   Mild thinness   |
|   130 | 2.80 |  286.72 |    128.78 | 122.37 |  L:0.09 W:0.59 P:0.18 O:0.03   |    124.09 |    L:0.16 W:0.55 P:0.17 O:0.03    |  124.08 |   L:0.16 W:0.55 P:0.17 O:0.03   | Moderate thinness |

| m(kg) | h(m) | CDDA(L) | Simple(L) | BMI(L) | BMI(P) fat/water/protein/other | Brozek(L) | Brozek(P) fat/water/protein/other | Siri(L) | Siri(P) fat/water/protein/other | Category          |
|-------|------|---------|-----------|--------|--------------------------------|-----------|-----------------------------------|---------|---------------------------------|-------------------|
|   145 | 0.55 |    2.17 |    140.28 |   0.00 | L:6.52 W:-3.59 P:-1.10 O:-0.17 |      0.00 |  L:8.03 W:-4.57 P:-1.41 O:-0.21   |    0.00 | L:8.68 W:-4.99 P:-1.54 O:-0.23  | Obese (Class III) |
|   145 | 0.70 |    4.48 |    140.55 | 261.63 | L:3.97 W:-1.93 P:-0.59 O:-0.09 |    267.19 |  L:4.10 W:-2.02 P:-0.62 O:-0.09   |  281.02 | L:4.43 W:-2.23 P:-0.69 O:-0.10  | Obese (Class III) |
|   145 | 1.00 |   13.06 |    141.07 | 186.97 | L:1.87 W:-0.57 P:-0.17 O:-0.03 |    183.27 |  L:1.75 W:-0.49 P:-0.15 O:-0.02   |  187.37 | L:1.88 W:-0.57 P:-0.18 O:-0.03  | Obese (Class III) |
|   145 | 1.22 |   23.72 |    141.46 | 167.08 | L:1.21 W:-0.14 P:-0.04 O:-0.01 |    164.64 |  L:1.12 W:-0.08 P:-0.02 O:-0.00   |  166.94 | L:1.20 W:-0.13 P:-0.04 O:-0.01  | Obese (Class III) |
|   145 | 1.50 |   44.08 |    141.96 | 154.15 |  L:0.75 W:0.16 P:0.05 O:0.01   |    153.21 |    L:0.72 W:0.18 P:0.06 O:0.01    |  154.47 |   L:0.76 W:0.15 P:0.05 O:0.01   | Obese (Class III) |
|   145 | 1.62 |   55.53 |    142.17 | 150.66 |  L:0.62 W:0.25 P:0.08 O:0.01   |    150.21 |    L:0.61 W:0.26 P:0.08 O:0.01    |  151.21 |   L:0.64 W:0.23 P:0.07 O:0.01   | Obese (Class III) |
|   145 | 1.75 |   70.00 |    142.41 | 147.69 |  L:0.51 W:0.32 P:0.10 O:0.01   |    147.70 |    L:0.51 W:0.32 P:0.10 O:0.01    |  148.48 |   L:0.54 W:0.30 P:0.09 O:0.01   | Obese (Class III) |
|   145 | 2.00 |  104.49 |    142.86 | 143.59 |  L:0.36 W:0.42 P:0.13 O:0.02   |    144.25 |    L:0.38 W:0.40 P:0.12 O:0.02    |  144.74 |   L:0.40 W:0.39 P:0.12 O:0.02   | Obese (Class II)  |
|   145 | 2.27 |  152.78 |    143.34 | 140.64 |  L:0.25 W:0.49 P:0.15 O:0.02   |    141.80 |    L:0.29 W:0.46 P:0.14 O:0.02    |  142.08 |   L:0.30 W:0.45 P:0.14 O:0.02   |    Overweight     |
|   145 | 2.72 |  262.84 |    144.17 | 137.56 |  L:0.13 W:0.57 P:0.17 O:0.03   |    139.28 |    L:0.19 W:0.52 P:0.16 O:0.02    |  139.35 |   L:0.20 W:0.52 P:0.16 O:0.02   |      Normal       |
|   145 | 2.80 |  286.72 |    144.31 | 137.17 |  L:0.11 W:0.58 P:0.18 O:0.03   |    138.96 |    L:0.18 W:0.53 P:0.16 O:0.02    |  139.00 |   L:0.18 W:0.53 P:0.16 O:0.02   |   Mild thinness   |

| m(kg) | h(m) | CDDA(L) | Simple(L) | BMI(L) | BMI(P) fat/water/protein/other | Brozek(L) | Brozek(P) fat/water/protein/other | Siri(L) | Siri(P) fat/water/protein/other | Category          |
|-------|------|---------|-----------|--------|--------------------------------|-----------|-----------------------------------|---------|---------------------------------|-------------------|
|   160 | 0.55 |    2.17 |    155.47 |   0.00 | L:7.21 W:-4.03 P:-1.24 O:-0.19 |      0.00 |  L:9.38 W:-5.45 P:-1.68 O:-0.25   |    0.00 | L:10.15 W:-5.95 P:-1.83 O:-0.27 | Obese (Class III) |
|   160 | 0.70 |    4.48 |    155.76 | 308.29 | L:4.39 W:-2.21 P:-0.68 O:-0.10 |      0.00 |  L:4.66 W:-2.38 P:-0.73 O:-0.11   |    0.00 | L:5.04 W:-2.62 P:-0.81 O:-0.12  | Obese (Class III) |
|   160 | 1.00 |   13.06 |    156.35 | 213.59 | L:2.08 W:-0.70 P:-0.22 O:-0.03 |    209.38 |  L:1.96 W:-0.62 P:-0.19 O:-0.03   |  214.62 | L:2.11 W:-0.72 P:-0.22 O:-0.03  | Obese (Class III) |
|   160 | 1.22 |   23.72 |    156.78 | 188.88 | L:1.35 W:-0.23 P:-0.07 O:-0.01 |    185.78 |  L:1.25 W:-0.16 P:-0.05 O:-0.01   |  188.71 | L:1.34 W:-0.22 P:-0.07 O:-0.01  | Obese (Class III) |
|   160 | 1.50 |   44.08 |    157.33 | 172.92 |  L:0.84 W:0.10 P:0.03 O:0.00   |    171.52 |    L:0.80 W:0.13 P:0.04 O:0.01    |  173.13 |   L:0.85 W:0.10 P:0.03 O:0.00   | Obese (Class III) |
|   160 | 1.62 |   55.53 |    157.57 | 168.63 |  L:0.70 W:0.19 P:0.06 O:0.01   |    167.80 |    L:0.67 W:0.21 P:0.07 O:0.01    |  169.08 |   L:0.72 W:0.18 P:0.06 O:0.01   | Obese (Class III) |
|   160 | 1.75 |   70.00 |    157.83 | 164.99 |  L:0.58 W:0.27 P:0.08 O:0.01   |    164.69 |    L:0.57 W:0.28 P:0.09 O:0.01    |  165.70 |   L:0.60 W:0.26 P:0.08 O:0.01   | Obese (Class III) |
|   160 | 2.00 |  104.49 |    158.33 | 159.97 |  L:0.41 W:0.38 P:0.12 O:0.02   |    160.45 |    L:0.43 W:0.37 P:0.11 O:0.02    |  161.09 |   L:0.45 W:0.36 P:0.11 O:0.02   | Obese (Class III) |
|   160 | 2.27 |  152.78 |    158.88 | 156.35 |  L:0.29 W:0.46 P:0.14 O:0.02   |    157.44 |    L:0.32 W:0.44 P:0.14 O:0.02    |  157.82 |   L:0.34 W:0.43 P:0.13 O:0.02   |  Obese (Class I)  |
|   160 | 2.72 |  262.84 |    159.79 | 152.59 |  L:0.16 W:0.55 P:0.17 O:0.03   |    154.34 |    L:0.22 W:0.51 P:0.16 O:0.02    |  154.47 |   L:0.22 W:0.51 P:0.16 O:0.02   |      Normal       |
|   160 | 2.80 |  286.72 |    159.96 | 152.11 |  L:0.14 W:0.56 P:0.17 O:0.03   |    153.95 |    L:0.20 W:0.52 P:0.16 O:0.02    |  154.04 |   L:0.21 W:0.52 P:0.16 O:0.02   |      Normal       |

| m(kg) | h(m) | CDDA(L) | Simple(L) | BMI(L) | BMI(P) fat/water/protein/other | Brozek(L) | Brozek(P) fat/water/protein/other | Siri(L) | Siri(P) fat/water/protein/other | Category          |
|-------|------|---------|-----------|--------|--------------------------------|-----------|-----------------------------------|---------|---------------------------------|-------------------|
|   175 | 0.55 |    2.17 |    170.75 |   0.00 | L:7.90 W:-4.48 P:-1.38 O:-0.21 |      0.00 |  L:10.90 W:-6.44 P:-1.98 O:-0.30  |    0.00 | L:11.79 W:-7.02 P:-2.16 O:-0.32 | Obese (Class III) |
|   175 | 0.70 |    4.48 |    171.07 |   0.00 | L:4.82 W:-2.48 P:-0.76 O:-0.11 |      0.00 |  L:5.26 W:-2.77 P:-0.85 O:-0.13   |    0.00 | L:5.68 W:-3.04 P:-0.94 O:-0.14  | Obese (Class III) |
|   175 | 1.00 |   13.06 |    171.72 | 241.76 | L:2.29 W:-0.84 P:-0.26 O:-0.04 |    237.22 |  L:2.17 W:-0.76 P:-0.23 O:-0.04   |  243.80 | L:2.34 W:-0.87 P:-0.27 O:-0.04  | Obese (Class III) |
|   175 | 1.22 |   23.72 |    172.19 | 211.60 | L:1.49 W:-0.32 P:-0.10 O:-0.01 |    207.83 |  L:1.38 W:-0.25 P:-0.08 O:-0.01   |  211.47 | L:1.49 W:-0.32 P:-0.10 O:-0.01  | Obese (Class III) |
|   175 | 1.50 |   44.08 |    172.80 | 192.26 |  L:0.94 W:0.04 P:0.01 O:0.00   |    190.33 |    L:0.88 W:0.08 P:0.02 O:0.00    |  192.34 |   L:0.94 W:0.04 P:0.01 O:0.00   | Obese (Class III) |
|   175 | 1.62 |   55.53 |    173.07 | 187.07 |  L:0.78 W:0.14 P:0.04 O:0.01   |    185.81 |    L:0.74 W:0.17 P:0.05 O:0.01    |  187.41 |   L:0.79 W:0.14 P:0.04 O:0.01   | Obese (Class III) |
|   175 | 1.75 |   70.00 |    173.35 | 182.69 |  L:0.65 W:0.23 P:0.07 O:0.01   |    182.03 |    L:0.63 W:0.24 P:0.07 O:0.01    |  183.30 |   L:0.67 W:0.22 P:0.07 O:0.01   | Obese (Class III) |
|   175 | 2.00 |  104.49 |    173.91 | 176.64 |  L:0.46 W:0.35 P:0.11 O:0.02   |    176.89 |    L:0.47 W:0.34 P:0.11 O:0.02    |  177.72 |   L:0.50 W:0.33 P:0.10 O:0.02   | Obese (Class III) |
|   175 | 2.27 |  152.78 |    174.51 | 172.29 |  L:0.33 W:0.44 P:0.13 O:0.02   |    173.26 |    L:0.36 W:0.42 P:0.13 O:0.02    |  173.77 |   L:0.37 W:0.41 P:0.13 O:0.02   |  Obese (Class I)  |
|   175 | 2.72 |  262.84 |    175.52 | 167.78 |  L:0.18 W:0.53 P:0.16 O:0.02   |    169.53 |    L:0.24 W:0.49 P:0.15 O:0.02    |  169.73 |   L:0.25 W:0.49 P:0.15 O:0.02   |      Normal       |
|   175 | 2.80 |  286.72 |    175.70 | 167.20 |  L:0.16 W:0.54 P:0.17 O:0.03   |    169.06 |    L:0.22 W:0.50 P:0.16 O:0.02    |  169.22 |   L:0.23 W:0.50 P:0.15 O:0.02   |      Normal       |

| m(kg) | h(m) | CDDA(L) | Simple(L) | BMI(L) | BMI(P) fat/water/protein/other | Brozek(L) | Brozek(P) fat/water/protein/other | Siri(L) | Siri(P) fat/water/protein/other | Category          |
|-------|------|---------|-----------|--------|--------------------------------|-----------|-----------------------------------|---------|---------------------------------|-------------------|
|   190 | 0.55 |    2.17 |    186.11 |   0.00 | L:8.59 W:-4.93 P:-1.52 O:-0.23 |      0.00 |  L:12.62 W:-7.55 P:-2.32 O:-0.35  |    0.00 | L:13.66 W:-8.23 P:-2.53 O:-0.38 | Obese (Class III) |
|   190 | 0.70 |    4.48 |    186.46 |   0.00 | L:5.24 W:-2.76 P:-0.85 O:-0.13 |      0.00 |  L:5.89 W:-3.18 P:-0.98 O:-0.15   |    0.00 | L:6.36 W:-3.49 P:-1.07 O:-0.16  | Obese (Class III) |
|   190 | 1.00 |   13.06 |    187.17 | 271.56 | L:2.50 W:-0.97 P:-0.30 O:-0.04 |    266.93 |  L:2.39 W:-0.90 P:-0.28 O:-0.04   |  275.08 | L:2.57 W:-1.02 P:-0.31 O:-0.05  | Obese (Class III) |
|   190 | 1.22 |   23.72 |    187.69 | 235.27 | L:1.63 W:-0.41 P:-0.13 O:-0.02 |    230.83 |  L:1.52 W:-0.34 P:-0.10 O:-0.02   |  235.28 | L:1.63 W:-0.41 P:-0.13 O:-0.02  | Obese (Class III) |
|   190 | 1.50 |   44.08 |    188.36 | 212.16 | L:1.03 W:-0.02 P:-0.01 O:-0.00 |    209.67 |    L:0.96 W:0.03 P:0.01 O:0.00    |  212.13 | L:1.03 W:-0.02 P:-0.01 O:-0.00  | Obese (Class III) |
|   190 | 1.62 |   55.53 |    188.64 | 206.00 |  L:0.86 W:0.09 P:0.03 O:0.00   |    204.24 |    L:0.81 W:0.12 P:0.04 O:0.01    |  206.21 |   L:0.87 W:0.09 P:0.03 O:0.00   | Obese (Class III) |
|   190 | 1.75 |   70.00 |    188.96 | 200.78 |  L:0.72 W:0.18 P:0.06 O:0.01   |    199.72 |    L:0.69 W:0.20 P:0.06 O:0.01    |  201.29 |   L:0.73 W:0.17 P:0.05 O:0.01   | Obese (Class III) |
|   190 | 2.00 |  104.49 |    189.56 | 193.60 |  L:0.51 W:0.32 P:0.10 O:0.01   |    193.60 |    L:0.51 W:0.32 P:0.10 O:0.01    |  194.62 |   L:0.54 W:0.30 P:0.09 O:0.01   | Obese (Class III) |
|   190 | 2.27 |  152.78 |    190.22 | 188.45 |  L:0.37 W:0.41 P:0.13 O:0.02   |    189.27 |    L:0.39 W:0.40 P:0.12 O:0.02    |  189.93 |   L:0.41 W:0.38 P:0.12 O:0.02   | Obese (Class II)  |
|   190 | 2.72 |  262.84 |    191.32 | 183.12 |  L:0.21 W:0.51 P:0.16 O:0.02   |    184.85 |    L:0.26 W:0.48 P:0.15 O:0.02    |  185.13 |   L:0.27 W:0.47 P:0.15 O:0.02   |    Overweight     |
|   190 | 2.80 |  286.72 |    191.52 | 182.43 |  L:0.19 W:0.53 P:0.16 O:0.02   |    184.29 |    L:0.25 W:0.49 P:0.15 O:0.02    |  184.52 |   L:0.25 W:0.49 P:0.15 O:0.02   |      Normal       |

| m(kg) | h(m) | CDDA(L) | Simple(L) | BMI(L) | BMI(P) fat/water/protein/other | Brozek(L) | Brozek(P) fat/water/protein/other | Siri(L) | Siri(P) fat/water/protein/other | Category          |
|-------|------|---------|-----------|--------|--------------------------------|-----------|-----------------------------------|---------|---------------------------------|-------------------|
|   205 | 0.55 |    2.17 |    201.54 |   0.00 | L:9.27 W:-5.38 P:-1.65 O:-0.25 |      0.00 |  L:14.59 W:-8.83 P:-2.72 O:-0.41  |    0.00 | L:15.79 W:-9.61 P:-2.96 O:-0.44 | Obese (Class III) |
|   205 | 0.70 |    4.48 |    201.92 |   0.00 | L:5.67 W:-3.04 P:-0.93 O:-0.14 |      0.00 |  L:6.56 W:-3.61 P:-1.11 O:-0.17   |    0.00 | L:7.09 W:-3.96 P:-1.22 O:-0.18  | Obese (Class III) |
|   205 | 1.00 |   13.06 |    202.69 | 303.05 | L:2.70 W:-1.11 P:-0.34 O:-0.05 |    298.66 |  L:2.61 W:-1.05 P:-0.32 O:-0.05   |  308.62 | L:2.82 W:-1.18 P:-0.36 O:-0.05  | Obese (Class III) |
|   205 | 1.22 |   23.72 |    203.25 | 259.90 | L:1.77 W:-0.50 P:-0.15 O:-0.02 |    254.83 |  L:1.65 W:-0.42 P:-0.13 O:-0.02   |  260.19 | L:1.78 W:-0.50 P:-0.16 O:-0.02  | Obese (Class III) |
|   205 | 1.50 |   44.08 |    203.98 | 232.65 | L:1.12 W:-0.08 P:-0.02 O:-0.00 |    229.56 |  L:1.04 W:-0.03 P:-0.01 O:-0.00   |  232.51 | L:1.12 W:-0.08 P:-0.02 O:-0.00  | Obese (Class III) |
|   205 | 1.62 |   55.53 |    204.29 | 225.40 |  L:0.94 W:0.04 P:0.01 O:0.00   |    223.12 |    L:0.88 W:0.08 P:0.02 O:0.00    |  225.49 |   L:0.94 W:0.04 P:0.01 O:0.00   | Obese (Class III) |
|   205 | 1.75 |   70.00 |    204.63 | 219.28 |  L:0.79 W:0.14 P:0.04 O:0.01   |    217.78 |    L:0.75 W:0.16 P:0.05 O:0.01    |  219.67 |   L:0.79 W:0.13 P:0.04 O:0.01   | Obese (Class III) |
|   205 | 2.00 |  104.49 |    205.29 | 210.87 |  L:0.57 W:0.28 P:0.09 O:0.01   |    210.56 |    L:0.56 W:0.29 P:0.09 O:0.01    |  211.81 |   L:0.59 W:0.27 P:0.08 O:0.01   | Obese (Class III) |
|   205 | 2.27 |  152.78 |    206.00 | 204.84 |  L:0.41 W:0.39 P:0.12 O:0.02   |    205.48 |    L:0.42 W:0.37 P:0.12 O:0.02    |  206.29 |   L:0.45 W:0.36 P:0.11 O:0.02   | Obese (Class II)  |
|   205 | 2.72 |  262.84 |    207.21 | 198.61 |  L:0.24 W:0.49 P:0.15 O:0.02   |    200.30 |    L:0.29 W:0.46 P:0.14 O:0.02    |  200.67 |   L:0.30 W:0.46 P:0.14 O:0.02   |    Overweight     |
|   205 | 2.80 |  286.72 |    207.42 | 197.81 |  L:0.22 W:0.51 P:0.16 O:0.02   |    199.64 |    L:0.27 W:0.48 P:0.15 O:0.02    |  199.96 |   L:0.28 W:0.47 P:0.14 O:0.02   |    Overweight     |

