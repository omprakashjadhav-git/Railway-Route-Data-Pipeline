# from ntes import NTESClient
# client = NTESClient()
# print("NTES client created successfully")

# from ntes import NTESClient
# client = NTESClient()
# train_number = "04601"
# result = client.get_train_schedule(train_number)
# print(type(result))
# print(result)

# from ntes import NTESClient
# client = NTESClient()
# print(dir(client))

# from ntes import NTESClient
# import inspect
# client = NTESClient()
# print(inspect.signature(client.live_status))
# print(inspect.getdoc(client.live_status))

from ntes import NTESClient
client = NTESClient()
train_number = "04601"
start_date = "24-09-2026"
result = client.live_status(train_number, start_date)
print(type(result))
print(result)