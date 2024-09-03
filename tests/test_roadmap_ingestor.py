import pytest
from datetime import datetime
import json
from src import roadmap_output_ingestor as rp


@pytest.fixture
def mock_raw_data():
    return {
        "data": {
            "Address": "Anonymous",
            "City": "Transilvainia",
            "MaritalStatus": 2,
            "State": "CA",
            "Zip": "90123",
            "Primary_Age": 58,
            "Primary_BirthDate": "1966-06-06T00:00:00",
            "Primary_Blind": False,
            "Primary_Email": "anonymous@rssa.com",
            "Primary_FirstName": "John",
            "Primary_GenderID": "M",
            "Primary_LastName": "Doe",
            "Primary_Phone": "Anonymous",
            "Spouse_Age": 59,
            "Spouse_BirthDate": "1965-05-05T00:00:00",
            "Spouse_Blind": False,
            "Spouse_Email": "anonymous@rssa.com",
            "Spouse_FirstName": "Jane",
            "Spouse_GenderID": "F",
            "Spouse_LastName": "Doe",
            "Spouse_Phone": "Anonymous",
            "SSCalData": {
                "Primary_HasFullCoverage": True,
                "Primary_IsDisabled": False,
                "Primary_Blind": False,
                "Primary_HasChildren": False,
                "Primary_HasPension": False,
                "Primary_IsCollectingBenefits": False,
                "Primary_IsRemarried": True,
                "Primary_MarriedBefore60": True,
                "Primary_MarriedOver10Years": True,
                "Primary_CalBasis": 0,
                "Primary_EstRetirementAge": 0,
                "Primary_HowCalBenefits": 2,
                "Primary_BenefitsStartDate": None,
                "Primary_DivorceDate": "2020-05-18T04:00:00",
                "Primary_EntitlementDate": None,
                "Primary_FRA": "2033-06-05T00:00:00",
                "Primary_AnualEarningRate": 50000.0000,
                "Primary_AnualPartTimeEarningRate": 0.0000,
                "Primary_BenefitsAmount": None,
                "Primary_DisabilityBenefit": None,
                "Primary_PenAmount": None,
                "Primary_PenSalarySS": None,
                "Primary_PIA": 390.6000,
                "Primary_PIA62": 390.6000,
                "Primary_PIA70": 390.6000,
                "Primary_QEAvgSalary": None,
                "Primary_SSPIA": 0.0000,
                "Primary_SSEarning": None,
                "Primary_WEPBendRate": 0.0000,
                "Primary_FRAAge": 67,
                "Primary_FRAYear": 804,
                "Primary_LastYearEarningsAge": 56,
                "Primary_LastYearPartTimeEarningsAge": 0,
                "Primary_LifeExpectancy": 85,
                "Primary_QEYearsWorked": None,
                "Spouse_HasFullCoverage": True,
                "Spouse_IsDisabled": False,
                "Spouse_Blind": False,
                "Spouse_HasPension": False,
                "Spouse_IsCollectingBenefits": False,
                "Spouse_IsLiving": True,
                "Spouse_CalBasis": 0,
                "Spouse_EstRetirementAge": 0,
                "Spouse_HowCalBenefits": 2,
                "Spouse_BenefitsStartDate": None,
                "Spouse_DeathDate": None,
                "Spouse_EntitlementDate": None,
                "Spouse_FRA": "2032-05-04T00:00:00",
                "Spouse_AnualEarningRate": 60000.0000,
                "Spouse_AnualIncome": None,
                "Spouse_AnualPartTimeEarningRate": 0.0000,
                "Spouse_BenefitAmount": None,
                "Spouse_DisabilityBenefit": None,
                "Spouse_PenAmount": None,
                "Spouse_PenSalarySS": None,
                "Spouse_PIA": 282.6000,
                "Spouse_PIA62": 282.6000,
                "Spouse_PIA70": 282.6000,
                "Spouse_QEAvgSalary": None,
                "Spouse_SSPIA": 1560.0000,
                "Spouse_SSEarning": None,
                "Spouse_WEPBendRate": 0.0000,
                "Spouse_FRAAge": 67,
                "Spouse_FRAYear": 804,
                "Spouse_LastYearEarningsAge": 0,
                "Spouse_LastYearPartTimeEarningsAge": 0,
                "Spouse_LifeExpectancy": 90,
                "Spouse_QEYearsWorked": None,
                "SSCalChildren": [
                    {
                        "Name": "Junior Doe",
                        "BirthDate": "2000-01-01T00:00:00",
                        "Age": 23,
                        "HighSchoolGradDate": "2018-06-01T00:00:00",
                        "IsCollectingBenefits": False,
                        "IsDisabled": False,
                    }
                ],
                "SSCalEarnings": [
                    {"YearID": 2022, "IsPrimary": True, "Earning": 50000},
                    {"YearID": 2022, "IsPrimary": False, "Earning": 45000},
                    {"YearID": 2021, "IsPrimary": True, "Earning": 48000},
                    {"YearID": 2021, "IsPrimary": False, "Earning": 43000},
                ],
                "SSCalPensions": [
                    {
                        "Title": "Company Pension",
                        "AnnualAmount": 12000,
                        "LumpSumAmount": None,
                        "StartYear": 2025,
                        "ExemptFromGPO": False,
                    }
                ],
            },
            "Settings": {
                "COLA": 2.0,
                "InflationRate": 2.5,
                "NominalRateOfReturn": 6.0,
                "RealRateOfReturn": 3.5,
            },
        }
    }


def test_get_primary(mock_raw_data):
    primary = rp.get_primary(mock_raw_data)
    assert primary["name"] == "John Doe"


def test_get_spouse(mock_raw_data):
    spouse = rp.get_spouse(mock_raw_data)
    assert spouse["name"] == "Jane Doe"
