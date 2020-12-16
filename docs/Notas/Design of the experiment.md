# Design of the experiment

## Description of the experiment

<!-- Definir cómo es actualmente el producto. Explicar cómo está compuesto, en qué se basa su front-end y definir su back-end -->

We developed a platform which performs a detailed analysis over a specified search of the literature regarding a research theme. Using the results from a user defined search through academic literature indexers, such as Scopus, this platform shows a series of graphs which sort the results in a more useful way to the user using different complexity level analysis [REF]. These analysis vary from showing the most prolific authors, through the most cited authors or papers, to much more complex analysis such as the most cited authors counting as unique the citations of the different authors of each institution, and sorting their papers by the quartile of the journal at their publication time.

The platform, which we called *pysurveillance*, is divided into two different elements: the front-end and the back-end. Although it is completely written in Python, the front-end uses a package called *streamlit* [REF]. This package, despite being relatively easy to use in comparison to other front-end engines, it is powerful enough for supporting *pysurveillance* in the actual state


## Development of the experiment

Definir el proceso y las razones para haber llegado a construir y definir esta herramienta. Empezar definiendo el proceso que seguía David, y explicar que se ha automatizado con esta herramienta. Además, añadir que al principio se añadieron funciones básicas que Scopus ya tenía (análisis de primer nivel) y luego se han ido añadiendo análisis de mayor complejidad para diferentes estadísticas. **Estaría bien poder definir de alguna manera el grado de análisis**




En la parte teórica de esta sección, Eli está de apoyo. Contiene diseño del producto y desarrollo del producto. Diseño del producto contendrá la explicación teórica de qué es nuestro prototipo. Gráficas que analicen el funcionamiento del producto, diagramas de llamadas a la web, etc. Se explicarán las dos opciones del producto, la de recoger los datos de la API de Scopus y la de importar csv. También añadiremos la opción de captación de cuartiles para evaluar el impacto de los artículos que mostramos. Por otro lado, en la parte de desarrollo del producto se definirá el procedimiento que se ha seguido para la realización de la aplicación, desde la explicación teórica de lo que David realizaba a su implementación en Python



Diseño y desarrollo de la solución: lo mío.
Diseño del experimento: Queremos comparar herramienta vs excel. Entonces definimos una serie de métricas (**tiempo de respuesta**, **Intuitividad** (excel vs herramienta. Medir el tiempo que tarda una persona de media en aprender a usar la herramienta vs el tiempo que tarda en aprender a hacer lo mismo en excel), **Capacidad de prueba** (alguna métrica que sirva para poder validar cuánto de buenos son los resultados de excel o herramienta. Con herramienta se puede demostrar que nuestros resultados son buenos, que mientras si no usas la herramienta no puedes validar de ninguna manera cuánto de buenos son tus resultados. Con nuestra herramienta ademas puedes decir cuánto de buenos son, ya que son el top X de papers/autores, etc.), LLUVIA DE IDEAS) para ver en qué indicadores lo nuestro es mejor que excel. Se define el experimento.
