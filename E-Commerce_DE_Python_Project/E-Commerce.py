import pandas as pd
import requests

customer = pd.read_csv('Input_File/Customer.csv')
print(customer)
order = pd.read_csv('Input_File/order.csv')
print(order)
product = pd.read_csv('Input_File/product.csv')
print(product)

"""print("customer row :",customer.shape[0])
print("order row :",order.shape[0])
print("product row :",product.shape[0])

print("customer column :",customer.shape[1])
print("order column :",order.shape[1])
print("product column :",product.shape[1])

print(customer.columns)
print(order.columns)
print(product.columns)

print(customer.dtypes)
print(order.dtypes)
print(product.dtypes)

print(customer.isnull().sum())
print(order.isnull().sum())
print(product.isnull().sum())

print(customer.duplicated().sum())
print(order.duplicated().sum())
print(product.duplicated().sum())"""

customer = customer.drop_duplicates(subset="customer_id")
customer["customer_name"] = customer["customer_name"].str.strip().str.capitalize()
customer["email"] = customer["email"].str.strip()
customer["city"] = customer["city"].str.strip()
customer["email"] = customer["email"].fillna('Unknown')
customer["city"] = customer["city"].fillna('Unknown')
customer["customer_name"] = customer["customer_name"].fillna('Unkown')
print(customer)


product = product.drop_duplicates(subset = "product_id")
product["category"] = product["category"].str.capitalize()
product["category"] = product["category"].fillna('NA')
product["valid_price"] = product["price"].fillna(0)
product["vaild_stock"] = product["stock"]
product.loc[product["vaild_stock"] < 0 , "vaild_stock"] = 0
print(product[["product_id","product_name","category","valid_price","vaild_stock"]])


order = order.drop_duplicates(subset="order_id")
order["quantity"] = order["quantity"].fillna(0)
order.loc[order["price"] < 0 , "price"] = 0
order["price"] = order["price"].fillna(0)
order["order_date"] = pd.to_datetime(order["order_date"], errors="coerce")
order.loc[order["quantity"] < 0 , "quantity"] = 0
order["status"] = order["status"].str.strip()
order = order[order["customer_id"].isin (customer["customer_id"])]
order = order[order["product_id"].isin (product["product_id"])]
print(order)


api_data = "https://jsonplaceholder.typicode.com/users?utm_source=chatgpt.com"
get_data = requests.get(api_data)
json_data = get_data.json()
for data in json_data :
    print(data['id'],data['name'],data['email'],data['address']['city'])
print()  

print(get_data.status_code)
print(type(json_data))
print(get_data.content)

api_df = pd.DataFrame(json_data)
api_df["city"] = api_df["address"].apply(lambda x:x["city"])
api_df = api_df[["id","name","email","city"]]
print(api_df)

order.to_csv("Output_file/order_cleaned.csv",index = False)
product.to_csv("Output_file/product_cleaned.csv",index = False)
customer.to_csv("Output_file/customer_cleaned.csv",index = False)
api_df.to_json("Output_file/cleaned_json.json",orient = "records",indent = 4)