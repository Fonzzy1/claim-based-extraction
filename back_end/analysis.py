#! docker compose exec -it back-end python3
from constants import InfrastructureType, Dimension, reverse_map
import numpy as np
from scipy.stats import ks_2samp
from models import Corpus
from scipy.stats import combine_pvalues
from copy import deepcopy
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


class Distribution():
    def __init__(self, corpus):
        self.corpus = corpus
        self.claims =  [claim for article in self.corpus.articles for claim in article.claims]
        self.distribution = { (z,y):[] for z in (i.value for i in Dimension) for y in (j.value for j in InfrastructureType)}

        for claim in self.claims:
            self.distribution[(claim.dimension.value, claim.infrastructure.value)].append(claim.valence)


        self.fig = None 
        self.create_base_plot()

    def compare_article(self, text):
        """
        Compare the valence distributions of the article to the
        corpus distribution using KS test for each dimension and 
        infrastructure pair.
        """
        text_dist = { k:[] for k in self.distribution.keys()}
        for claim in text.claims:
            text_dist[(claim.dimension.value, claim.infrastructure.value)].append(claim.valence)

        individual_p_values = []

        for pair in self.distribution.keys():
            corpus_valences = self.distribution[pair]
            new_article_valences = text_dist.get(pair, [])

            if new_article_valences:  # Ensure there's data to compare
                ks_statistic, p_value = ks_2samp(corpus_valences, new_article_valences)
                individual_p_values.append(p_value)
        # Combining the p-values obtained from individual tests

        combined_statistic, combined_p_value = combine_pvalues(individual_p_values, method='fisher')

        return combined_statistic, combined_p_value

    def create_base_plot(self):
        # Extract the data lists from the dictionary

        data = [{"value": val, "dimension": dim, "infrastructure": infra} for (dim, infra), vals in self.distribution.items() for val in vals]
        df = pd.DataFrame(data)

        self.fig = px.box(df, x="value", y="infrastructure", color='dimension',notched=False)

    def plot_text(self, text):
        new_plot = deepcopy(self.fig)
        data = [{"value": claim.valence, "dimension": claim.dimension.value, "infrastructure": claim.infrastructure.value} for claim in text.claims]
        df = pd.DataFrame(data)

        
        # Iterate over each dimension to create separate scatter traces
        for dimension in df['dimension'].unique():
            dimension_data = df[df['dimension'] == dimension]
            scatter = go.Scatter(
                x=dimension_data['value'],
                y=dimension_data['infrastructure'],
                mode='markers',
                marker=dict(
                    size=10  # Set the size of the markers here
                ),
                name=f'Claims - {dimension}',  # Display name for legend
                showlegend=True
            )
            new_plot.add_trace(scatter)
        new_plot.write_html('test2.html')

        return new_plot






if __name__=='__main__':
    corpus= Corpus.from_pickle('corpus.pkl')
    self= Distribution(corpus)
    self.fig.write_html("interactive_plot.html")

    most_contrarian = 1
    index = -1
    for i,text in enumerate(corpus.articles):
        stat, p = self.compare_article(text)
        if p < most_contrarian:
            most_contrarian = p
            index= i
    self.plot_text(text)
        



