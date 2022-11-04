# Pysurveillance conference

## Diapo 1

Good afternoon to everyone. My name is Julen Cestero, I am a PhD student from Spain, and today I'm gonna introduce you Pysurveillance, which is a novel tool for supporting research in the systematic literature review process.

## Diapo 2

The structure of this presentation is the following one.

## Diapo 3

So, first,

## Diapo 4

Why did we build Pysurveillance? So, now I'm gonna describe what a typical research process typically looks like to, for example, a PhD student, or a senior researcher with a new research line. With the basic idea of the field in mind, this person would lookup to information into the main scholar research engines, for example, Google Scholar, Scopus, or Web of Science. After the query is created, this researcher gets a list of the most relevant publications of the search, ACCORDING TO THE SEARCH ENGINE. These search engines show the results ordered by certain criteria, for example, using the closest title to the query, the most viewed papers, etc. And it's up to the own researcher to filter through thousands of papers to find the most relevants for them. In most cases, this researcher won't pass from the first page, reading every abstract until they get content with some of them. This process seems arbitrary and neither efficient and effective.

## Diapo 5

For aiding with that problem, we present Pysurveillance, which is a Bibliometric analysis tool that can retrieve and sort the data resulting from the aforementioned research query, in a fast and effective way. The results of the query are displayed with various graphs that show, for example, the top 10 papers in terms of citations, the most prolific authors or the most cited journals. All of them in a neat User Interface that allows to sort through the data or filter results.

## Diapo 6

But first, a small comment about the tools that currently work similar to our own.

## Diapo 7

We can divide the Bibliometric tools into two different groups. First, the Performance Analysis Tools, which aim to evaluate groups of scientific actors and the impact of their activity based on bibliographic data, more like analyzing this bibliographic data. And second, the Science Mapping tools, whose objective is to display data, to represent intellectual connections and the evolution in a knowledge area. And some examples about these two groups are Publish or Perish, CR Explorer or Scientopy for the Performance Analysis tools, and Bibliometrix, SciMAT or Bibtools for the Science Mapping tools.

## Diapo 8

Having said this, now I'll show you our tool, Pysurveillance

## Diapo 9

So, Pysurveillance is an open source web tool that sorts and displays fancy graphs from a research query. In the right hand we can see a screenshot of the tool, and a graph that depicts the evolution of the interest in the research field from the query. On the sidebar we have the logo of the tool, a box using for uploading csv files to be graphed within the tool, and a textbox where the user can introduce their own query. Pysurveillance also analyzes the data with different analysis, differentiated by their complexity grade. These grades vary from first grade analysis, where it correlates different properties with the count of this property. For example, the number of publications per year, or the number of publications per author. The second grade analysis adds another feature, which is the number of citations, and correlates the number of citations    per paper, per author or per journal. The third grade analysis scales even more, adding another feature more. For example, the number of citations of an author, counting as unique the citations from the same source. And a feature that is still work in progress is the fourth grade analysis, which adds the impact factor of the journal the paper is published to this equation.

## Diapo 10

We used Streamlit to build the front-end, which is a python library used for building dashboards in a fast and easy way. Our aim for creating this front page for our tool was to display the sorted information in a clear, fast and useful way, so that the researcher could get the most important information with a simple glance over the screen. For that, we developed several graphs, ordered by the complexity grade, such as the number of publications per year, per author, the top cited authors, sources, papers, and so on. There are two ways of using Pysurveillance. One is to import a csv file from a Scopus query, and the second one is to use a search box in the sidebar to search directly through the Scopus API. Also, it can retrieve the information about the impact factor of the publications using Scimago, and we have currently a couple of graphs which use this functionality, although we plan to enhance the tool with it in future iterations. And finally, we have a wordcloud with the key words of the query, that can be used to polish the query.

## Diapo 11

As a small note, the back-end of the tool is totally dependant from the UI calls, we don't have yet an independent back-end running constantly, as we didn't need it. However, even if the back-end is integrated with the front-end, we can separate them conceptually and classify the back-end into two different scripts. First, the Scopus scraper is in charge of the queries to the Scopus API. It sanitizes the query introduced by the researcher, and retrieves the information from Scopus. Because of performance reasons, after getting the number of results from the query, it will ask the user if they truly want to download the results of the query, and they have to confirm it for the scraper to continue to download all the query, which can take a while. On the other hand, after the data from Scopus is loaded into the memory, via a manual csv upload or using the API call, this data is processed and sorted for building the front-end graphs.

## Diapo 12

Well, until now I showed you some features of Pysurveillance, but how good is it comparing to other State of the Art tools?

## Diapo 13

For that, we have this table, which compares the State of the Art tools with Pysurveillance. The criteria for comparing them are the platform, programming language, latest update, if it allows online requests or if the data must be manually added, if it preprocess data for deleting duplicates and stuff like that, then we check if these tools have something similar to the grade comparisons we used, and finally a couple of notes about the user interaction easiness and other notes. And long story short, the first 3 tools, apart from Pysurveillance, have rudimentary grade analysis, but have other utilities like merging several csv files, being able to retrieve data from several online databases, or making more abstract connections between publications. However, the last two tools, Bibliometrix and Bibliotools, both are similar to Pysurveillance in terms of displayed inf  ormation, and we truly can inspire future work of our tool on these tools, but they have a small flaw that is their need to manual interaction for loading the data or creating the graphs. In that, Pysurveillance has the advantage of being very straightforward and focused on being accessible, not requiring manual interaction at all with the inner data.

## Diapo 14

And with that, we can get...

## Diapo 15

...the following conclusions. First, we saw that automating systematic literature studies enhances the research process. Then, we introduced Pysurveillance as a tool for automating this process, making emphasis on the visual communication system. And finally we saw that Pysurveillance can compete with the State of the Art tools, having some of their best qualities.

## Diapo 16

And with that I finish my presentation. I wanted to thank the other collaborators of this project, mainly David and Elizabeth who were invested in this project since the day one.

## Diapo 17

And if you have any questions, you can contact me with the email shown on screen. Thank you for your attention. 
