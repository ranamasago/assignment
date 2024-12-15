import pandas as pd
orders = pd.read_csv('orders.csv')
items = pd.read_csv('items.csv')
merged_data = pd.merge(orders, items, on='item_id')
merged_data['purchase_amount'] = merged_data['order_num'] * merged_data['item_price']
average_purchase = merged_data.groupby('user_id')['purchase_amount'].mean()
max_average_purchase = average_purchase.idxmax()
max_average_amount = average_purchase.max()
result = [max_average_purchase, max_average_amount]
print(result)