#! docker compose exec -it back-end python3
from models import Corpus, Text, Article
from typing import Union
from constants import InfrastructureType, Dimension, reverse_map
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from copy import deepcopy
from scipy.stats import ks_2samp, chi2
import numpy as np

def fisher_combined_p_value(p_values):
    """
    Combines p-values using Fisher's method.
    """
    # Calculate the test statistic
    chi2_stat = -2 * np.sum(np.log(p_values))
    df = 2 * len(p_values)
    # Calculate the combined p-value
    combined_p_value = 1 - chi2.cdf(chi2_stat, df)
    return combined_p_value

class Distribution():
    def __init__(self, corpus):
        self.corpus = corpus
        self.claims =  [claim for article in self.corpus.articles for claim in article.claims]
        self.fig = None 
        self.distribution = {
            y: {
                    z: [] for z in (i.value for i in Dimension)
                } for y in (j.value for j in InfrastructureType)
            }
         
        for claim in self.claims:
            self.distribution[claim.infrastructure.value][claim.dimension.value].append(claim.valence)
        self.create_base_chart()

    def create_base_chart(self):
        plot_data = { z: {} for z in (i.value for i in Dimension) }

        for category, data in self.distribution.items():
                for dim, value in data.items():
                    plot_data[dim][category] = value

        unique_groups = set(reverse_map.values())
        color_map = {group: color for group, color in zip(unique_groups, mcolors.TABLEAU_COLORS)}

        # Set up the subplot
        fig, axs = plt.subplots(nrows=len(plot_data.keys()), ncols=1, figsize=(14, 10))

        for i, dim in enumerate(plot_data.keys()):
            subcategories = list(plot_data[dim].keys())
            data = list(plot_data[dim].values())
            
            # Colors based on group membership via reverse_map
            colors = [color_map[reverse_map[subcategory]] for subcategory in subcategories]

            bplot = axs[i].boxplot(data, patch_artist=True, vert=False)
            
            for patch, color in zip(bplot['boxes'], colors):
                patch.set_facecolor(color)
            
            axs[i].set_title(dim)
            axs[i].set_xlabel('Score')
            axs[i].set_ylabel('Energy Subcategory')
            axs[i].set_yticklabels(subcategories)
        self.fig = fig

    def make_comparison_graph(self, text: Union[Text, Article]):
        new_fig = deepcopy(self.fig)
        for ax in new_fig.axes:
            dim = ax.title.get_text()
            needed_claims = [claim for claim in text.claims if claim.dimension.value == dim]
            for claim in needed_claims:
                # Get the index of the subcategory
                subcategory_index = list(self.distribution.keys()).index(claim.infrastructure.value)
                # Plot each claim as a distinct point on the box plot
                ax.scatter(claim.valence, subcategory_index + 1, color='black', zorder=3, marker='x')
        return new_fig

    def compare_article(self, text):
        """
        Compare the valence distributions of the article to the
        corpus distribution using KS test for each dimension and 
        infrastructure pair.
        """
        results = {}
        for category, data in self.distribution.items():
            for dim, corpus_values in data.items():
                # Extract article claims for the current dimension and infrastructure pair
                text_values = [
                    claim.valence for claim in text.claims
                    if claim.dimension.value == dim and claim.infrastructure.value == category
                ]
                
                if text_values:
                    # Perform KS test
                    stat, p_value = ks_2samp(corpus_values, text_values)
                    results[(category, dim)] = (stat, p_value)
        return fisher_combined_p_value( [x[1] for x in results.values()]), results


