import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Union
import altair as alt
# import argparse as arg
# parser = arg.ArgumentParser()
# parser.add_argument('-c', '--csv', help='csv file to analyze')
# args = parser.parse_args()
# print(args.csv)

def substringSieve(string_list):
    '''
        Function to clean same authors with different substring
    '''
    string_list.sort(key=lambda s: len(s), reverse=True)
    out = []
    for s in string_list:
        if not any([s in o for o in out]):
            out.append(s)
    deleted_items = list(set(string_list) - set(out))
    for d in deleted_items:
        for ii, el in enumerate(out):
            if d in el:
                out.pop(ii)
                out.append(d)
                break
    return out

def init():
    st.title('Technological surveillance')

def get_info_csv(file: str) -> Union[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    df = pd.read_csv(file).fillna(0)
    authors = substringSieve(list(set([ii.lstrip() for auth_block in df['Authors'] for ii in auth_block.split(',') if 'No author name' not in ii])))
    sources = set(df['Source title'])
    affiliations = set(df['Affiliations'])
    papers = set(df['Title'])
    return authors, sources, affiliations, papers, df

def first_grade_analysis(df: pd.DataFrame, authors: pd.DataFrame, affiliations: pd.DataFrame) -> Union[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    '''
        Processing data
    '''
    years = set(df['Year'])
    publications_per_year = pd.DataFrame({year: [len(df.query(f'Year == {year}'))] for year in years}).T.sort_index()
    publications_per_year.columns = ['Publications']

    publications_per_author = pd.DataFrame(data={author: [len(list(filter(lambda x: author in x, df['Authors'])))] for author in authors}).T
    publications_per_author.columns = ['Publications']

    publications_per_affiliations =  pd.DataFrame(data={affiliation: [len(list(filter(lambda x: affiliation == x, df['Affiliations'])))] for affiliation in affiliations if type(affiliation) == str}).T
    publications_per_affiliations.columns = ['Publications']

    return publications_per_year, publications_per_author, publications_per_affiliations

def second_grade_analysis(df: pd.DataFrame, authors: pd.DataFrame, sources: pd.DataFrame, papers: pd.DataFrame) -> Union[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    '''
        Processing data
    '''
    cites_per_author = pd.DataFrame(data={author: [df[df['Authors'].str.contains(author)]['Cited by'].sum()] for author in authors}).T
    cites_per_author.columns = ['Cites']
    cites_per_source = pd.DataFrame(data={source: [df[df['Source title'].str.contains(source)]['Cited by'].sum()] for source in sources}).T
    cites_per_source.columns = ['Cites']
    cites_per_paper = pd.DataFrame(data={paper: [df[df['Title'] == paper]['Cited by'].sum()] for paper in papers}).T
    cites_per_paper.columns = ['Cites']
    return cites_per_author, cites_per_source, cites_per_paper

def third_grade_analysis(df: pd.DataFrame, authors: pd.DataFrame) -> pd.DataFrame:
    '''
        Authors per source per cites
    '''
    sources_per_author = pd.DataFrame(data={author: [df[df['Authors'].str.contains(author)]['Source title']] for author in authors})
    num_sources_per_author = pd.DataFrame(data={author: [len(sources_per_author[author][0])] for author in authors}).T
    num_sources_per_author.columns = ['Sources']
    return num_sources_per_author

def plot_first_grade_analysis(ppY: pd.DataFrame, ppAuth: pd.DataFrame, ppAff: pd.DataFrame) -> None:
    st.subheader('Number of publications per year')
    '''
        Number of publications per year
    '''
    st.line_chart(ppY)

    st.subheader('Number of publications per author')
    '''
        Publications by author #TODO: in future streamlit, change matplotlib to horizontal streamlit
    '''
    top_authors = ppAuth.sort_values(by=['Publications'], ascending=False).head(10)
    plot = alt.Chart(top_authors.reset_index(), width=700).mark_bar().encode(
        x='Publications:Q',
        y=alt.Y('index:N', sort='-x')
    ).properties(height=700)
    st.altair_chart(plot)

def plot_second_grade_analysis(cpAuth: pd.DataFrame, cpS: pd.DataFrame, cpP: pd.DataFrame) -> None:
    st.subheader('Top 10 Author by cited number')
    '''
        Top 10 Authors by cites
    '''
    top_authors = cpAuth.sort_values(by=['Cites'], ascending=False).head(10)
    plt.barh(np.arange(len(top_authors)), top_authors['Cites'])
    plt.yticks(np.arange(len(top_authors)), top_authors.index)
    plt.gca().invert_yaxis()
    plt.title('Top 10 authors')
    plt.xlabel = 'Prueba'
    plt.tight_layout()
    st.pyplot()

    st.subheader('Top 10 Sources by cited number')
    '''
        Top 10 Sources by cites
    '''
    top_sources = cpS.sort_values(by=['Cites'], ascending=False).head(10)
    plt.barh(np.arange(len(top_sources)), top_sources['Cites'])
    plt.yticks(np.arange(len(top_sources)), top_sources.index)
    plt.gca().invert_yaxis()
    plt.title('Top 10 sources')
    # plt.xlabel('Cited times')
    st.pyplot()

    st.subheader('Top 10 Papers by cited number')
    '''
        Top 10 Papers by cites
    '''
    top_papers = cpP.sort_values(by=['Cites'], ascending=False).head(10)
    plot = alt.Chart(top_papers.reset_index(), width=1000).mark_bar().encode(
        x='Cites:Q',
        y=alt.Y('index:N', sort='-x')
    ).properties(height=700)
    st.altair_chart(plot)

def plot_third_grade_analysis(nSpAuth: pd.DataFrame) -> None:
    '''
        Top 10 Authors by number of Sources which cited them
    '''
    st.subheader('Top 10 Authors by number of Sources which cited them')
    top_authors = nSpAuth.sort_values(by=['Sources'], ascending=False).head(10)
    plt.barh(np.arange(len(top_authors)), top_authors['Sources'])
    plt.yticks(np.arange(len(top_authors)), top_authors.index)
    plt.gca().invert_yaxis()
    plt.title('Top 10 authors')
    # plt.xlabel('Cited times')
    st.pyplot()

def main():
    init()
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        authors, sources, affiliations, papers, df = get_info_csv(uploaded_file)

        st.header('1st grade analysis')
        first_ppY, first_ppAuth, first_ppAff = first_grade_analysis(df, authors, affiliations)
        plot_first_grade_analysis(first_ppY, first_ppAuth, first_ppAff)

        st.header('2nd grade analysis')
        second_cpAuth, second_cpS, second_cpP = second_grade_analysis(df, authors, sources, papers)
        plot_second_grade_analysis(second_cpAuth, second_cpS, second_cpP)

        st.header('3rd grade analysis')
        third_nSpAuth = third_grade_analysis(df, authors)
        plot_third_grade_analysis(third_nSpAuth)

if __name__ == "__main__":
    main()