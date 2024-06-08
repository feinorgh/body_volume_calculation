#!/usr/bin/env python3
"""Outputs data to compare various algorithms
   for calculating human body volume

   The calculations in here are taken from
   * https://en.wikipedia.org/wiki/Body_fat_percentage

"""

import matplotlib.pyplot as plt
import numpy as np


def get_body_density(body_fat_ratio=0.12):
    """Returns the average body density in kg / L

    This estimation seems to relate well to real world examples

    See:
        Heymsfield SB, Wang J, Kehayias J, Heshka S, Lichtman S, Pierson RN Jr. Chemical determination of human body density in vivo: relevance to hydrodensitometry. Am J Clin Nutr. 1989 Dec;50(6):1282-9. doi: 10.1093/ajcn/50.6.1282. PMID: 2596420.
    """
    density_fat = 0.9  # kg / L
    density_water = 1.0  # kg / L
    density_protein = 1.35  # kg / L

    # figures below are mass ratios to a typical human cell
    lipids = 0.12
    water = 0.65
    protein = 0.20
    other = 0.03

    lipids_adj = lipids * (body_fat_ratio / lipids)

    fat_free_total = water + protein + other
    non_fat_ratio = (1.0 - lipids_adj) / fat_free_total

    water_adj = water * non_fat_ratio
    protein_adj = protein * non_fat_ratio
    other_adj = other * non_fat_ratio

    # we assume that 'other' has the same density as water
    return (
        lipids_adj * density_fat
        + water_adj * density_water
        + other_adj * density_water
        + protein_adj * density_protein
    )


def get_examples():
    """Gets a list of examples to calculate the values on"""
    examples = []
    for weight in range(35, 200, 5):  # units in kg
        for height in range(85, 255, 10):
            height_m = height / 100  # we want the units in m
            bmi = get_bmi(height_m, weight)
            bfr_bmi = get_bmi_body_fat_ratio(bmi)
            density = get_body_density(bfr_bmi)
            bfr_brozak = get_brozak_body_fat_ratio(density)
            bfr_siri   = get_siri_body_fat_ratio(density)
            bmi_volume = get_bmi_body_volume(height_m, weight)
            brozak_volume = get_brozak_body_volume(height_m, weight)
            siri_volume = get_siri_body_volume(height_m, weight)
            examples.append(
                {
                    "weight": weight,
                    "height": height_m,
                    "bmi": bmi,
                    "bfr_bmi": bfr_bmi,
                    "bfr_brozak": bfr_brozak,
                    "bfr_siri": bfr_siri,
                    "density": density,
                    "bmi_volume": bmi_volume,
                    "brozak_volume": brozak_volume,
                    "siri_volume": siri_volume
                }
            )
    return examples


def get_brozak_body_fat_ratio(density):
    """Gets the body fat ratio (Brozak) for a given density (in g/cm^3)"""
    return 4.57 / density - 4.142


def get_brozak_body_volume(height, weight, gender="male", age=30):
    """Gets the body volume in L using the Brozak formula for body/fat ratio, where
        height in m
        weight in kg
        gender is "male", "female", or "fluid"
        age in years
    """
    bmi = get_bmi(height, weight)
    bfr = get_bmi_body_fat_ratio(bmi, gender, age)
    density = get_body_density(bfr)
    bfr_brozak = get_brozak_body_fat_ratio(density)
    density = get_body_density(bfr_brozak)
    volume = weight * density
    if volume < 0 or volume > weight * 2:
        return 0
    return volume


def get_siri_body_fat_ratio(density):
    """Gets the body fat ratio (Siri) for a given density (in g/cm^3)"""
    return 4.95 / density - 4.50


def get_siri_body_volume(height, weight, gender="male", age=30):
    """Gets the body volume in L using the Siri formula for body/fat ratio
        height in m
        weight in kg
        gender is "male", "female", or "fluid"
        age in years
    """
    bmi = get_bmi(height, weight)
    bfr = get_bmi_body_fat_ratio(bmi, gender, age)
    density = get_body_density(bfr)
    bfr_siri = get_siri_body_fat_ratio(density)
    density = get_body_density(bfr_siri)
    volume = weight * density
    if volume < 0 or volume > weight * 2:
        return 0
    return volume


def get_bmi_body_fat_ratio(bmi=20, gender="Male", age=30):
    """Gets the body fat ratio from the BMI, where
        bmi is body mass index (float)
        gender is "Male", "Female", or "Fluid"
        age is in years (integer)
    """
    gender_contrib = 0
    if gender.lower() == "male":
        gender_contrib = 1
    if gender.lower() == "fluid":
        gender_contrib = 0.5

    return ((1.39 * bmi) + (0.16 * age) - (10.34 * gender_contrib) - 9) / 100


def get_bmi_body_volume(height, weight, gender="male", age=30):
    """Gets the body volume using BMI for body/fat ratio where:
        height in m
        weight in kg
        gender is "Male" or "Female" or "Fluid"
        age is in years
    """
    bmi = get_bmi(height, weight)
    bfr = get_bmi_body_fat_ratio(bmi, gender, age)
    density = get_body_density(bfr)
    volume = weight * density
    if volume > weight * 2:
        return weight * 2
    if volume < 0:
        return 0
    return volume


def get_cdda_original_volume(height):
    """Returns the volume in L for the original CDDA calculation, where
        height is in m
    """
    avg_human_volume = 70
    your_height = height * 100
    base_volume = your_height / 2.5
    proportional_volume = base_volume / avg_human_volume
    return pow(proportional_volume, 3.0) * avg_human_volume


def get_bmi(height, weight):
    """Gets the BMI for a given height and weight
    weight is in kg
    height is in m
    """
    return weight / pow(height, 2)


def get_bmi_category(bmi):
    """Returns a string with the BMI basic category"""
    if bmi >= 40.0:
        return "Obese (Class III)"
    if bmi >= 35.0:
        return "Obese (Class II)"
    if bmi >= 30.0:
        return "Obese (Class I)"
    if bmi >= 25.0:
        return "Overweight"
    if bmi >= 18.5:
        return "Normal"
    if bmi >= 17.0:
        return "Mild thinness"
    if bmi >= 16.0:
        return "Moderate thinness"
    return "Severe thinness"


def make_3d_plot():
    """Make a 3D plot with heights, weights, and models"""

    weights = range(25, 200, 10)
    heights = [x / 100 for x in range(75, 230, 10)]
    age = 30
    gender = "male"

    ax = plt.figure().add_subplot(projection="3d")

    for height in heights:
        volumes = []
        for weight in weights:
            volume = get_bmi_body_volume(height, weight, gender, age)
            volumes.append(volume)
        ax.plot(weights, volumes, height, "r")

    for height in heights:
        volumes = []
        for weight in weights:
            volume = get_brozak_body_volume(height, weight, gender, age)
            volumes.append(volume)
        ax.plot(weights, volumes, height, "b")

    for height in heights:
        volumes = []
        for weight in weights:
            volume = get_siri_body_volume(height, weight, gender, age)
            volumes.append(volume)
        ax.plot(weights, volumes, height, "y")

    for height in heights:
        volumes = []
        for weight in weights:
            volume = get_cdda_original_volume(height)
            volumes.append(volume)
        ax.plot(weights, volumes, height, color="g")

    ax.set_xlabel("Weight (kg)")
    ax.set_ylabel("Volume (L)")
    ax.set_zlabel("Height (m)")
    ax.set_title("Comparison of Body Volume Models")
    plt.show()


def print_comparison_table():
    """Prints a comparison table between different models"""
    for weight in range(25, 150, 15):
        print("| Weight (kg) | Height (m) | CDDA (L) | BMI Model (L) | Brozak Model (L) | Siri Model (L) | Classification    |")
        print("|-------------|------------|----------|---------------|------------------|----------------|-------------------|")
        for height in [0.7, 1.22, 1.75, 2.27, 2.8]:
            orig = get_cdda_original_volume(height)
            bmi = get_bmi_body_volume(height, weight)
            brozak = get_brozak_body_volume(height, weight)
            siri = get_siri_body_volume(height, weight)
            classification = get_bmi_category(get_bmi(height, weight))
            print(f"| {weight: >11} | {height:>10} | {orig:>8.2f} | {bmi:>13.2f} | {brozak:>16.2f} | {siri:>14.2f} | {classification:<17} |")
        print("")

def main():
    print_comparison_table()
    make_3d_plot()


if __name__ == "__main__":
    main()
