import xmlrpc.client

url = "http://localhost:8016"
username = 'learn'
password = 'learn'
db = 'learn'

# "xmlrpc/2/common" Used to fetch version information

common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
# print(common.version())

user_uid = common.authenticate(db, username, password, {})
print(user_uid)

# 'xmlrpc/2/object' 'execue_kw'
# 'db, uid, password, model_name, method_name, [], {}'

models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

# Search Function

property_ids = models.execute_kw(db, user_uid, password, 'estate.property', 'search', [[]]) # ,{'offset':2, 'limit':1}
print("Search Function =>", property_ids)

# Count Function

count_property_ids = models.execute_kw(db, user_uid, password, 'estate.property', 'search_count', [[]])
print("Count Function =>", count_property_ids)

# Read Function

read_property_ids = models.execute_kw(db, user_uid, password, 'estate.property', 'read', [property_ids], {'fields': ['name']})
print("Read Function =>", read_property_ids)

# Search & Read Function

search_read_property_ids = models.execute_kw(db, user_uid, password, 'estate.property', 'search_read',  [[]], {'fields': ['name']})
print("Search & Read Function =>", search_read_property_ids)

# Create Function

create_property_ids = models.execute_kw(db, user_uid, password, 'estate.property', 'create', [{'name': "Property form RPC", 'sales_id': 6}])
print("Create Function =>", create_property_ids)

# Write Function (To Update)

write_property_ids = models.execute_kw(db, user_uid, password, 'estate.property', 'write', [[8], {'name': "Property form RPC updated"}])
read_name_get = models.execute_kw(db, user_uid, password, 'estate.property', 'name_get', [[8]])
print("Write/Update Function =>", write_property_ids)

unlink_property_ids = models.execute_kw(db, user_uid, password, 'estate.property', 'unlink', [[8]])
print("Unlink Function =>", unlink_property_ids)