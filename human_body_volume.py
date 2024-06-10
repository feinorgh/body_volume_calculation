#!/usr/bin/env python3
"""Outputs data to compare various algorithms
   for calculating human body volume

   The calculations in here are taken from
   * https://en.wikipedia.org/wiki/Body_fat_percentage

"""

import matplotlib.pyplot as plt


def get_body_density(body_fat_ratio=0.12):
    """Returns the average body density in kg / L

    body_fat_ratio is the ratio to 1.0 of body fat

    This estimation seems to relate well to real world examples

    See:
        Heymsfield SB, Wang J, Kehayias J, Heshka S, Lichtman S, Pierson RN Jr.
        Chemical determination of human body density in vivo: relevance to
        hydrodensitometry. Am J Clin Nutr. 1989 Dec;50(6):1282-9.
        doi: 10.1093/ajcn/50.6.1282. PMID: 2596420.
    """

    density_fat = 0.9  # kg / L
    density_water = 1.0  # kg / L
    density_protein = 1.35  # kg / L

    # figures below are mass ratios to a typical human cell (lipids: 0.12)
    water = 0.65
    protein = 0.20
    other = 0.03

    non_fat_ratio = 1.0 - body_fat_ratio

    water_adj = water * non_fat_ratio
    protein_adj = protein * non_fat_ratio
    other_adj = other * non_fat_ratio
    lipids_adj = body_fat_ratio

    # we assume that 'other' has the same density as water
    return {
        "average_density": (
            lipids_adj * density_fat
            + water_adj * density_water
            + other_adj * density_water
            + protein_adj * density_protein
        )
        / (lipids_adj + water_adj + other_adj + protein_adj),
        "proportions": {
            "lipids": lipids_adj,
            "water": water_adj,
            "protein": protein_adj,
            "other": other_adj,
        },
    }


def get_examples():
    """Gets a list of examples to calculate the values on"""
    examples = []
    for weight in range(35, 200, 5):  # units in kg
        for height in range(85, 255, 10):
            height_m = height / 100  # we want the units in m
            bmi = get_bmi(height_m, weight)
            bfr_bmi = get_bmi_body_fat_ratio(bmi)
            density = get_body_density(bfr_bmi)
            avg_density = density.get("average_density")
            bfr_brozek = get_brozek_body_fat_ratio(avg_density)
            bfr_siri = get_siri_body_fat_ratio(avg_density)
            bmi_volume = get_bmi_body_volume(height_m, weight)
            brozek_volume = get_brozek_body_volume(height_m, weight)
            siri_volume = get_siri_body_volume(height_m, weight)
            examples.append(
                {
                    "weight": weight,
                    "height": height_m,
                    "bmi": bmi,
                    "bfr_bmi": bfr_bmi,
                    "bfr_brozek": bfr_brozek,
                    "bfr_siri": bfr_siri,
                    "density": density,
                    "bmi_volume": bmi_volume,
                    "brozek_volume": brozek_volume,
                    "siri_volume": siri_volume,
                }
            )
    return examples


def get_brozek_body_fat_ratio(density):
    """Gets the body fat ratio (Brozek) for a given density (in g/cm^3)"""
    return 4.57 / density - 4.142


def get_brozek_body_volume(height, weight, gender="male", age=30):
    """Gets the body volume in L using the Brozek formula for
    body/fat ratio, where
    height in m
    weight in kg
    gender is "male", "female", or "fluid"
    age in years
    """
    bmi = get_bmi(height, weight)
    bfr = get_bmi_body_fat_ratio(bmi, gender, age)
    density = get_body_density(bfr)
    avg_density = density.get("average_density")
    bfr_brozek = get_brozek_body_fat_ratio(avg_density)
    density = get_body_density(bfr_brozek)
    avg_density = density.get("average_density")
    volume = weight / avg_density
    if volume < 0 or volume > weight * 2:
        volume = 0
    return {"volume": volume, "proportions": density.get("proportions")}


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
    avg_density = density.get("average_density")
    bfr_siri = get_siri_body_fat_ratio(avg_density)
    density = get_body_density(bfr_siri)
    avg_density = density.get("average_density")
    volume = weight / avg_density
    if volume < 0 or volume > weight * 2:
        volume = 0
    return {"volume": volume, "proportions": density.get("proportions")}


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
    avg_density = density.get("average_density")
    volume = weight / avg_density
    if volume < 0 or volume > weight * 2:
        volume = 0
    return {"volume": volume, "proportions": density.get("proportions")}


def get_cdda_original_volume(height):
    """Returns the volume in L for the original CDDA calculation, where
    height is in m
    """
    avg_human_volume = 70
    your_height = height * 100
    base_volume = your_height / 2.5
    proportional_volume = base_volume / avg_human_volume
    return pow(proportional_volume, 3.0) * avg_human_volume


def get_cdda_simple_brozek_volume(height, weight):
    """Returns the volume in L for the (simplified) Brozek based formula, where
    height is in m
    weight is in kg
    """
    height_cm = height * 100
    density = (
        1.097
        - 0.00046971 * weight
        + 0.00000056 * pow(weight, 2)
        - 0.00012828 * height_cm
    )
    volume = weight / density
    return volume


def get_bmi(height, weight):
    """Gets the BMI for a given height and weight
    weight is in kg
    height is in m
    """
    return weight / pow(height, 2)


def get_bmi_category(bmi):
    """Returns a string with the BMI basic category"""
    classification = "Severe thinness"
    if bmi >= 40.0:
        classification = "Obese (Class III)"
    elif bmi >= 35.0:
        classification = "Obese (Class II)"
    elif bmi >= 30.0:
        classification = "Obese (Class I)"
    elif bmi >= 25.0:
        classification = "Overweight"
    elif bmi >= 18.5:
        classification = "Normal"
    elif bmi >= 17.0:
        classification = "Mild thinness"
    elif bmi >= 16.0:
        classification = "Moderate thinness"
    return classification


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
            volumes.append(volume.get("volume"))
        ax.plot(weights, volumes, height, "r")

    for height in heights:
        volumes = []
        for weight in weights:
            volume = get_brozek_body_volume(height, weight, gender, age)
            volumes.append(volume.get("volume"))
        ax.plot(weights, volumes, height, "b")

    for height in heights:
        volumes = []
        for weight in weights:
            volume = get_siri_body_volume(height, weight, gender, age)
            volumes.append(volume.get("volume"))
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


def format_proportions(prop):
    """Formats proportions in a compact way"""
    string = ""
    for k, v in prop.items():
        string += f"{k[0].upper()}:{v:.2f} "
    return string.strip()


def print_comparison_table():
    """Prints a comparison table between different models"""
    for weight in range(25, 220, 15):
        titles = [
            "m(kg)",
            "h(m)",
            "CDDA(L)",
            "Simple(L)",
            "BMI(L)",
            "BMI(P) fat/water/protein/other",
            "Brozek(L)",
            "Brozek(P) fat/water/protein/other",
            "Siri(L)",
            "Siri(P) fat/water/protein/other",
        ]
        length = {}
        for title in titles:
            print(f"| {title} ", end="")
            length[title] = len(title)
        print(f"| Category{' '*9} |")
        for title in titles:
            print(f"|{'-'*(length[title]+2)}", end="")
        print(f"|{'-'*19}|")
        # 0.55 m is the height of the world's shortest human,
        # Chandra Bahadur Dangi, weight unknown.
        #   https://en.wikipedia.org/wiki/Chandra_Bahadur_Dangi
        # 2.72 m (8'11") is the tallest human ever in existence,
        # Robert Wadlow. his adult weight was 199 kg / 439 lb
        #   https://en.wikipedia.org/wiki/Robert_Wadlow
        # 1.62 m is the average female height worldwide
        # 1.75 m is the average male height worldwide
        for height in [
            0.55,
            0.7,
            1.0,
            1.22,
            1.50,
            1.62,
            1.75,
            2.00,
            2.27,
            2.72,
            2.8,
        ]:
            bmi = get_bmi_body_volume(height, weight)
            brozek = get_brozek_body_volume(height, weight)
            siri = get_siri_body_volume(height, weight)
            values = {
                "CDDA(L)": get_cdda_original_volume(height),
                "Simple(L)": get_cdda_simple_brozek_volume(height, weight),
                "BMI(L)": bmi.get("volume"),
                "BMI(P) fat/water/protein/other": bmi.get("proportions"),
                "Brozek(L)": brozek.get("volume"),
                "Brozek(P) fat/water/protein/other": brozek.get(
                    "proportions"
                ),
                "Siri(L)": siri.get("volume"),
                "Siri(P) fat/water/protein/other": siri.get("proportions"),
            }
            print(f"| {weight:>5} | {height:>4.2f} ", end="")
            for k, v in values.items():
                if k.endswith("other"):
                    print(f"| {format_proportions(v):^{len(k)}} ", end="")
                else:
                    print(f"| {v:>{len(k)}.2f} ", end="")
            print(f"| {get_bmi_category(get_bmi(height, weight)):^17} |")
        print("")


def main():
    """Prints a comparison table and makes a 3D plot of the formulas"""
    print_comparison_table()
    make_3d_plot()


if __name__ == "__main__":
    main()
