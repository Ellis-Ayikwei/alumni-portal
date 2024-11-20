from datetime import datetime
import json
from models import storage
from models.alumni_group import AlumniGroup
from models.contract import Contract

# contract = storage.get(Contract, "454929f3-ab7d-413d-88bf-d153229b4def")
# print (contract.to_dict()["group"]["members"])


# group = storage.get(AlumniGroup, "2fe8e8f3-d036-410a-b5dc-025ea0e9cd73")
# for contract in group.contracts:
#     print(contract.to_dict())
#     print("-"*50)

expiry_date = 'Wed, 13 Nov 2024 00:00:00 GMT'

# Parse the date string
parsed_date = datetime.strptime(expiry_date, "%a, %d %b %Y %H:%M:%S %Z").date()

print(parsed_date)
