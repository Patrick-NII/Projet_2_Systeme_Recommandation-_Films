import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.express as px
import streamlit as st
import collections
import io
from PIL import Image
from mpl_toolkits.mplot3d import Axes3D
from plotly.offline import iplot , plot
from plotly.subplots import make_subplots
plt.style.use('ggplot')
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title="Tableau de bord", layout="wide")

# Ajout du style CSS
st.markdown("""
    <style>
        .sidebar .sidebar-content {
            background-color: black !important;
        }
        /* Désactive la décoration du texte */
        a {
            text-decoration: none !important;
        }
        p {
            text-decoration: none !important;
            color:white !important;
        }
        /* unvisited link */
        p a:visited {
            color: #f8b319;
        }
        button.styled-button:hover {
            color: #000;
        }
    </style>
""", unsafe_allow_html=True)


# Afficher l'image en haut de la barre latérale
st.sidebar.image("C:\\Users\\teddy\\Documents\\Projet.2\\logo.png", use_column_width=True)

# Fonction pour générer le HTML d'un bouton avec le style souhaité
def generate_styled_button_html(label, url=None):
    if url:
        return f'<a href="{url}" target="_blank" class="styled-button">{label}</a>'
    else:
        return f'<button class="styled-button" style="color: #f8b319;">{label}</button>'

# Fonction pour afficher un bouton avec le style souhaité
def styled_button(label, url=None):
    button_html = generate_styled_button_html(label, url)
    return st.sidebar.markdown(button_html, unsafe_allow_html=True)

# Style CSS pour les boutons
st.markdown("""
<style>
.styled-button {
    background-color: rgba(0,0,0,0.8); /* Noir légèrement opaque */
    border: none;
    color: #f8b319; /* Jaune */
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    display: block;
    font-size: 16px;
    margin: 10px 0;
    width: 100%; /* Définir la largeur de tous les boutons */
    cursor: pointer;
    border-radius: 5px;
    transition: background-color 0.3s ease;
}

.styled-button:hover {
    background-color: #f8b319; /* Jaune légèrement opaque */
    color: #000;
}
</style>
""", unsafe_allow_html=True)

# Fonction pour charger les données et créer le graphique
def create_yearly_counts_plot(df):
    # Nombre de films par année
    yearly_counts = df.groupby('startYear').size().reset_index(name='count')

    # Créer le graphique avec Plotly
    fig = px.line(
        yearly_counts,
        x='startYear',
        y='count',
        markers=True,
        labels={'startYear': 'Année', 'count': 'Nombre de films'},
        title='Nombre de films par année'
    )
    fig.update_traces(line=dict(color='#f8b319'))
    fig.update_layout(template='plotly_dark')
    return fig

# Charger les données
merge = "C:\\Users\\teddy\\Documents\\Projet.2\\merged_final.csv"
df = pd.read_csv(merge, sep=',')
df = df.drop(columns=['titleId', 'poster_path', 'backdrop_path', 'nconst_director'])
df = df[df['startYear'] != 2024]

# Affichage du titre "Accès au site :" dans la barre latérale
st.sidebar.markdown("<h3 style='color: #FFF;'>Accès au site :</h3>", unsafe_allow_html=True)

# Affichage des boutons dans la barre latérale
styled_button('🛖 Home', 'https://cine-creuse-recommendation-ml-project.netlify.app/')
styled_button('⭐ Favorites', 'https://cine-creuse-recommendation-ml-project.netlify.app/')

# Calcul des statistiques
unique_film_count = df['title'].nunique()
unique_genre1_count = df['genre1'].nunique()
unique_directors_count = df['Director_name'].nunique()

# Créer les graphiques d'indicateurs
fig1 = go.Figure(go.Indicator(
    mode="number",
    value=unique_film_count,
    title="Films",
    number={'font': {'color': '#f8b319'}}
))
fig2 = go.Figure(go.Indicator(
    mode="number",
    value=unique_genre1_count,
    title="Genres",
    number={'font': {'color': '#f8b319'}}
))
fig3 = go.Figure(go.Indicator(
    mode="number",
    value=unique_directors_count,
    title="Réalisateurs",
    number={'font': {'color': '#f8b319'}}
))
fig1.update_layout(
    width=800,
    height=300,
    template='plotly_dark'
)
fig2.update_layout(
    width=800,
    height=300,
    template='plotly_dark'
)
fig3.update_layout(
    width=800,
    height=300,
    template='plotly_dark'
)

# Ajouter le titre "Tableau de bord"
st.title('Tableau de bord')

# Affichage des indicateurs dans trois colonnes
col1, col2, col3 = st.columns(3)
col1.plotly_chart(fig1, use_container_width=True)
col2.plotly_chart(fig2, use_container_width=True)
col3.plotly_chart(fig3, use_container_width=True)

# Affichage du graphique annuel
fig = create_yearly_counts_plot(df)
st.plotly_chart(fig, use_container_width=True)

# Genres
st.subheader('Genres')

# Créer la figure et les sous-graphiques
fig, axes = plt.subplots(1, 2,facecolor='black' ,figsize=(14, 6))

# Premier sous-graphique
data_genre1 = df['genre1'].value_counts().to_dict()
wc_genre1 = WordCloud(width=2000, height=1000, random_state=1, background_color='black', colormap='rainbow').generate_from_frequencies(data_genre1)
axes[0].imshow(wc_genre1)
axes[0].set_title('Genres principaux', fontsize=20, color='white')
axes[0].axis('off')

# Deuxième sous-graphique
data_genre2 = df['genre2'].value_counts().to_dict()
wc_genre2 = WordCloud(width=2000, height=1000, random_state=1, background_color='black', colormap='rainbow').generate_from_frequencies(data_genre2)
axes[1].imshow(wc_genre2)
axes[1].set_title('Genres secondaires', fontsize=20, color='white')
axes[1].axis('off')

plt.tight_layout()

# Affichage de la figure avec Streamlit
st.pyplot(fig)

# Affichage du graphique de la quantité de films par genre
genre_counts = df.apply(lambda row: pd.Series(row[['genre1', 'genre2']].unique()), axis=1).stack().value_counts()
index = genre_counts.index
x = list(range(len(index)))
bar_width = 0.8

fig_genre = go.Figure()
fig_genre.add_trace(go.Bar(
    x=x,
    y=genre_counts.values,
    width=bar_width,
    name='Total genre counts',
    marker_color='#f8b319'  # Couleur personnalisée
))
fig_genre.update_layout(
    xaxis=dict(
        tickmode='array',
        tickvals=x,
        ticktext=index,
        tickangle=45
    ),
    legend=dict(title='Légende'),
    xaxis_title='Genre',
    yaxis_title='Quantité',
    title='Quantité de films par genre',
    template='plotly_dark'
)
st.plotly_chart(fig_genre, use_container_width=True)

# Evolution des genres de film par décennie
df['startYear'] = df['startYear'].astype(int)
df_filtered = df[df['startYear'] <= 2023]
df_filtered['decade'] = (df_filtered['startYear'] // 10) * 10
df_genre_count = df_filtered.groupby(['decade', 'genre1']).size().reset_index(name='total_genre')

fig_decade_genre = px.bar(df_genre_count,
             x='genre1',
             y='total_genre',
             color='genre1',
             animation_frame='decade',
             title='Evolution des genres de film par décennie',
             category_orders={'decade': list(range(df_genre_count['decade'].min(), 2024, 10))})

fig_decade_genre.update_layout(yaxis_range=[0, df_genre_count['total_genre'].max() * 1.1], template = 'plotly_dark')
st.plotly_chart(fig_decade_genre, use_container_width=True)

# Distribution des notes moyennes
fig = go.Figure()

fig.add_trace(go.Histogram(
    x=df['averageRating'],
    marker_color='#f8b319',
    name='Note moyenne',
    xbins=dict(
        start=min(df['averageRating']),
        end=max(df['averageRating']),
        size=0.5  # Ajustez la taille des bacs si nécessaire
    )
))
fig.update_layout(
    title='Distribution des notes moyennes',
    xaxis_title='Note moyenne',
    yaxis_title='Nombre de films',
    template='plotly_dark'
)
st.plotly_chart(fig, use_container_width=True)

# Top 5 des films les mieux notés
topscore = pd.Series(collections.Counter(df['averageRating']), name="IMDb Rating").to_frame(name='Count').sort_values(by='Count', ascending=False).head(5)

from plotly.subplots import make_subplots

# Films récents
recent_movies = df[df['startYear'] >= 2022]
recent_movies = recent_movies.sort_values(by=['averageRating'], ascending=False).head(15)
recent_movies = recent_movies.rename(columns={
    'title': 'Titre',
    'startYear': 'Année de sortie',
    'Director_name': 'Réalisateur',
    'genre1': 'Genre principal',
    'averageRating': 'Note moyenne'
})
# Top 15 des films
top15movies = df.sort_values(by=['averageRating'], ascending=False).head(15)
top15movies = top15movies.rename(columns={
    'title': 'Titre',
    'startYear': 'Année de sortie',
    'Director_name': 'Réalisateur',
    'genre1': 'Genre principal',
    'averageRating': 'Note moyenne'
})
# Créer la figure subplot
fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=("15 meilleurs films récents", "Les 15 meilleurs films dans IMDb"),
    specs=[[{'type': 'domain'}, {'type': 'domain'}]]
)
# Ajouter le tableau des films récents
fig.add_trace(
    go.Table(
        header=dict(values=['Titre', 'Année de sortie', 'Réalisateur', 'Catégorie', 'Note'],
                    fill_color='#f8b319',
                    height=30,
                    align='left',
                    font=dict(color='black', size=13)),
        cells=dict(values=[recent_movies['Titre'], recent_movies['Année de sortie'], recent_movies['Réalisateur'], recent_movies['Genre principal'], recent_movies['Note moyenne']],
                   fill_color='lavender',
                   height=30,
                   align='left',
                   font=dict(color='black', size=12))
    ),
    row=1, col=1
)
# Ajouter le tableau des 15 meilleurs films
fig.add_trace(
    go.Table(
        header=dict(values=['Titre', 'Année de sortie', 'Réalisateur', 'Catégorie', 'Note'],
                    fill_color='#f8b319',
                    height=30,
                    align='left',
                    font=dict(color='black', size=13)),
        cells=dict(values=[top15movies['Titre'], top15movies['Année de sortie'], top15movies['Réalisateur'], top15movies['Genre principal'], top15movies['Note moyenne']],
                   fill_color='lavender',
                   height=30,
                   align='left',
                   font=dict(color='black', size=12))
    ),
    row=1, col=2
)
fig.update_layout(height=800, width=1500, template='plotly_dark')
st.plotly_chart(fig, use_container_width=True)

# Répartition des réalisateurs (Word Cloud)
st.title("Répartition des réalisateurs")
plt.figure(facecolor='black', figsize=(14, 6))
data = df['Director_name'].value_counts().to_dict()
wc = WordCloud(width=800, height=400, random_state=1, background_color='black', colormap='rainbow').generate_from_frequencies(data)
plt.imshow(wc)
plt.title('Réalisateurs', fontsize=20)
plt.axis('off')
st.pyplot(plt)

# Les 15 réalisateurs les plus prolifiques (Pie Chart)
st.title("Les 15 réalisateurs les plus prolifiques")
top_directors = df['Director_name'].value_counts().head(15)
pie_fig = px.pie(
    names=top_directors.index,
    values=top_directors.values,
    title='Les 15 réalisateurs les plus prolifiques',
    labels={'names': 'Réalisateur', 'values': 'Nombre de films'},
    width=800,
    height=600,
)
pie_fig.update_traces(textposition='outside', textinfo='percent+label', marker=dict(line=dict(color='#000000', width=2)))
pie_fig.update_layout(template='plotly_dark')
st.plotly_chart(pie_fig, use_container_width=True)

# Diviser les noms des acteurs et actrices dans une liste
df['Actors_Actresses'] = df['Actors_Actresses'].str.split(',')
df_actors = df.explode('Actors_Actresses')

# Get top 20 actors/actresses and their counts
count_actors = df_actors['Actors_Actresses'].value_counts().head(15)

fig = go.Figure(data=[go.Bar(
    x=count_actors.index,
    y=count_actors.values,
    marker=dict(color='#f8b319'),
)])

fig.update_layout(
    title='Acteurs et actrices les plus populaires',
    xaxis_title='Acteur/Actrice',
    yaxis_title='Nombre de films',
    xaxis=dict(tickfont=dict(size=10)),
    height=500,
    margin=dict(l=100, r=20, t=50, b=50),
    template='plotly_dark',
    font=dict(size=10)
)
st.plotly_chart(fig, use_container_width=True)

# Top 5 acteurs/actrices les plus prolifiques par décennie
st.subheader("Top 5 acteurs/actrices les plus prolifiques par décennie")

# Ajouter la colonne 'decade' au DataFrame
df['decade'] = (df['startYear'] // 10) * 10

# Exploser le DataFrame pour avoir une ligne par acteur/actrice par décennie
df_exploded = df.explode('Actors_Actresses')

# Compter le nombre de films par acteur/actrice par décennie
actor_counts_by_decade = df_exploded.groupby(['decade', 'Actors_Actresses']).size().reset_index(name='film_count')

# Trier les acteurs/actrices par décennie en fonction du nombre de films
top_actors_by_decade = actor_counts_by_decade.sort_values(by=['decade', 'film_count'], ascending=[True, False])
top_actors_by_decade = top_actors_by_decade.groupby('decade').head(5)

# Créer le graphique avec Plotly Express
fig = px.bar(
    top_actors_by_decade,
    x='Actors_Actresses',
    y='film_count',
    color='Actors_Actresses',
    animation_frame='decade',
    range_y=[0, top_actors_by_decade['film_count'].max() + 5],
    title='Top 5 acteurs/actrices les plus prolifiques par décennie',
    labels={'film_count': 'Nombre de films', 'Actors_Actresses': 'Acteur/Actrice'},
    height=600
)

# Définir la durée de chaque frame de l'animation
fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 1800

# Mettre à jour la mise en page du graphique
fig.update_layout(xaxis={'categoryorder': 'total descending'}, showlegend=False, template='plotly_dark')

# Afficher le graphique avec Streamlit
st.plotly_chart(fig, use_container_width=True)


# Répartition des maisons de production
production_companies = df['production_companies_name'].value_counts().head(10)

fig_production = px.pie(
    names=production_companies.index,
    values=production_companies.values,
    title='Répartition des 10 maisons de production les plus populaires',
    labels={'names': 'Maisons de production', 'values': 'Pourcentage'},
    width=800,
    height=600,
)

fig_production.update_traces(textposition='outside', textinfo='percent+label', marker=dict(line=dict(color='#000000', width=2)))
fig_production.update_layout(template='plotly_dark')

st.plotly_chart(fig_production, use_container_width=True)
