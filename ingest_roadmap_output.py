import json
from datetime import datetime


def preprocess_roadmap_output(file_path):
    with open(file_path, "r", encoding="utf-8-sig") as f:
        data = json.load(f)

    # Extract primary and spouse information
    primary = {
        "name": f"{data['Primary_FirstName']} {data['Primary_LastName']}",
        "birth_date": datetime.strptime(data["Primary_BirthDate"], "%Y-%m-%dT%H:%M:%S"),
        "age": data["Primary_Age"],
        "gender": data["Primary_GenderID"],
        "pia": data["SSCalData"]["Primary_PIA"],
        "fra": datetime.strptime(data["SSCalData"]["Primary_FRA"], "%Y-%m-%d %H:%M:%S"),
        "fra_age": data["SSCalData"]["Primary_FRAAge"],
    }

    spouse = {
        "name": f"{data['Spouse_FirstName']} {data['Spouse_LastName']}",
        "birth_date": datetime.strptime(data["Spouse_BirthDate"], "%Y-%m-%dT%H:%M:%S"),
        "age": data["Spouse_Age"],
        "gender": data["Spouse_GenderID"],
        "pia": data["SSCalData"]["Spouse_PIA"],
        "fra": datetime.strptime(data["SSCalData"]["Spouse_FRA"], "%Y-%m-%d %H:%M:%S"),
        "fra_age": data["SSCalData"]["Spouse_FRAAge"],
    }

    # Calculate earnings history
    primary_earnings = {}
    spouse_earnings = {}
    for entry in data["SSCalData"]["SSCalEarnings"]:
        if entry["IsPrimary"] == 1:
            primary_earnings[entry["YearID"]] = entry["Earning"]
        else:
            spouse_earnings[entry["YearID"]] = entry["Earning"]

    # Calculate total years worked and total earnings
    primary_years_worked = sum(
        1 for earning in primary_earnings.values() if earning > 0
    )
    primary_total_earnings = sum(primary_earnings.values())
    spouse_years_worked = sum(1 for earning in spouse_earnings.values() if earning > 0)
    spouse_total_earnings = sum(spouse_earnings.values())

    # Format the preprocessed data
    preprocessed_data = f"""
Primary Beneficiary:
Name: {primary['name']}
Date of Birth: {primary['birth_date'].strftime('%Y-%m-%d')}
Current Age: {primary['age']}
Gender: {primary['gender']}
Total Years Worked: {primary_years_worked}
Total Lifetime Earnings: ${primary_total_earnings:,.2f}
Average Annual Earnings: ${primary_total_earnings / primary_years_worked:,.2f}
Primary Insurance Amount (PIA): ${primary['pia']:,.2f}
Full Retirement Age (FRA): {primary['fra'].strftime('%Y-%m-%d')} (Age {primary['fra_age']})

Spouse:
Name: {spouse['name']}
Date of Birth: {spouse['birth_date'].strftime('%Y-%m-%d')}
Current Age: {spouse['age']}
Gender: {spouse['gender']}
Total Years Worked: {spouse_years_worked}
Total Lifetime Earnings: ${spouse_total_earnings:,.2f}
Average Annual Earnings: ${spouse_total_earnings / spouse_years_worked:,.2f}
Primary Insurance Amount (PIA): ${spouse['pia']:,.2f}
Full Retirement Age (FRA): {spouse['fra'].strftime('%Y-%m-%d')} (Age {spouse['fra_age']})

Marital Status: {"Married" if data['MaritalStatus'] == 2 else "Other"}

Primary Beneficiary Earnings History:
"""
    for year, earnings in sorted(primary_earnings.items(), reverse=True):
        preprocessed_data += f"{year}: ${earnings:,.2f}\n"

    preprocessed_data += "\nSpouse Earnings History:\n"
    for year, earnings in sorted(spouse_earnings.items(), reverse=True):
        preprocessed_data += f"{year}: ${earnings:,.2f}\n"

    return preprocessed_data

