import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

products = pd.read_csv("data/products.csv")
ratings = pd.read_csv("data/ratings.csv")


# ----------------------------
# Content-Based Filtering
# ----------------------------
def content_based_recommend(product_name, top_n=5):
    tfidf = TfidfVectorizer(stop_words='english')

    products['description'] = products['description'].fillna('')
    tfidf_matrix = tfidf.fit_transform(products['description'])

    similarity = cosine_similarity(tfidf_matrix)

    indices = pd.Series(products.index, index=products['name']).drop_duplicates()

    if product_name not in indices:
        return pd.DataFrame()   # ✅ FIX

    idx = indices[product_name]
    sim_scores = list(enumerate(similarity[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]

    product_indices = [i[0] for i in sim_scores]
    return products.iloc[product_indices]


# ----------------------------
# Collaborative Filtering
# ----------------------------
def collaborative_filtering(product_name, top_n=5):
    pivot = ratings.pivot_table(index='user_id', columns='product_id', values='rating').fillna(0)

    similarity = cosine_similarity(pivot.T)
    sim_df = pd.DataFrame(similarity, index=pivot.columns, columns=pivot.columns)

    product_id = products[products['name'] == product_name]['product_id'].values

    if len(product_id) == 0:
        return pd.DataFrame()   # ✅ FIX

    product_id = product_id[0]

    similar_products = sim_df[product_id].sort_values(ascending=False)[1:top_n+1]

    return products[products['product_id'].isin(similar_products.index)]


# ----------------------------
# Hybrid Recommendation
# ----------------------------
def hybrid_recommend(product_name):
    content = content_based_recommend(product_name)
    collab = collaborative_filtering(product_name)

    # ✅ Safe concat
    combined = pd.concat([content, collab], ignore_index=True).drop_duplicates()
    return combined