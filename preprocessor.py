def preprocess_data(data):
    processed_data = []

    # Process primary person data
    primary = {
        "Name": f"{data['Primary_FirstName']} {data['Primary_LastName']}",
        "Age": data["Primary_Age"],
        "Gender": data["Primary_GenderID"],
        "PIA": data["SSCalData"]["Primary_PIA"],
        "FRA": data["SSCalData"]["Primary_FRA"],
        "EstRetirementAge": data["SSCalData"]["Primary_EstRetirementAge"],
    }
    processed_data.append(primary)

    # Process spouse data
    spouse = {
        "Name": f"{data['Spouse_FirstName']} {data['Spouse_LastName']}",
        "Age": data["Spouse_Age"],
        "Gender": data["Spouse_GenderID"],
        "PIA": data["SSCalData"]["Spouse_PIA"],
        "FRA": data["SSCalData"]["Spouse_FRA"],
        "EstRetirementAge": data["SSCalData"]["Spouse_EstRetirementAge"],
    }
    processed_data.append(spouse)

    # Process earnings data
    for earning in data["SSCalData"]["SSCalEarnings"]:
        person = "Primary" if earning["IsPrimary"] == 1 else "Spouse"
        processed_data.append(
            {
                "Person": person,
                "Year": earning["YearID"],
                "Earning": earning["Earning"],
            }
        )

    return processed_data

