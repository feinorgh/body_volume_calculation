# Human Body Volume Calculation (Mostly for Cataclysm: Dark Days Ahead)

This repository contains a script that uses four different models to estimate volume
of a human body.

It is by no means a guarantee that the results are accurate, or can be relied upon in any medical context.

Also, this has been an unreasonable amount of work just to prove a point, and is unnecessarily detailed.

Anyway, To run the script, you need Python3 and matplotlib (just comment out the plotting business, if you
don't want to install matplotlib)

# Graph over relations between models and parameters

![3D Plot](Figure_1.png)

The green lines are the original CDDA volume calculation (independent of weight) results for various heighs.

The red lines are the BMI model results.

The blue lines are the Brozak model results.

The yellow lines are the Siri model results.

You can examine this graph better if you run the script yourself, where you can rotate and zoom in.

The graph shows (mostly) that the more sensitive the model is for weight, the larger the difference
between low and high body weight.

It also shows that something weird is going on with the Brozak models and Siri models outside the normal
human size ranges.


# Results

Out of these models, the pure "BMI Model" (really just a simple volume = weight / density calculation) seems
to give reasonable results. The "Brozak" and "Siri" models break down when values are way outside normal
human weights and heights (other models must be used for infants, dissoluted devourers, and blobs, supposedly).

The classification is not meant to fat or thin shame anyone (real or imagined characters), but is the standard
classification that WHO uses (see https://en.wikipedia.org/wiki/Body_mass_index#Categories).


| Weight (kg) | Height (m) | CDDA (L) | BMI Model (L) | Brozak Model (L) | Siri Model (L) | Classification    |
|-------------|------------|----------|---------------|------------------|----------------|-------------------|
|          25 |        0.7 |     4.48 |         24.46 |            24.61 |          24.48 | Obese (Class III) |
|          25 |        1.0 |    13.06 |         26.08 |            25.92 |          25.89 | Overweight        |
|          25 |       1.22 |    23.72 |         26.59 |            26.30 |          26.30 | Moderate thinness |
|          25 |        1.5 |    44.08 |         26.95 |            26.55 |          26.57 | Severe thinness   |
|          25 |       1.75 |    70.00 |         27.13 |            26.68 |          26.71 | Severe thinness   |
|          25 |        2.0 |   104.49 |         27.25 |            26.76 |          26.80 | Severe thinness   |
|          25 |       2.27 |   152.78 |         27.34 |            26.82 |          26.87 | Severe thinness   |
|          25 |        2.8 |   286.72 |         27.44 |            26.89 |          26.95 | Severe thinness   |

| Weight (kg) | Height (m) | CDDA (L) | BMI Model (L) | Brozak Model (L) | Siri Model (L) | Classification    |
|-------------|------------|----------|---------------|------------------|----------------|-------------------|
|          40 |        0.7 |     4.48 |         36.08 |            36.54 |          36.08 | Obese (Class III) |
|          40 |        1.0 |    13.06 |         40.23 |            40.30 |          40.16 | Obese (Class III) |
|          40 |       1.22 |    23.72 |         41.54 |            41.33 |          41.27 | Overweight        |
|          40 |        1.5 |    44.08 |         42.45 |            42.00 |          42.00 | Mild thinness     |
|          40 |       1.75 |    70.00 |         42.92 |            42.34 |          42.37 | Severe thinness   |
|          40 |        2.0 |   104.49 |         43.23 |            42.56 |          42.60 | Severe thinness   |
|          40 |       2.27 |   152.78 |         43.45 |            42.71 |          42.77 | Severe thinness   |
|          40 |        2.8 |   286.72 |         43.72 |            42.90 |          42.97 | Severe thinness   |

| Weight (kg) | Height (m) | CDDA (L) | BMI Model (L) | Brozak Model (L) | Siri Model (L) | Classification    |
|-------------|------------|----------|---------------|------------------|----------------|-------------------|
|          55 |        0.7 |     4.48 |         45.40 |            45.61 |          44.60 | Obese (Class III) |
|          55 |        1.0 |    13.06 |         53.26 |            53.68 |          53.34 | Obese (Class III) |
|          55 |       1.22 |    23.72 |         55.74 |            55.75 |          55.58 | Obese (Class II)  |
|          55 |        1.5 |    44.08 |         57.46 |            57.08 |          57.02 | Normal            |
|          55 |       1.75 |    70.00 |         58.35 |            57.74 |          57.73 | Mild thinness     |
|          55 |        2.0 |   104.49 |         58.92 |            58.15 |          58.19 | Severe thinness   |
|          55 |       2.27 |   152.78 |         59.35 |            58.45 |          58.51 | Severe thinness   |
|          55 |        2.8 |   286.72 |         59.85 |            58.80 |          58.89 | Severe thinness   |

| Weight (kg) | Height (m) | CDDA (L) | BMI Model (L) | Brozak Model (L) | Siri Model (L) | Classification    |
|-------------|------------|----------|---------------|------------------|----------------|-------------------|
|          70 |        0.7 |     4.48 |         52.44 |            50.95 |          49.08 | Obese (Class III) |
|          70 |        1.0 |    13.06 |         65.17 |            65.93 |          65.30 | Obese (Class III) |
|          70 |       1.22 |    23.72 |         69.18 |            69.51 |          69.17 | Obese (Class III) |
|          70 |        1.5 |    44.08 |         71.96 |            71.75 |          71.61 | Obese (Class I)   |
|          70 |       1.75 |    70.00 |         73.40 |            72.85 |          72.80 | Normal            |
|          70 |        2.0 |   104.49 |         74.34 |            73.54 |          73.54 | Mild thinness     |
|          70 |       2.27 |   152.78 |         75.02 |            74.03 |          74.08 | Severe thinness   |
|          70 |        2.8 |   286.72 |         75.84 |            74.61 |          74.70 | Severe thinness   |

| Weight (kg) | Height (m) | CDDA (L) | BMI Model (L) | Brozak Model (L) | Siri Model (L) | Classification    |
|-------------|------------|----------|---------------|------------------|----------------|-------------------|
|          85 |        0.7 |     4.48 |         57.18 |            51.30 |          48.14 | Obese (Class III) |
|          85 |        1.0 |    13.06 |         75.95 |            76.92 |          75.89 | Obese (Class III) |
|          85 |       1.22 |    23.72 |         81.87 |            82.56 |          82.00 | Obese (Class III) |
|          85 |        1.5 |    44.08 |         85.97 |            86.01 |          85.74 | Obese (Class II)  |
|          85 |       1.75 |    70.00 |         88.09 |            87.68 |          87.55 | Overweight        |
|          85 |        2.0 |   104.49 |         89.47 |            88.72 |          88.67 | Normal            |
|          85 |       2.27 |   152.78 |         90.48 |            89.45 |          89.47 | Moderate thinness |
|          85 |        2.8 |   286.72 |         91.68 |            90.31 |          90.40 | Severe thinness   |

| Weight (kg) | Height (m) | CDDA (L) | BMI Model (L) | Brozak Model (L) | Siri Model (L) | Classification    |
|-------------|------------|----------|---------------|------------------|----------------|-------------------|
|         100 |        0.7 |     4.48 |         59.63 |            44.73 |          39.71 | Obese (Class III) |
|         100 |        1.0 |    13.06 |         85.61 |            86.48 |          84.93 | Obese (Class III) |
|         100 |       1.22 |    23.72 |         93.80 |            94.84 |          94.00 | Obese (Class III) |
|         100 |        1.5 |    44.08 |         99.47 |            99.84 |          99.40 | Obese (Class III) |
|         100 |       1.75 |    70.00 |        102.42 |           102.21 |         101.97 | Obese (Class I)   |
|         100 |        2.0 |   104.49 |        104.33 |           103.67 |         103.56 | Overweight        |
|         100 |       2.27 |   152.78 |        105.72 |           104.71 |         104.69 | Normal            |
|         100 |        2.8 |   286.72 |        107.38 |           105.91 |         105.98 | Severe thinness   |

| Weight (kg) | Height (m) | CDDA (L) | BMI Model (L) | Brozak Model (L) | Siri Model (L) | Classification    |
|-------------|------------|----------|---------------|------------------|----------------|-------------------|
|         115 |        0.7 |     4.48 |         59.79 |            28.18 |          20.49 | Obese (Class III) |
|         115 |        1.0 |    13.06 |         94.14 |            94.41 |          92.21 | Obese (Class III) |
|         115 |       1.22 |    23.72 |        104.97 |           106.30 |         105.10 | Obese (Class III) |
|         115 |        1.5 |    44.08 |        112.48 |           113.20 |         112.57 | Obese (Class III) |
|         115 |       1.75 |    70.00 |        116.37 |           116.42 |         116.06 | Obese (Class II)  |
|         115 |        2.0 |   104.49 |        118.90 |           118.40 |         118.21 | Overweight        |
|         115 |       2.27 |   152.78 |        120.74 |           119.80 |         119.72 | Normal            |
|         115 |        2.8 |   286.72 |        122.94 |           121.40 |         121.46 | Severe thinness   |

| Weight (kg) | Height (m) | CDDA (L) | BMI Model (L) | Brozak Model (L) | Siri Model (L) | Classification    |
|-------------|------------|----------|---------------|------------------|----------------|-------------------|
|         130 |        0.7 |     4.48 |         57.66 |             0.00 |           0.00 | Obese (Class III) |
|         130 |        1.0 |    13.06 |        101.56 |           100.48 |          97.48 | Obese (Class III) |
|         130 |       1.22 |    23.72 |        115.40 |           116.85 |         115.22 | Obese (Class III) |
|         130 |        1.5 |    44.08 |        124.99 |           126.07 |         125.21 | Obese (Class III) |
|         130 |       1.75 |    70.00 |        129.96 |           130.32 |         129.80 | Obese (Class III) |
|         130 |        2.0 |   104.49 |        133.19 |           132.91 |         132.61 | Obese (Class I)   |
|         130 |       2.27 |   152.78 |        135.55 |           134.72 |         134.57 | Overweight        |
|         130 |        2.8 |   286.72 |        138.35 |           136.79 |         136.81 | Moderate thinness |

| Weight (kg) | Height (m) | CDDA (L) | BMI Model (L) | Brozak Model (L) | Siri Model (L) | Classification    |
|-------------|------------|----------|---------------|------------------|----------------|-------------------|
|         145 |        0.7 |     4.48 |         53.23 |             0.00 |           0.00 | Obese (Class III) |
|         145 |        1.0 |    13.06 |        107.85 |           104.41 |         100.42 | Obese (Class III) |
|         145 |       1.22 |    23.72 |        125.07 |           126.43 |         124.28 | Obese (Class III) |
|         145 |        1.5 |    44.08 |        137.00 |           138.44 |         137.29 | Obese (Class III) |
|         145 |       1.75 |    70.00 |        143.19 |           143.88 |         143.19 | Obese (Class III) |
|         145 |        2.0 |   104.49 |        147.20 |           147.17 |         146.75 | Obese (Class II)  |
|         145 |       2.27 |   152.78 |        150.14 |           149.46 |         149.23 | Overweight        |
|         145 |        2.8 |   286.72 |        153.63 |           152.07 |         152.06 | Mild thinness     |

