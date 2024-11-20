# from datetime import datetime
# import json
# from models import storage
# from models.alumni_group import AlumniGroup
# from models.contract import Contract

# # contract = storage.get(Contract, "454929f3-ab7d-413d-88bf-d153229b4def")
# # print (contract.to_dict()["group"]["members"])


# # group = storage.get(AlumniGroup, "2fe8e8f3-d036-410a-b5dc-025ea0e9cd73")
# # for contract in group.contracts:
# #     print(contract.to_dict())
# #     print("-"*50)

# expiry_date = 'Wed, 13 Nov 2024 00:00:00 GMT'

# # Parse the date string
# parsed_date = datetime.strptime(expiry_date, "%a, %d %b %Y %H:%M:%S %Z").date()

# print(parsed_date)



strA ="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczMjA5Nzk2NCwianRpIjoiYmViYWNlN2MtZTFhMi00NmIyLWI2NjMtMmI3M2ZhMjk3NzEyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IkFsdW1uaV9zdXBlcl9hZG1pbiIsIm5iZiI6MTczMjA5Nzk2NCwiY3NyZiI6IjllZDcyYTYwLWRhMTYtNDQ5My1iODQxLWFkZDRlNDFlYzRkYSIsImV4cCI6MTczMjEwMTU2NH0.lrrMtHGIuGr4xcQmiU_0T3s2wtciiqD6_2-jlTQ_oiA"
strB = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczMjA5ODA1OCwianRpIjoiMDJhNmEwMjUtOTZkZC00ZWVmLWJmOWItOTY1Njc1NTY5NTJiIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IkFsdW1uaV9zdXBlcl9hZG1pbiIsIm5iZiI6MTczMjA5ODA1OCwiY3NyZiI6IjE1NGIyYThjLTczZmEtNGRmMC05MDEzLTFlNTBiNDQ5ZTc2YyIsImV4cCI6MTczMjEwMTY1OH0.PnhFiLwsVmcjlwwzGYs1mzPYC0RyFEaaGRLFWjz-TWY"
print(strA==strB)