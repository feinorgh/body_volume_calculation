# Human Body Volume Calculation (Mostly for Cataclysm: Dark Days Ahead)

This repository contains a script that uses five different models to estimate the volume of a human body.

There is no guarantee that the results are accurate, or can be relied upon in any medical context, or even useful in a gaming context.

Also, this has been an unreasonable amount of work just to prove a point, and is unnecessarily detailed.

Anyway, To run the script, you need Python3 and matplotlib (just comment out the plotting business, if you
don't want to install matplotlib)

# Models

Assumption: Volume = Weight / Density

There are five models provided:

## CDDA Original

The original volume calculation from https://github.com/CleverRaven/Cataclysm-DDA/pull/74162)

## CDDA Simple

A proposed volume calculation model based on an online tool, found in https://github.com/CleverRaven/Cataclysm-DDA/pull/74348

## BMI Model

Uses the calculations for producing body fat ratio from BMI, and then applying the average body density based on lipids, water, and protein onto the weight.

## Brozak Model

Uses the Brozak formula for body fat ratio, estimated from BMI. The Brozak model reputedly has ±1% accuracy against empirical methods such as water immersion.

## Siri Model

An older model that used to be used in the same manner as the Brozak model, reputely has ±10% accuracy compared to empirical methods.

# Graph over relations between models and parameters

![3D Plot](Figure_1.png)

The green lines are the original CDDA volume calculation (independent of weight) results for various heighs.

The red lines are the BMI model results.

The blue lines are the Brozak model results.

The yellow lines are the Siri model results.

You can examine this graph better if you run the script yourself, where you can rotate and zoom in.

The graph shows (mostly) that the more sensitive the model is for weight, the larger the difference
between low and high body weight.

The BMI based models (including Brozek and Siri) all seem to produce volumes that inflated (*drum roll*) at
lower heights, the "BMI Model" less so.

It also shows that something weird is going on with the Brozak models and Siri models outside the normal
human size ranges.


# Results

Out of these models, the pure "BMI Model" (really just a simple volume = weight / density calculation) seems
to give reasonable results. The "Brozak" and "Siri" models break down when values are way outside normal
human weights and heights (other models must be used for infants, dissoluted devourers, and blobs, supposedly).

The classification is not meant to fat or thin shame anyone (real or imagined characters), but is the standard
classification that WHO uses (see https://en.wikipedia.org/wiki/Body_mass_index#Categories).

| Weight (kg) | Height (m) | CDDA (L) | CDDA Simple (L) | BMI Model (L) | Brozak Model (L) | Siri Model (L) | Classification    |
|-------------|------------|----------|-----------------|---------------|------------------|----------------|-------------------|
|          25 |        0.7 |     4.48 |           23.22 |         25.55 |            25.39 |          25.53 | Obese (Class III) |
|          25 |        1.0 |    13.06 |           23.30 |         23.96 |            24.11 |          24.14 | Overweight        |
|          25 |       1.22 |    23.72 |           23.37 |         23.50 |            23.77 |          23.76 | Moderate thinness |
|          25 |        1.5 |    44.08 |           23.44 |         23.19 |            23.54 |          23.52 | Severe thinness   |
|          25 |       1.75 |    70.00 |           23.51 |         23.04 |            23.43 |          23.40 | Severe thinness   |
|          25 |        2.0 |   104.49 |           23.59 |         22.93 |            23.35 |          23.32 | Severe thinness   |
|          25 |       2.27 |   152.78 |           23.66 |         22.86 |            23.30 |          23.26 | Severe thinness   |
|          25 |        2.8 |   286.72 |           23.82 |         22.78 |            23.24 |          23.19 | Severe thinness   |

| Weight (kg) | Height (m) | CDDA (L) | CDDA Simple (L) | BMI Model (L) | Brozak Model (L) | Siri Model (L) | Classification    |
|-------------|------------|----------|-----------------|---------------|------------------|----------------|-------------------|
|          40 |        0.7 |     4.48 |           37.38 |         44.35 |            43.79 |          44.34 | Obese (Class III) |
|          40 |        1.0 |    13.06 |           37.51 |         39.77 |            39.70 |          39.84 | Obese (Class III) |
|          40 |       1.22 |    23.72 |           37.61 |         38.51 |            38.72 |          38.77 | Overweight        |
|          40 |        1.5 |    44.08 |           37.74 |         37.69 |            38.09 |          38.09 | Mild thinness     |
|          40 |       1.75 |    70.00 |           37.86 |         37.28 |            37.79 |          37.76 | Severe thinness   |
|          40 |        2.0 |   104.49 |           37.97 |         37.01 |            37.60 |          37.55 | Severe thinness   |
|          40 |       2.27 |   152.78 |           38.10 |         36.82 |            37.46 |          37.41 | Severe thinness   |
|          40 |        2.8 |   286.72 |           38.34 |         36.60 |            37.30 |          37.23 | Severe thinness   |

| Weight (kg) | Height (m) | CDDA (L) | CDDA Simple (L) | BMI Model (L) | Brozak Model (L) | Siri Model (L) | Classification    |
|-------------|------------|----------|-----------------|---------------|------------------|----------------|-------------------|
|          55 |        0.7 |     4.48 |           51.70 |         66.62 |            66.32 |          67.82 | Obese (Class III) |
|          55 |        1.0 |    13.06 |           51.89 |         56.80 |            56.36 |          56.72 | Obese (Class III) |
|          55 |       1.22 |    23.72 |           52.02 |         54.27 |            54.26 |          54.43 | Obese (Class II)  |
|          55 |        1.5 |    44.08 |           52.20 |         52.65 |            53.00 |          53.05 | Normal            |
|          55 |       1.75 |    70.00 |           52.36 |         51.85 |            52.39 |          52.40 | Mild thinness     |
|          55 |        2.0 |   104.49 |           52.52 |         51.34 |            52.02 |          51.99 | Severe thinness   |
|          55 |       2.27 |   152.78 |           52.70 |         50.97 |            51.75 |          51.70 | Severe thinness   |
|          55 |        2.8 |   286.72 |           53.04 |         50.54 |            51.44 |          51.37 | Severe thinness   |

| Weight (kg) | Height (m) | CDDA (L) | CDDA Simple (L) | BMI Model (L) | Brozak Model (L) | Siri Model (L) | Classification    |
|-------------|------------|----------|-----------------|---------------|------------------|----------------|-------------------|
|          70 |        0.7 |     4.48 |           66.17 |         93.44 |            96.17 |          99.84 | Obese (Class III) |
|          70 |        1.0 |    13.06 |           66.41 |         75.19 |            74.32 |          75.04 | Obese (Class III) |
|          70 |       1.22 |    23.72 |           66.59 |         70.83 |            70.50 |          70.84 | Obese (Class III) |
|          70 |        1.5 |    44.08 |           66.82 |         68.09 |            68.29 |          68.43 | Obese (Class I)   |
|          70 |       1.75 |    70.00 |           67.02 |         66.76 |            67.26 |          67.31 | Normal            |
|          70 |        2.0 |   104.49 |           67.23 |         65.91 |            66.63 |          66.63 | Mild thinness     |
|          70 |       2.27 |   152.78 |           67.45 |         65.31 |            66.19 |          66.15 | Severe thinness   |
|          70 |        2.8 |   286.72 |           67.90 |         64.61 |            65.68 |          65.60 | Severe thinness   |

| Weight (kg) | Height (m) | CDDA (L) | CDDA Simple (L) | BMI Model (L) | Brozak Model (L) | Siri Model (L) | Classification    |
|-------------|------------|----------|-----------------|---------------|------------------|----------------|-------------------|
|          85 |        0.7 |     4.48 |           80.79 |        126.35 |           140.84 |         150.07 | Obese (Class III) |
|          85 |        1.0 |    13.06 |           81.08 |         95.13 |            93.93 |          95.20 | Obese (Class III) |
|          85 |       1.22 |    23.72 |           81.30 |         88.25 |            87.51 |          88.11 | Obese (Class III) |
|          85 |        1.5 |    44.08 |           81.58 |         84.04 |            84.00 |          84.26 | Obese (Class II)  |
|          85 |       1.75 |    70.00 |           81.84 |         82.02 |            82.40 |          82.53 | Overweight        |
|          85 |        2.0 |   104.49 |           82.09 |         80.75 |            81.44 |          81.48 | Normal            |
|          85 |       2.27 |   152.78 |           82.36 |         79.85 |            80.77 |          80.75 | Moderate thinness |
|          85 |        2.8 |   286.72 |           82.91 |         78.81 |            80.00 |          79.92 | Severe thinness   |

| Weight (kg) | Height (m) | CDDA (L) | CDDA Simple (L) | BMI Model (L) | Brozak Model (L) | Siri Model (L) | Classification    |
|-------------|------------|----------|-----------------|---------------|------------------|----------------|-------------------|
|         100 |        0.7 |     4.48 |           95.54 |        167.69 |           200.00 |         200.00 | Obese (Class III) |
|         100 |        1.0 |    13.06 |           95.90 |        116.81 |           115.64 |         117.74 | Obese (Class III) |
|         100 |       1.22 |    23.72 |           96.16 |        106.61 |           105.44 |         106.39 | Obese (Class III) |
|         100 |        1.5 |    44.08 |           96.49 |        100.53 |           100.16 |         100.60 | Obese (Class III) |
|         100 |       1.75 |    70.00 |           96.79 |         97.64 |            97.84 |          98.07 | Obese (Class I)   |
|         100 |        2.0 |   104.49 |           97.09 |         95.85 |            96.46 |          96.56 | Overweight        |
|         100 |       2.27 |   152.78 |           97.42 |         94.59 |            95.50 |          95.52 | Normal            |
|         100 |        2.8 |   286.72 |           98.07 |         93.13 |            94.42 |          94.35 | Severe thinness   |

| Weight (kg) | Height (m) | CDDA (L) | CDDA Simple (L) | BMI Model (L) | Brozak Model (L) | Siri Model (L) | Classification    |
|-------------|------------|----------|-----------------|---------------|------------------|----------------|-------------------|
|         115 |        0.7 |     4.48 |          110.43 |        221.18 |           230.00 |         230.00 | Obese (Class III) |
|         115 |        1.0 |    13.06 |          110.84 |        140.48 |           140.08 |         143.42 | Obese (Class III) |
|         115 |       1.22 |    23.72 |          111.14 |        125.98 |           124.41 |         125.84 | Obese (Class III) |
|         115 |        1.5 |    44.08 |          111.53 |        117.58 |           116.83 |         117.49 | Obese (Class III) |
|         115 |       1.75 |    70.00 |          111.87 |        113.64 |           113.59 |         113.95 | Obese (Class II)  |
|         115 |        2.0 |   104.49 |          112.22 |        111.23 |           111.69 |         111.88 | Overweight        |
|         115 |       2.27 |   152.78 |          112.60 |        109.53 |           110.39 |         110.47 | Normal            |
|         115 |        2.8 |   286.72 |          113.36 |        107.57 |           108.93 |         108.89 | Severe thinness   |

| Weight (kg) | Height (m) | CDDA (L) | CDDA Simple (L) | BMI Model (L) | Brozak Model (L) | Siri Model (L) | Classification    |
|-------------|------------|----------|-----------------|---------------|------------------|----------------|-------------------|
|         130 |        0.7 |     4.48 |          125.43 |        260.00 |             0.00 |           0.00 | Obese (Class III) |
|         130 |        1.0 |    13.06 |          125.90 |        166.41 |           168.20 |         173.37 | Obese (Class III) |
|         130 |       1.22 |    23.72 |          126.24 |        146.45 |           144.63 |         146.68 | Obese (Class III) |
|         130 |        1.5 |    44.08 |          126.69 |        135.21 |           134.05 |         134.98 | Obese (Class III) |
|         130 |       1.75 |    70.00 |          127.08 |        130.04 |           129.68 |         130.20 | Obese (Class III) |
|         130 |        2.0 |   104.49 |          127.48 |        126.89 |           127.16 |         127.45 | Obese (Class I)   |
|         130 |       2.27 |   152.78 |          127.92 |        124.68 |           125.45 |         125.59 | Overweight        |
|         130 |        2.8 |   286.72 |          128.78 |        122.15 |           123.54 |         123.52 | Moderate thinness |

| Weight (kg) | Height (m) | CDDA (L) | CDDA Simple (L) | BMI Model (L) | Brozak Model (L) | Siri Model (L) | Classification    |
|-------------|------------|----------|-----------------|---------------|------------------|----------------|-------------------|
|         145 |        0.7 |     4.48 |          140.55 |        290.00 |             0.00 |           0.00 | Obese (Class III) |
|         145 |        1.0 |    13.06 |          141.07 |        194.95 |           201.38 |         209.36 | Obese (Class III) |
|         145 |       1.22 |    23.72 |          141.46 |        168.11 |           166.30 |         169.18 | Obese (Class III) |
|         145 |        1.5 |    44.08 |          141.96 |        153.47 |           151.87 |         153.14 | Obese (Class III) |
|         145 |       1.75 |    70.00 |          142.41 |        146.84 |           146.12 |         146.84 | Obese (Class III) |
|         145 |        2.0 |   104.49 |          142.86 |        142.83 |           142.86 |         143.27 | Obese (Class II)  |
|         145 |       2.27 |   152.78 |          143.34 |        140.04 |           140.67 |         140.89 | Overweight        |
|         145 |        2.8 |   286.72 |          144.31 |        136.86 |           138.26 |         138.27 | Mild thinness     |

