import pandas as pd


items = pd.read_csv('items.csv')  


target_item_id = 101


target_item = items[items['item_id'] == target_item_id].iloc[0]


recommend_candidates = items[items['item_id'] != target_item_id].copy()


recommend_candidates['category_distance'] = (
    (recommend_candidates['small_category'] != target_item['small_category']).astype(int) +
    (recommend_candidates['big_category'] != target_item['big_category']).astype(int)
)
recommend_candidates['price_distance'] = abs(recommend_candidates['item_price'] - target_item['item_price'])
recommend_candidates['page_distance'] = abs(recommend_candidates['pages'] - target_item['pages'])


recommend_candidates = recommend_candidates.sort_values(
    by=['category_distance', 'price_distance', 'page_distance']
)


top_recommendations = recommend_candidates.head(3)['item_id'].tolist()


print(top_recommendations)