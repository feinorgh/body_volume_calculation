# Human Body Volume Calculation (Mostly for Cataclysm: Dark Days Ahead)

This repository contains a script that uses four different models to estimate volume
of a human body.

It is by no means a guarantee that the results are accurate, or can be relied upon in any medical context.

To run the script, you need matplotlib (or just comment out the plotting business)

# Graph over relations between models and parameters

![3D Plot](Figure_1.png)

# Results

| Weight (kg) | Height (m) | CDDA (L) | BMI Model (L) | Brozak Model (L) | Siri Model (L) | Classification    |
|-------------|------------|----------|---------------|------------------|----------------|-------------------|
|          25 |        0.7 |     4.48 |         24.46 |            24.61 |          24.48 | Obese (Class III) |
|          25 |       1.22 |    23.72 |         26.59 |            26.30 |          26.30 | Moderate thinness |
|          25 |       1.75 |    70.00 |         27.13 |            26.68 |          26.71 | Severe thinness   |
|          25 |       2.27 |   152.78 |         27.34 |            26.82 |          26.87 | Severe thinness   |
|          25 |        2.8 |   286.72 |         27.44 |            26.89 |          26.95 | Severe thinness   |

| Weight (kg) | Height (m) | CDDA (L) | BMI Model (L) | Brozak Model (L) | Siri Model (L) | Classification    |
|-------------|------------|----------|---------------|------------------|----------------|-------------------|
|          40 |        0.7 |     4.48 |         36.08 |            36.54 |          36.08 | Obese (Class III) |
|          40 |       1.22 |    23.72 |         41.54 |            41.33 |          41.27 | Overweight        |
|          40 |       1.75 |    70.00 |         42.92 |            42.34 |          42.37 | Severe thinness   |
|          40 |       2.27 |   152.78 |         43.45 |            42.71 |          42.77 | Severe thinness   |
|          40 |        2.8 |   286.72 |         43.72 |            42.90 |          42.97 | Severe thinness   |

| Weight (kg) | Height (m) | CDDA (L) | BMI Model (L) | Brozak Model (L) | Siri Model (L) | Classification    |
|-------------|------------|----------|---------------|------------------|----------------|-------------------|
|          55 |        0.7 |     4.48 |         45.40 |            45.61 |          44.60 | Obese (Class III) |
|          55 |       1.22 |    23.72 |         55.74 |            55.75 |          55.58 | Obese (Class II)  |
|          55 |       1.75 |    70.00 |         58.35 |            57.74 |          57.73 | Mild thinness     |
|          55 |       2.27 |   152.78 |         59.35 |            58.45 |          58.51 | Severe thinness   |
|          55 |        2.8 |   286.72 |         59.85 |            58.80 |          58.89 | Severe thinness   |

| Weight (kg) | Height (m) | CDDA (L) | BMI Model (L) | Brozak Model (L) | Siri Model (L) | Classification    |
|-------------|------------|----------|---------------|------------------|----------------|-------------------|
|          70 |        0.7 |     4.48 |         52.44 |            50.95 |          49.08 | Obese (Class III) |
|          70 |       1.22 |    23.72 |         69.18 |            69.51 |          69.17 | Obese (Class III) |
|          70 |       1.75 |    70.00 |         73.40 |            72.85 |          72.80 | Normal            |
|          70 |       2.27 |   152.78 |         75.02 |            74.03 |          74.08 | Severe thinness   |
|          70 |        2.8 |   286.72 |         75.84 |            74.61 |          74.70 | Severe thinness   |

| Weight (kg) | Height (m) | CDDA (L) | BMI Model (L) | Brozak Model (L) | Siri Model (L) | Classification    |
|-------------|------------|----------|---------------|------------------|----------------|-------------------|
|          85 |        0.7 |     4.48 |         57.18 |            51.30 |          48.14 | Obese (Class III) |
|          85 |       1.22 |    23.72 |         81.87 |            82.56 |          82.00 | Obese (Class III) |
|          85 |       1.75 |    70.00 |         88.09 |            87.68 |          87.55 | Overweight        |
|          85 |       2.27 |   152.78 |         90.48 |            89.45 |          89.47 | Moderate thinness |
|          85 |        2.8 |   286.72 |         91.68 |            90.31 |          90.40 | Severe thinness   |

| Weight (kg) | Height (m) | CDDA (L) | BMI Model (L) | Brozak Model (L) | Siri Model (L) | Classification    |
|-------------|------------|----------|---------------|------------------|----------------|-------------------|
|         100 |        0.7 |     4.48 |         59.63 |            44.73 |          39.71 | Obese (Class III) |
|         100 |       1.22 |    23.72 |         93.80 |            94.84 |          94.00 | Obese (Class III) |
|         100 |       1.75 |    70.00 |        102.42 |           102.21 |         101.97 | Obese (Class I)   |
|         100 |       2.27 |   152.78 |        105.72 |           104.71 |         104.69 | Normal            |
|         100 |        2.8 |   286.72 |        107.38 |           105.91 |         105.98 | Severe thinness   |

| Weight (kg) | Height (m) | CDDA (L) | BMI Model (L) | Brozak Model (L) | Siri Model (L) | Classification    |
|-------------|------------|----------|---------------|------------------|----------------|-------------------|
|         115 |        0.7 |     4.48 |         59.79 |            28.18 |          20.49 | Obese (Class III) |
|         115 |       1.22 |    23.72 |        104.97 |           106.30 |         105.10 | Obese (Class III) |
|         115 |       1.75 |    70.00 |        116.37 |           116.42 |         116.06 | Obese (Class II)  |
|         115 |       2.27 |   152.78 |        120.74 |           119.80 |         119.72 | Normal            |
|         115 |        2.8 |   286.72 |        122.94 |           121.40 |         121.46 | Severe thinness   |

| Weight (kg) | Height (m) | CDDA (L) | BMI Model (L) | Brozak Model (L) | Siri Model (L) | Classification    |
|-------------|------------|----------|---------------|------------------|----------------|-------------------|
|         130 |        0.7 |     4.48 |         57.66 |             0.00 |           0.00 | Obese (Class III) |
|         130 |       1.22 |    23.72 |        115.40 |           116.85 |         115.22 | Obese (Class III) |
|         130 |       1.75 |    70.00 |        129.96 |           130.32 |         129.80 | Obese (Class III) |
|         130 |       2.27 |   152.78 |        135.55 |           134.72 |         134.57 | Overweight        |
|         130 |        2.8 |   286.72 |        138.35 |           136.79 |         136.81 | Moderate thinness |

| Weight (kg) | Height (m) | CDDA (L) | BMI Model (L) | Brozak Model (L) | Siri Model (L) | Classification    |
|-------------|------------|----------|---------------|------------------|----------------|-------------------|
|         145 |        0.7 |     4.48 |         53.23 |             0.00 |           0.00 | Obese (Class III) |
|         145 |       1.22 |    23.72 |        125.07 |           126.43 |         124.28 | Obese (Class III) |
|         145 |       1.75 |    70.00 |        143.19 |           143.88 |         143.19 | Obese (Class III) |
|         145 |       2.27 |   152.78 |        150.14 |           149.46 |         149.23 | Overweight        |
|         145 |        2.8 |   286.72 |        153.63 |           152.07 |         152.06 | Mild thinness     |

