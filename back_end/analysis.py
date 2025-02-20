from models import Corpus
from constants import InfrastructureType, Dimension, reverse_map
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


class Distribution():
    def __init__(self, corpus):
        self.corpus = corpus
        self.claims =  [claim for article in self.corpus.articles for claim in article.claims]
        self.chart = None 
        self.distribution = {
            x: {
                y: {
                    z: [] for z in (i.value for i in Dimension)
                } for y in (j.value for j in InfrastructureType)
            } for x in set(reverse_map.values()) 
            }
         
        for claim in self.claims:
            self.distribution[reverse_map[claim.infrastructure.value]][claim.infrastructure.value][claim.dimension.value].append(claim.valence)


if __name__ == '__main__':
    corpus = Corpus.from_pickle('../corpus.pkl')
    self = Distribution(corpus)
    # Prepare data for plotting
    plot_data = { z: {} for z in (i.value for i in Dimension) }

    for category, subcategories in self.distribution.items():
        for subcategory, data in subcategories.items():
            for dim, value in data.items():
                plot_data[dim][subcategory] = value

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

    # Adjust layout
    plt.tight_layout()
    plt.savefig('fig')
