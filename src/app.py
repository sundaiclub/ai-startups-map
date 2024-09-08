import streamlit as st
from encoder import Encoder
from postgres_db import PostgresDB
import pandas as pd
from dimension_reduction import reduce_dimensions
import numpy as np
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt

encoder = Encoder()

db = PostgresDB(dbname="postgres", user="postgres", password="postgres")
print(db.get_num_rows())

def create_tsne_plot(tsne_embeddings, labels, query_embedding):
    df = pd.DataFrame(tsne_embeddings, columns=['x', 'y'])
    df['label'] = labels

    query_df = pd.DataFrame(query_embedding, columns=['x', 'y'])
    query_df['label'] = ['Query']

    df_combined = pd.concat([df, query_df], ignore_index=True)

    fig = px.scatter(
        df_combined, 
        x='x', y='y', 
        color='label',
        color_discrete_map={"Query": "red"},
        title='t-SNE Embeddings'
    )

    return fig


query = st.text_area('Enter your query')

if st.button('Search'):
    query_embed, results = db.search_similar_descriptions(query)
    embeds = [query_embed] + [res[2] for res in results]
    embeds = np.array(embeds)
    tsne_embeds = reduce_dimensions(embeds)
    labels = [res[0] for res in results]

    df = pd.DataFrame(results, columns=['Company', 'Description', 'Vector', 'Distance'])
    df['X'] = tsne_embeds[1:, 0]
    df['Y'] = tsne_embeds[1:, 1]
    df = df[['Company', 'Description', 'X', 'Y', 'Distance']]

    st.dataframe(df)
    fig = create_tsne_plot(tsne_embeds[1:], labels, tsne_embeds[0].reshape(1, -1))
    st.plotly_chart(fig)