import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Custom modules
from postgres_db import PostgresDB
from dimension_reduction import reduce_dimensions

# Initialize database connection
@st.cache_resource
def init_db():
    return PostgresDB(dbname="postgres", user="postgres", password="postgres")

db = init_db()

def get_shade(distance, mean, std_dev):
    if mean - 2 * std_dev <= distance < mean - 1 * std_dev:
        return "#F0FFFF"
    elif mean - 1 * std_dev <= distance < mean:
        return "#89CFF0"  # Royal Blue
    elif mean <= distance < mean + 1 * std_dev:
        return "#0096FF"  # Steel Blue
    elif mean + 1 * std_dev <= distance < mean + 2 * std_dev:
        return "#0000FF"  # Sky Blue
    
    else:
        return "#0047AB"  # Light Blue


def create_tsne_plot(tsne_embeddings, labels, query_embedding):
    """
    Creates a t-SNE plot using the embeddings and labels.
    """
    
    df = pd.DataFrame(tsne_embeddings, columns=['x', 'y'])
    mean = np.mean(labels)
    std_dev = np.std(labels)
    labels = [get_shade(dist, mean, std_dev) for dist in labels]
    df['label'] = labels
    
    query_df = pd.DataFrame([query_embedding], columns=['x', 'y'])
    query_df['label'] = 'Query'

    df_combined = pd.concat([df, query_df], ignore_index=True)

    fig = px.scatter(
        df_combined, 
        x='x', y='y', 
        color='label',
        color_discrete_map={"#0047AB": "#0047AB", "#0000FF": "#0000FF", "#0096FF": "#0096FF", "#89CFF0": "#89CFF0", "#F0FFFF": "#F0FFFF", "Query": "red"},
        title='t-SNE Embeddings'
    )

    return fig

def perform_search(query):
    query_embed, results = db.search_similar_descriptions(query)
    embeddings = np.array([query_embed] + [res[2] for res in results])
    tsne_embeds = reduce_dimensions(embeddings)
    labels = [res[0] for res in results]

    df = pd.DataFrame(results, columns=['Company', 'Description', 'Vector', 'Distance'])
    df['X'] = tsne_embeds[1:, 0]
    df['Y'] = tsne_embeds[1:, 1]
    df = df[['Company', 'Description', 'X', 'Y', 'Distance']]
    df['info'] = df['Company'] + '\n' + df['Description']

    return df, tsne_embeds, df['Distance'].tolist()

def main():
    st.title("Company Search and Analysis")

    query = st.text_area('Enter your query')

    if st.button('Search'):
        if query:
            try:
                st.session_state.query = query
                df, tsne_embeds, labels = perform_search(query)
                st.session_state.df = df

                st.subheader("Search Results")
                st.dataframe(df)

                st.subheader("t-SNE Visualization")
                fig = create_tsne_plot(tsne_embeds[1:], labels, tsne_embeds[0])
                st.plotly_chart(fig)

            except Exception as e:
                st.error(f"An error occurred during the search: {e}")
        else:
            st.error("Please enter a query.")



if __name__ == "__main__":
    main()