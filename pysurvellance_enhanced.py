import hashlib
import pickle as pkl
import re
from io import StringIO

import pandas as pd
import plotly.express as px
import streamlit as st
from wordcloud import WordCloud

import scopus_scrapper as ss


def init():
    st.title("Pysurveillance")
    st.sidebar.image("demo/logo.png")


@st.cache
def load_scrapped_data(query):
    with open(f"queries/{hashlib.sha1(query.encode()).hexdigest()}.pkl", "rb") as f:
        return pkl.load(f)


def substringSieve(string_list):
    """
    Function to clean same authors with different substring
    """
    string_list.sort(key=lambda s: len(s), reverse=True)
    out = []
    for s in string_list:
        if all(s not in o for o in out):
            out.append(s)
    deleted_items = list(set(string_list) - set(out))
    for d in deleted_items:
        for ii, el in enumerate(out):
            if d in el:
                out.pop(ii)
                out.append(d)
                break
    return out


@st.cache
def get_info(df: pd.DataFrame):
    authors = substringSieve(
        list({ii.lstrip() for auth_block in df["Authors"] for ii in auth_block.split(",") if "No author name" not in ii})
    )
    sources = set(df["Source title"])
    affiliations = set(df["Affiliations"])
    papers = set(df["Title"])
    author_keywords = df["Author Keywords"]
    return authors, sources, affiliations, papers, author_keywords


@st.cache
def get_queried_data(df, x_var, y_var):
    df[x_var] = df[x_var].astype(str)
    if x_var in ["Authors", "Affiliations"]:
        X = substringSieve(
            list(
                {
                    ii.lstrip()
                    for x_block in df[x_var]
                    if x_block != "0"
                    for ii in x_block.split(",")
                    if "No author name" not in ii
                }
            )
        )
        if y_var == "Count":
            results = pd.DataFrame({x: [len(list(filter(lambda f: x in f, df[x_var])))] for x in X}).T
        elif y_var == "Cited by":
            results = pd.DataFrame(({x: [df[df[x_var].str.contains(re.escape(x), na=False)][y_var].sum()] for x in X})).T
        else:
            raise NotImplementedError
    else:
        X = set(df[x_var])
        if y_var == "Count":
            results = pd.DataFrame({x: [len(list(filter(lambda f: x == f, df[x_var])))] for x in X if x != "0"}).T
        elif y_var == "Cited by":
            results = pd.DataFrame(({x: [df[df[x_var] == x][y_var].sum()] for x in X if x != "0"})).T
        else:
            raise NotImplementedError
    results.columns = [y_var]
    if x_var == "Year":
        return results.sort_index()
    else:
        return results.sort_values(by=y_var, ascending=False)


def plot_results(df, y_var, num):
    fig = px.bar(df.head(num), y=y_var)
    st.plotly_chart(fig, use_container_width=True, height=700)


def filter_df_by_years(df, years):
    return df.query(f"(Year >= {years[0]}) & (Year <= {years[1]})")


def make_plots(uploaded_file, scrapped_data, str_num_items):
    df = (
        pd.read_csv(uploaded_file).fillna("0")
        if uploaded_file is not None
        else pd.read_csv(StringIO(scrapped_data.to_csv())).fillna("0")
    )
    df["Cited by"] = pd.to_numeric(df["Cited by"])
    df["Year"] = pd.to_numeric(df["Year"])
    # authors, sources, affiliations, papers, author_keywords = get_info(df)
    list_years = [int(year) for year in set(scrapped_data["Year"])]
    years = st.sidebar.slider("Years", min(list_years), max(list_years), (min(list_years), max(list_years)))
    df = filter_df_by_years(df, years)
    str_num_items.markdown(f'Showing **{len(df.query(f"(Year >= {years[0]}) & (Year <= {years[1]})"))}** results')
    num_results = len(df.query(f"(Year >= {years[0]}) & (Year <= {years[1]})"))
    st.markdown(f"Showing **{num_results}** results")

    selected_num_results = st.slider("Number of results:", min_value=3, max_value=num_results, value=10)
    col1, col2 = st.columns(2)
    x_var = col1.selectbox("X variable", ["Authors", "Title", "Year", "Affiliations", "Source title"])
    y_var = col2.selectbox("Y variable", ["Count", "Cited by"])
    df_results = get_queried_data(df, x_var, y_var)
    if x_var == "Year":
        plot_results(df_results, y_var, 10000)
    else:
        plot_results(df_results, y_var, selected_num_results)


def main():
    st.set_page_config(layout="wide")
    init()
    uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
    query = st.sidebar.text_area("Scopus query")
    try:
        scrapped_data = load_scrapped_data(query)
    except Exception:
        scrapped_data = None
    str_num_items = st.sidebar.empty()
    if query is not None and query != "":
        try:
            num_items = ss.check_query(query)
        except Exception:
            st.warning("No results found")
            return
        str_num_items.markdown(f"**{num_items}** results")
        st.sidebar.markdown("Analyze them?")
        if st.sidebar.button("Start"):
            with st.spinner("Scrapping data from Scopus. Please wait..."):
                try:
                    scrapped_data = ss.get_csv(num_items, query)
                except Exception as e:
                    st.warning("No results found")
                with open(f"queries/{hashlib.sha1(query.encode()).hexdigest()}.pkl", "wb") as f:
                    pkl.dump(scrapped_data, f)
            st.success("Done")
    if uploaded_file is not None or scrapped_data is not None:
        make_plots(uploaded_file, scrapped_data, str_num_items)


if __name__ == "__main__":
    main()
