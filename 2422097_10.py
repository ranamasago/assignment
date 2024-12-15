import pandas as pd


orders = pd.read_csv('orders.csv')  
items = pd.read_csv('items.csv')    


merged_data = pd.merge(orders, items, on='item_id')
merged_data['purchase_amount'] = merged_data['order_num'] * merged_data['item_price']


max_purchase = merged_data.loc[merged_data['purchase_amount'].idxmax()]
result = [max_purchase['order_id'], max_purchase['purchase_amount']]


print(result)