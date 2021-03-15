import hashlib
import pickle as pkl
from io import StringIO
from typing import Union

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from wordcloud import WordCloud

import scopus_scrapper as ss
import altair as alt


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


@st.cache
def get_info_csv(file: str) -> Union[
    pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    df = pd.read_csv(file).fillna(0)
    authors = substringSieve(list(set(
        [ii.lstrip() for auth_block in df['Authors'] for ii in auth_block.split(',') if 'No author name' not in ii])))
    sources = set(df['Source title'])
    affiliations = set(df['Affiliations'])
    papers = set(df['Title'])
    author_keywords = df['Author Keywords']
    return df, authors, sources, affiliations, papers, author_keywords


@st.cache
def get_info_df(scrapped_data: pd.DataFrame) -> Union[
    pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    df = pd.read_csv(StringIO(scrapped_data))
    authors = substringSieve(list(set(
        [ii.lstrip() for auth_block in df['Authors'] for ii in auth_block.split(',') if 'No author name' not in ii])))
    sources = set(df['Source title'])
    affiliations = set(df['Affiliations'])
    papers = set(df['Title'])
    author_keywords = df['Author Keywords']
    return df, authors, sources, affiliations, papers, author_keywords


def first_grade_analysis(df: pd.DataFrame, authors: pd.DataFrame, affiliations: pd.DataFrame) -> Union[
    pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    '''
        Processing data
    '''
    years = set(df['Year'])
    publications_per_year = pd.DataFrame({year: [len(df.query(f'Year == {year}'))] for year in years}).T.sort_index()
    publications_per_year.columns = ['Publications']

    publications_per_author = pd.DataFrame(
        data={author: [len(list(filter(lambda x: author in x, df['Authors'])))] for author in authors}).T
    publications_per_author.columns = ['Publications']

    publications_per_affiliations = pd.DataFrame(
        data={affiliation: [len(list(filter(lambda x: affiliation == x, df['Affiliations'])))] for affiliation in
              affiliations if type(affiliation) == str}).T
    publications_per_affiliations.columns = ['Publications']

    return publications_per_year, publications_per_author, publications_per_affiliations


def second_grade_analysis(df: pd.DataFrame, authors: pd.DataFrame, sources: pd.DataFrame, papers: pd.DataFrame) -> Union[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    '''
        Processing data
    '''
    cites_per_author = pd.DataFrame(data={author: [df[df['Authors'].str.contains(author, na=False)]['Cited by'].sum()] for author in authors}).T
    cites_per_author.columns = ['Cites']
    cites_per_source = pd.DataFrame(data={source: [df[df['Source title'].str.contains(source, na=False)]['Cited by'].sum()] for source in sources if type(source) == str}).T
    cites_per_source.columns = ['Cites']
    cites_per_paper = pd.DataFrame(data={paper: [df[df['Title'] == paper]['Cited by'].sum()] for paper in papers}).T
    cites_per_paper.columns = ['Cites']
    return cites_per_author, cites_per_source, cites_per_paper


def third_grade_analysis(df: pd.DataFrame, authors: pd.DataFrame) -> pd.DataFrame:
    '''
        Authors per source per cites
    '''
    sources_per_author = pd.DataFrame(
        data={author: [df[df['Authors'].str.contains(author, na=False)]['Source title']] for author in authors})
    num_sources_per_author = pd.DataFrame(data={author: [len(sources_per_author[author][0])] for author in authors}).T
    num_sources_per_author.columns = ['Sources']
    return num_sources_per_author


def fourth_grade_analysis(df: pd.DataFrame, papers: pd.DataFrame) -> pd.DataFrame:
    for paper in papers:
        if len(df[df['Title'] == paper]['Year'].values) == 0 or len(df[df['Title'] == paper]['Year'].values) == 0:
            return None
    scimago_per_paper = pd.DataFrame(data={paper: [df[df['Title'] == paper]['Cited by'].sum()] for paper in papers}).T
    sources_per_paper = pd.DataFrame(data={paper: [df[df['Title'] == paper]['Source title'].values[0]] for paper in papers}).T
    years_per_paper = pd.DataFrame(data={paper: [df[df['Title'] == paper]['Year'].values[0]] for paper in papers}).T
    scimago_per_paper.columns = ['Cites']
    sources_per_paper.columns= ['Source']
    years_per_paper.columns= ['Year']
    scimago_per_paper =  scimago_per_paper.join(sources_per_paper)
    scimago_per_paper =  scimago_per_paper.join(years_per_paper)
    return scimago_per_paper

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
    # fig, ax = plt.subplots()
    top_authors = ppAuth.sort_values(by=['Publications'], ascending=False).head(10)
    st.bar_chart(top_authors, height=400)


def plot_second_grade_analysis(cpAuth: pd.DataFrame, cpS: pd.DataFrame, cpP: pd.DataFrame) -> None:
    st.subheader('Top 10 Author by cited number')
    '''
        Top 10 Authors by cites
    '''
    top_authors = cpAuth.sort_values(by=['Cites'], ascending=False).head(10)
    st.bar_chart(top_authors, height=400)

    st.subheader('Top 10 Sources by cited number')
    '''
        Top 10 Sources by cites
    '''
    top_sources = cpS.sort_values(by=['Cites'], ascending=False).head(10)
    st.bar_chart(top_sources, height=400)

    st.subheader('Top 10 Papers by cited number')
    '''
        Top 10 Papers by cites
    '''
    top_papers = cpP.sort_values(by=['Cites'], ascending=False).head(10)
    st.bar_chart(top_papers, height=400)

def plot_third_grade_analysis(nSpAuth: pd.DataFrame, auth_kw: pd.DataFrame) -> None:
    '''
        Top 10 Authors by number of Sources which cited them
    '''
    st.subheader('Top 10 Authors by number of Sources which cited them')
    top_authors = nSpAuth.sort_values(by=['Sources'], ascending=False).head(10)
    st.bar_chart(top_authors, height=400)

    st.subheader('Author keywords word cloud')
    '''
        Author keywords word cloud
    '''
    auth_kw_str = auth_kw.to_csv(index=False)
    wordcloud = WordCloud(width=800, height=400).generate(auth_kw_str)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()
    st.pyplot(height=600)

def plot_fourth_grade_analysis(scimago: pd.DataFrame, scimago_years: list , scimago_avaliable:bool) -> None:
    if scimago is not None:
        st.subheader('Top 10 Papers by cited number and scimago quartil')
        '''
            Top 10 Papers by cites number and scimago quartil
        '''

        top_papers = scimago.sort_values(by=['Cites'], ascending=False).head(10)

        if scimago_avaliable:
            top_papers = scimago.query(" Year == @scimago_years")
            top_papers = top_papers.sort_values(by=['Cites'], ascending=False).head(10)

        quartiles = []
        for source, paper, cites, year in zip(list(top_papers.Source), list(top_papers.Cites.index), list(top_papers.Cites), list(top_papers.Year)):
            quartil = ss.process_scimago_file(year, source)
            ##if quartil is not None and scimago_avaliable:
            quartiles.append([paper, source, cites, year, quartil])
        df = pd.DataFrame(quartiles, columns=('papers', 'source', 'cites', 'year', 'quartiles'))
        c = alt.Chart(df).mark_circle().encode( x = 'papers', y = 'cites', size = 'cites', color = 'year', tooltip = ['papers', 'source', 'cites', 'year', 'quartiles'])
        st.altair_chart(c, use_container_width=True)
        st.table(df)

def print_analysis(df, authors, sources, affiliations, papers, author_keywords, years, scimago_years, scimago_avaliable) -> None:
    st.header('1st grade analysis')
    first_ppY, first_ppAuth, first_ppAff = first_grade_analysis(
        df.query(f'(Year >= {years[0]}) & (Year <= {years[1]})'), authors, affiliations)
    plot_first_grade_analysis(first_ppY, first_ppAuth, first_ppAff)

    st.header('2nd grade analysis')
    second_cpAuth, second_cpS, second_cpP = second_grade_analysis(
        df.query(f'(Year >= {int(years[0])}) & (Year <= {int(years[1])})'), authors, sources, papers)
    plot_second_grade_analysis(second_cpAuth, second_cpS, second_cpP)

    st.header('3rd grade analysis')
    third_nSpAuth = third_grade_analysis(df.query(f'(Year >= {years[0]}) & (Year <= {years[1]})'), authors)
    plot_third_grade_analysis(third_nSpAuth, author_keywords)

    fourth_nSpAuth = fourth_grade_analysis(df.query(f'(Year >= {int(years[0])}) & (Year <= {int(years[1])})'), papers)
    if fourth_nSpAuth is not  None:
        st.header('4th grade analysis')
        plot_fourth_grade_analysis(fourth_nSpAuth, scimago_years, scimago_avaliable)


@st.cache
def load_scrapped_data(query):
    with open(f'queries/{hashlib.sha1(query.encode()).hexdigest()}.pkl', 'rb') as f:
        return pkl.load(f)


def main():
    init()
    # years = ss.get_years_scimago()
    uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
    query = st.sidebar.text_area('Scopus query')
    try:
        scrapped_data = load_scrapped_data(query)
    except:
        scrapped_data = None
    str_num_items = st.sidebar.empty()
    if not (query is None or query == ''):
        try:
            num_items = ss.check_query(query)
        except:
            st.warning('No results found')
            return
        str_num_items.markdown(f'**{num_items}** results')
        st.sidebar.markdown('Analyze them?')
        if st.sidebar.button('Start'):
            with st.spinner('Scrapping data from Scopus. Please wait...'):
                try:
                    scrapped_data = ss.get_csv(num_items, query)
                except Exception as e:
                    st.warning('No results found')
                with open(f'queries/{hashlib.sha1(query.encode()).hexdigest()}.pkl', 'wb') as f:
                    pkl.dump(scrapped_data, f)
            st.success('Done')
    if uploaded_file is not None:
        # st.sidebar.markdown('**Scimago data available from**')
        # st.sidebar.markdown('%s **to** %s' % (years[-1], years[0]))
        scimago_avaliable = st.sidebar.checkbox('Scimago available')
        scimago_years=[]
        # if(scimago_avaliable):
            # scimago_years = years
        df, authors, sources, affiliations, papers, author_keywords = get_info_csv(uploaded_file)
        list_years = [int(year) for year in set(df['Year'])]
        years = st.sidebar.slider('Years', min(list_years), max(list_years), (min(list_years), max(list_years)))
        str_num_items.markdown(f'Showing **{len(df.query(f"(Year >= {years[0]}) & (Year <= {years[1]})"))}** results')
        st.markdown(f'Showing **{len(df.query(f"(Year >= {years[0]}) & (Year <= {years[1]})"))}** results')
        print_analysis(df, authors, sources, affiliations, papers, author_keywords, years, scimago_years, scimago_avaliable)
    if scrapped_data is not None:
        # st.sidebar.markdown('**Scimago data available from**')
        # st.sidebar.markdown('%s **to** %s' % (years[-1], years[0]))
        scimago_avaliable = st.sidebar.checkbox('Scimago and Scopus available')
        scimago_years=[]
        # if(scimago_avaliable):
            # scimago_years = years
        list_years = [int(year) for year in set(scrapped_data['Year'])]
        years = st.sidebar.slider('Years', min(list_years), max(list_years), (min(list_years), max(list_years)))
        df, authors, sources, affiliations, papers, author_keywords = get_info_df(scrapped_data.to_csv())
        str_num_items.markdown(f'Showing **{len(df.query(f"(Year >= {years[0]}) & (Year <= {years[1]})"))}** results')
        st.markdown(f'Showing **{len(df.query(f"(Year >= {years[0]}) & (Year <= {years[1]})"))}** results')
        print_analysis(df, authors, sources, affiliations, papers, author_keywords, years, scimago_years, scimago_avaliable)


if __name__ == "__main__":
    main()
