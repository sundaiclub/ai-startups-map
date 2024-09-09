import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Custom modules
from postgres_db import PostgresDB
from dimension_reduction import reduce_dimensions

# Initialize database connection
def init_db():
    return PostgresDB(dbname="postgres", user="postgres", password="postgres")

db = init_db()

def get_shade(distance, mean, std_dev):
    if distance < mean - 2 * std_dev:
        return "Very Highly Relevant"  # Dark Blue
    elif mean - 2 * std_dev <= distance < mean - 1.5 * std_dev:
        return "Highly Relevant"  # Royal Blue
    elif mean - 1.5 * std_dev <= distance < mean - 1 * std_dev:
        return "Relevant"  # Steel Blue
    elif mean - 1 * std_dev <= distance < mean:
        return "OKOK"  # Sky Blue
    elif mean <= distance < mean + 1 * std_dev:
        return "Not So Relevant"  # Light Blue
    else:
        return "Very Not So Relevant"  # Very Light Blue


def create_tsne_plot(tsne_embeddings, labels, hover_data, query_embedding):
    """
    Creates a t-SNE plot using the embeddings and labels.
    """
    
    df = pd.DataFrame(tsne_embeddings, columns=['x', 'y'])
    mean = np.mean(labels)
    std_dev = np.std(labels)
    labels = [get_shade(dist, mean, std_dev) for dist in labels]
    df['label'] = labels
    df['hover_data'] = hover_data
    query_df = pd.DataFrame([query_embedding], columns=['x', 'y'])
    query_df['label'] = 'Query'

    df_combined = pd.concat([df, query_df], ignore_index=True)

    fig = px.scatter(
        df_combined, 
        hover_name='hover_data',
        x='x', y='y', 
        color='label',
        color_discrete_map={
            "Very Highly Relevant": "#00008B",   # Dark Blue
            "Highly Relevant": "#4169E1",        # Royal Blue
            "Relevant": "#4682B4",              # Steel Blue
            "OKOK": "#87CEEB",                  # Sky Blue
            "Not So Relevant": "#ADD8E6",        # Light Blue
            "Very Not So Relevant": "#E0FFFF",  # Very Light Blue
            "Query": "red"
        },
        title='t-SNE Embeddings',
    )

    return fig


def perform_search(query):
    query_embed, results = db.search_similar_descriptions(query)
    embeddings = np.array([query_embed] + [res[4] for res in results])
    tsne_embeds = reduce_dimensions(embeddings)
    df = pd.DataFrame(results, columns=['Company', 'Country', 'Sector', 'Description', 'Vector', 'Distance'])
    df['X'] = tsne_embeds[1:, 0]
    df['Y'] = tsne_embeds[1:, 1]
    df = df[['Company', 'Country', 'Sector', 'Description', 'X', 'Y', 'Distance']]
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
                df['hover_info'] = 'Company: ' + df['Company'] + '\n'+ 'Country: ' + df['Country'] + '\n' + 'Sector: ' + df['Sector'] 
                st.session_state.df = df

                st.subheader("Search Results")
                st.dataframe(df)

                st.subheader("t-SNE Visualization")
                fig = create_tsne_plot(tsne_embeds[1:], labels, df['hover_info'].tolist(), tsne_embeds[0])
                st.plotly_chart(fig)

            except Exception as e:
                st.error(f"An error occurred during the search: {e}")
        else:
            st.error("Please enter a query.")



if __name__ == "__main__":
    main()