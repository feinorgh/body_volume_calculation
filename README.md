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

This model also takes the proportion of fat vs. other components into account, and uses the same clamping strategy as above.

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

| m(kg) | h(m) | CDDA(L) | Simple(L) | BMI(L) | Brozek(L) | Siri(L) | Category          |
|-------|------|---------|-----------|--------|-----------|---------|-------------------|
|    25 | 0.55 |    2.17 |     23.18 |  27.78 |     27.47 |   27.78 | Obese (Class III) |
|    25 | 0.70 |    4.48 |     23.22 |  25.70 |     25.67 |   25.82 | Obese (Class III) |
|    25 | 1.00 |   13.06 |     23.30 |  24.05 |     24.29 |   24.32 |    Overweight     |
|    25 | 1.22 |   23.72 |     23.37 |  23.55 |     23.87 |   23.87 | Moderate thinness |
|    25 | 1.50 |   44.08 |     23.44 |  23.20 |     23.59 |   23.57 |  Severe thinness  |
|    25 | 1.62 |   55.53 |     23.48 |  23.16 |     23.56 |   23.53 |  Severe thinness  |
|    25 | 1.75 |   70.00 |     23.51 |  23.16 |     23.56 |   23.53 |  Severe thinness  |
|    25 | 2.00 |  104.49 |     23.59 |  23.16 |     23.56 |   23.53 |  Severe thinness  |
|    25 | 2.27 |  152.78 |     23.66 |  23.16 |     23.56 |   23.53 |  Severe thinness  |
|    25 | 2.72 |  262.84 |     23.79 |  23.16 |     23.56 |   23.53 |  Severe thinness  |
|    25 | 2.80 |  286.72 |     23.82 |  23.16 |     23.56 |   23.53 |  Severe thinness  |

| m(kg) | h(m) | CDDA(L) | Simple(L) | BMI(L) | Brozek(L) | Siri(L) | Category          |
|-------|------|---------|-----------|--------|-----------|---------|-------------------|
|    40 | 0.55 |    2.17 |     37.31 |  44.44 |     43.95 |   44.44 | Obese (Class III) |
|    40 | 0.70 |    4.48 |     37.38 |  44.36 |     43.87 |   44.36 | Obese (Class III) |
|    40 | 1.00 |   13.06 |     37.51 |  39.99 |     40.11 |   40.27 | Obese (Class III) |
|    40 | 1.22 |   23.72 |     37.61 |  38.67 |     39.01 |   39.08 |    Overweight     |
|    40 | 1.50 |   44.08 |     37.74 |  37.77 |     38.28 |   38.28 |   Mild thinness   |
|    40 | 1.62 |   55.53 |     37.80 |  37.52 |     38.07 |   38.06 |  Severe thinness  |
|    40 | 1.75 |   70.00 |     37.86 |  37.31 |     37.90 |   37.87 |  Severe thinness  |
|    40 | 2.00 |  104.49 |     37.97 |  37.05 |     37.69 |   37.65 |  Severe thinness  |
|    40 | 2.27 |  152.78 |     38.10 |  37.05 |     37.69 |   37.65 |  Severe thinness  |
|    40 | 2.72 |  262.84 |     38.31 |  37.05 |     37.69 |   37.65 |  Severe thinness  |
|    40 | 2.80 |  286.72 |     38.34 |  37.05 |     37.69 |   37.65 |  Severe thinness  |

| m(kg) | h(m) | CDDA(L) | Simple(L) | BMI(L) | Brozek(L) | Siri(L) | Category          |
|-------|------|---------|-----------|--------|-----------|---------|-------------------|
|    55 | 0.55 |    2.17 |     51.60 |  61.11 |     60.42 |   61.11 | Obese (Class III) |
|    55 | 0.70 |    4.48 |     51.70 |  61.11 |     60.42 |   61.11 | Obese (Class III) |
|    55 | 1.00 |   13.06 |     51.89 |  57.11 |     56.95 |   57.32 | Obese (Class III) |
|    55 | 1.22 |   23.72 |     52.02 |  54.56 |     54.80 |   54.99 | Obese (Class II)  |
|    55 | 1.50 |   44.08 |     52.20 |  52.84 |     53.37 |   53.44 |      Normal       |
|    55 | 1.62 |   55.53 |     52.28 |  52.36 |     52.98 |   53.02 |      Normal       |
|    55 | 1.75 |   70.00 |     52.36 |  51.96 |     52.65 |   52.66 |   Mild thinness   |
|    55 | 2.00 |  104.49 |     52.52 |  51.39 |     52.19 |   52.16 |  Severe thinness  |
|    55 | 2.27 |  152.78 |     52.70 |  50.98 |     51.85 |   51.80 |  Severe thinness  |
|    55 | 2.72 |  262.84 |     52.99 |  50.95 |     51.83 |   51.77 |  Severe thinness  |
|    55 | 2.80 |  286.72 |     53.04 |  50.95 |     51.83 |   51.77 |  Severe thinness  |

| m(kg) | h(m) | CDDA(L) | Simple(L) | BMI(L) | Brozek(L) | Siri(L) | Category          |
|-------|------|---------|-----------|--------|-----------|---------|-------------------|
|    70 | 0.55 |    2.17 |     66.05 |  77.78 |     76.90 |   77.78 | Obese (Class III) |
|    70 | 0.70 |    4.48 |     66.17 |  77.78 |     76.90 |   77.78 | Obese (Class III) |
|    70 | 1.00 |   13.06 |     66.41 |  75.45 |     74.86 |   75.55 | Obese (Class III) |
|    70 | 1.22 |   23.72 |     66.59 |  71.24 |     71.25 |   71.63 | Obese (Class III) |
|    70 | 1.50 |   44.08 |     66.82 |  68.41 |     68.89 |   69.06 |  Obese (Class I)  |
|    70 | 1.62 |   55.53 |     66.92 |  67.64 |     68.25 |   68.36 |    Overweight     |
|    70 | 1.75 |   70.00 |     67.02 |  66.97 |     67.70 |   67.77 |      Normal       |
|    70 | 2.00 |  104.49 |     67.23 |  66.05 |     66.94 |   66.95 |   Mild thinness   |
|    70 | 2.27 |  152.78 |     67.45 |  65.38 |     66.40 |   66.36 |  Severe thinness  |
|    70 | 2.72 |  262.84 |     67.83 |  64.84 |     65.97 |   65.89 |  Severe thinness  |
|    70 | 2.80 |  286.72 |     67.90 |  64.84 |     65.97 |   65.89 |  Severe thinness  |

| m(kg) | h(m) | CDDA(L) | Simple(L) | BMI(L) | Brozek(L) | Siri(L) | Category          |
|-------|------|---------|-----------|--------|-----------|---------|-------------------|
|    85 | 0.55 |    2.17 |     80.64 |  94.44 |     93.38 |   94.44 | Obese (Class III) |
|    85 | 0.70 |    4.48 |     80.79 |  94.44 |     93.38 |   94.44 | Obese (Class III) |
|    85 | 1.00 |   13.06 |     81.08 |  94.44 |     93.38 |   94.44 | Obese (Class III) |
|    85 | 1.22 |   23.72 |     81.30 |  88.73 |     88.41 |   89.02 | Obese (Class III) |
|    85 | 1.50 |   44.08 |     81.58 |  84.50 |     84.84 |   85.14 | Obese (Class II)  |
|    85 | 1.62 |   55.53 |     81.70 |  83.35 |     83.87 |   84.10 |  Obese (Class I)  |
|    85 | 1.75 |   70.00 |     81.84 |  82.36 |     83.06 |   83.22 |    Overweight     |
|    85 | 2.00 |  104.49 |     82.09 |  80.99 |     81.93 |   81.99 |      Normal       |
|    85 | 2.27 |  152.78 |     82.36 |  79.99 |     81.12 |   81.11 | Moderate thinness |
|    85 | 2.72 |  262.84 |     82.83 |  78.95 |     80.27 |   80.20 |  Severe thinness  |
|    85 | 2.80 |  286.72 |     82.91 |  78.82 |     80.17 |   80.08 |  Severe thinness  |

| m(kg) | h(m) | CDDA(L) | Simple(L) | BMI(L) | Brozek(L) | Siri(L) | Category          |
|-------|------|---------|-----------|--------|-----------|---------|-------------------|
|   100 | 0.55 |    2.17 |     95.37 | 111.11 |    109.86 |  111.11 | Obese (Class III) |
|   100 | 0.70 |    4.48 |     95.54 | 111.11 |    109.86 |  111.11 | Obese (Class III) |
|   100 | 1.00 |   13.06 |     95.90 | 111.11 |    109.86 |  111.11 | Obese (Class III) |
|   100 | 1.22 |   23.72 |     96.16 | 107.03 |    106.29 |  107.22 | Obese (Class III) |
|   100 | 1.50 |   44.08 |     96.49 | 101.11 |    101.23 |  101.72 | Obese (Class III) |
|   100 | 1.62 |   55.53 |     96.63 |  99.50 |     99.88 |  100.24 | Obese (Class II)  |
|   100 | 1.75 |   70.00 |     96.79 |  98.12 |     98.73 |   99.00 |  Obese (Class I)  |
|   100 | 2.00 |  104.49 |     97.09 |  96.21 |     97.15 |   97.29 |    Overweight     |
|   100 | 2.27 |  152.78 |     97.42 |  94.82 |     96.02 |   96.06 |      Normal       |
|   100 | 2.72 |  262.84 |     97.97 |  93.38 |     94.84 |   94.78 |  Severe thinness  |
|   100 | 2.80 |  286.72 |     98.07 |  93.19 |     94.69 |   94.62 |  Severe thinness  |

| m(kg) | h(m) | CDDA(L) | Simple(L) | BMI(L) | Brozek(L) | Siri(L) | Category          |
|-------|------|---------|-----------|--------|-----------|---------|-------------------|
|   115 | 0.55 |    2.17 |    110.22 | 127.78 |    126.34 |  127.78 | Obese (Class III) |
|   115 | 0.70 |    4.48 |    110.43 | 127.78 |    126.34 |  127.78 | Obese (Class III) |
|   115 | 1.00 |   13.06 |    110.84 | 127.78 |    126.34 |  127.78 | Obese (Class III) |
|   115 | 1.22 |   23.72 |    111.14 | 126.18 |    124.93 |  126.24 | Obese (Class III) |
|   115 | 1.50 |   44.08 |    111.53 | 118.25 |    118.08 |  118.78 | Obese (Class III) |
|   115 | 1.62 |   55.53 |    111.69 | 116.10 |    116.26 |  116.80 | Obese (Class III) |
|   115 | 1.75 |   70.00 |    111.87 | 114.26 |    114.72 |  115.14 | Obese (Class II)  |
|   115 | 2.00 |  104.49 |    112.22 | 111.71 |    112.61 |  112.84 |    Overweight     |
|   115 | 2.27 |  152.78 |    112.60 | 109.87 |    111.10 |  111.20 |      Normal       |
|   115 | 2.72 |  262.84 |    113.25 | 107.95 |    109.53 |  109.50 |  Severe thinness  |
|   115 | 2.80 |  286.72 |    113.36 | 107.71 |    109.33 |  109.29 |  Severe thinness  |

| m(kg) | h(m) | CDDA(L) | Simple(L) | BMI(L) | Brozek(L) | Siri(L) | Category          |
|-------|------|---------|-----------|--------|-----------|---------|-------------------|
|   130 | 0.55 |    2.17 |    125.20 | 144.44 |    142.82 |  144.44 | Obese (Class III) |
|   130 | 0.70 |    4.48 |    125.43 | 144.44 |    142.82 |  144.44 | Obese (Class III) |
|   130 | 1.00 |   13.06 |    125.90 | 144.44 |    142.82 |  144.44 | Obese (Class III) |
|   130 | 1.22 |   23.72 |    126.24 | 144.44 |    142.82 |  144.44 | Obese (Class III) |
|   130 | 1.50 |   44.08 |    126.69 | 135.93 |    135.41 |  136.37 | Obese (Class III) |
|   130 | 1.62 |   55.53 |    126.88 | 133.15 |    133.04 |  133.79 | Obese (Class III) |
|   130 | 1.75 |   70.00 |    127.08 | 130.78 |    131.04 |  131.62 | Obese (Class III) |
|   130 | 2.00 |  104.49 |    127.48 | 127.51 |    128.31 |  128.66 |  Obese (Class I)  |
|   130 | 2.27 |  152.78 |    127.92 | 125.14 |    126.36 |  126.54 |    Overweight     |
|   130 | 2.72 |  262.84 |    128.65 | 122.68 |    124.34 |  124.36 |   Mild thinness   |
|   130 | 2.80 |  286.72 |    128.78 | 122.37 |    124.09 |  124.08 | Moderate thinness |

| m(kg) | h(m) | CDDA(L) | Simple(L) | BMI(L) | Brozek(L) | Siri(L) | Category          |
|-------|------|---------|-----------|--------|-----------|---------|-------------------|
|   145 | 0.55 |    2.17 |    140.28 | 161.11 |    159.30 |  161.11 | Obese (Class III) |
|   145 | 0.70 |    4.48 |    140.55 | 161.11 |    159.30 |  161.11 | Obese (Class III) |
|   145 | 1.00 |   13.06 |    141.07 | 161.11 |    159.30 |  161.11 | Obese (Class III) |
|   145 | 1.22 |   23.72 |    141.46 | 161.11 |    159.30 |  161.11 | Obese (Class III) |
|   145 | 1.50 |   44.08 |    141.96 | 154.15 |    153.21 |  154.47 | Obese (Class III) |
|   145 | 1.62 |   55.53 |    142.17 | 150.66 |    150.21 |  151.21 | Obese (Class III) |
|   145 | 1.75 |   70.00 |    142.41 | 147.69 |    147.70 |  148.48 | Obese (Class III) |
|   145 | 2.00 |  104.49 |    142.86 | 143.59 |    144.25 |  144.74 | Obese (Class II)  |
|   145 | 2.27 |  152.78 |    143.34 | 140.64 |    141.80 |  142.08 |    Overweight     |
|   145 | 2.72 |  262.84 |    144.17 | 137.56 |    139.28 |  139.35 |      Normal       |
|   145 | 2.80 |  286.72 |    144.31 | 137.17 |    138.96 |  139.00 |   Mild thinness   |

| m(kg) | h(m) | CDDA(L) | Simple(L) | BMI(L) | Brozek(L) | Siri(L) | Category          |
|-------|------|---------|-----------|--------|-----------|---------|-------------------|
|   160 | 0.55 |    2.17 |    155.47 | 177.78 |    175.78 |  177.78 | Obese (Class III) |
|   160 | 0.70 |    4.48 |    155.76 | 177.78 |    175.78 |  177.78 | Obese (Class III) |
|   160 | 1.00 |   13.06 |    156.35 | 177.78 |    175.78 |  177.78 | Obese (Class III) |
|   160 | 1.22 |   23.72 |    156.78 | 177.78 |    175.78 |  177.78 | Obese (Class III) |
|   160 | 1.50 |   44.08 |    157.33 | 172.92 |    171.52 |  173.13 | Obese (Class III) |
|   160 | 1.62 |   55.53 |    157.57 | 168.63 |    167.80 |  169.08 | Obese (Class III) |
|   160 | 1.75 |   70.00 |    157.83 | 164.99 |    164.69 |  165.70 | Obese (Class III) |
|   160 | 2.00 |  104.49 |    158.33 | 159.97 |    160.45 |  161.09 | Obese (Class III) |
|   160 | 2.27 |  152.78 |    158.88 | 156.35 |    157.44 |  157.82 |  Obese (Class I)  |
|   160 | 2.72 |  262.84 |    159.79 | 152.59 |    154.34 |  154.47 |      Normal       |
|   160 | 2.80 |  286.72 |    159.96 | 152.11 |    153.95 |  154.04 |      Normal       |

| m(kg) | h(m) | CDDA(L) | Simple(L) | BMI(L) | Brozek(L) | Siri(L) | Category          |
|-------|------|---------|-----------|--------|-----------|---------|-------------------|
|   175 | 0.55 |    2.17 |    170.75 | 194.44 |    192.26 |  194.44 | Obese (Class III) |
|   175 | 0.70 |    4.48 |    171.07 | 194.44 |    192.26 |  194.44 | Obese (Class III) |
|   175 | 1.00 |   13.06 |    171.72 | 194.44 |    192.26 |  194.44 | Obese (Class III) |
|   175 | 1.22 |   23.72 |    172.19 | 194.44 |    192.26 |  194.44 | Obese (Class III) |
|   175 | 1.50 |   44.08 |    172.80 | 192.26 |    190.33 |  192.34 | Obese (Class III) |
|   175 | 1.62 |   55.53 |    173.07 | 187.07 |    185.81 |  187.41 | Obese (Class III) |
|   175 | 1.75 |   70.00 |    173.35 | 182.69 |    182.03 |  183.30 | Obese (Class III) |
|   175 | 2.00 |  104.49 |    173.91 | 176.64 |    176.89 |  177.72 | Obese (Class III) |
|   175 | 2.27 |  152.78 |    174.51 | 172.29 |    173.26 |  173.77 |  Obese (Class I)  |
|   175 | 2.72 |  262.84 |    175.52 | 167.78 |    169.53 |  169.73 |      Normal       |
|   175 | 2.80 |  286.72 |    175.70 | 167.20 |    169.06 |  169.22 |      Normal       |

| m(kg) | h(m) | CDDA(L) | Simple(L) | BMI(L) | Brozek(L) | Siri(L) | Category          |
|-------|------|---------|-----------|--------|-----------|---------|-------------------|
|   190 | 0.55 |    2.17 |    186.11 | 211.11 |    208.74 |  211.11 | Obese (Class III) |
|   190 | 0.70 |    4.48 |    186.46 | 211.11 |    208.74 |  211.11 | Obese (Class III) |
|   190 | 1.00 |   13.06 |    187.17 | 211.11 |    208.74 |  211.11 | Obese (Class III) |
|   190 | 1.22 |   23.72 |    187.69 | 211.11 |    208.74 |  211.11 | Obese (Class III) |
|   190 | 1.50 |   44.08 |    188.36 | 211.11 |    208.74 |  211.11 | Obese (Class III) |
|   190 | 1.62 |   55.53 |    188.64 | 206.00 |    204.24 |  206.21 | Obese (Class III) |
|   190 | 1.75 |   70.00 |    188.96 | 200.78 |    199.72 |  201.29 | Obese (Class III) |
|   190 | 2.00 |  104.49 |    189.56 | 193.60 |    193.60 |  194.62 | Obese (Class III) |
|   190 | 2.27 |  152.78 |    190.22 | 188.45 |    189.27 |  189.93 | Obese (Class II)  |
|   190 | 2.72 |  262.84 |    191.32 | 183.12 |    184.85 |  185.13 |    Overweight     |
|   190 | 2.80 |  286.72 |    191.52 | 182.43 |    184.29 |  184.52 |      Normal       |

| m(kg) | h(m) | CDDA(L) | Simple(L) | BMI(L) | Brozek(L) | Siri(L) | Category          |
|-------|------|---------|-----------|--------|-----------|---------|-------------------|
|   205 | 0.55 |    2.17 |    201.54 | 227.78 |    225.22 |  227.78 | Obese (Class III) |
|   205 | 0.70 |    4.48 |    201.92 | 227.78 |    225.22 |  227.78 | Obese (Class III) |
|   205 | 1.00 |   13.06 |    202.69 | 227.78 |    225.22 |  227.78 | Obese (Class III) |
|   205 | 1.22 |   23.72 |    203.25 | 227.78 |    225.22 |  227.78 | Obese (Class III) |
|   205 | 1.50 |   44.08 |    203.98 | 227.78 |    225.22 |  227.78 | Obese (Class III) |
|   205 | 1.62 |   55.53 |    204.29 | 225.40 |    223.12 |  225.49 | Obese (Class III) |
|   205 | 1.75 |   70.00 |    204.63 | 219.28 |    217.78 |  219.67 | Obese (Class III) |
|   205 | 2.00 |  104.49 |    205.29 | 210.87 |    210.56 |  211.81 | Obese (Class III) |
|   205 | 2.27 |  152.78 |    206.00 | 204.84 |    205.48 |  206.29 | Obese (Class II)  |
|   205 | 2.72 |  262.84 |    207.21 | 198.61 |    200.30 |  200.67 |    Overweight     |
|   205 | 2.80 |  286.72 |    207.42 | 197.81 |    199.64 |  199.96 |    Overweight     |

