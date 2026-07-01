import csv


def generate_capital_allocation_csv(data, output_file):
    """
    Generate Capital Allocation CSV.

    Parameters:
        data: List of dictionaries
        output_file: Output CSV file path
    """

    with open(output_file, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "company_id",
            "year",
            "cfo_sign",
            "cfi_sign",
            "cff_sign",
            "pattern_label"
        ])

        for row in data:
            writer.writerow([
                row["company_id"],
                row["year"],
                row["cfo_sign"],
                row["cfi_sign"],
                row["cff_sign"],
                row["pattern_label"]
            ])