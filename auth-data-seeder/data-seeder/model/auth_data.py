from pydantic import BaseModel
from typing import List

class DemographicLanguageField(BaseModel):
    language: str
    value: str

class DemographicsModel(BaseModel):
    id: str
    name: List[DemographicLanguageField]
    gender:List[DemographicLanguageField]
    dob: str
    phoneNumber: str
    emailId: str
    addressLine1: List[DemographicLanguageField]
    addressLine2: List[DemographicLanguageField]
    addressLine3: List[DemographicLanguageField]
    city: List[DemographicLanguageField]
    postalCode: str
    province: List[DemographicLanguageField]
    region: List[DemographicLanguageField]
    zone:  List[DemographicLanguageField]