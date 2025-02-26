from flask import Flask, Response
import io
from models import Corpus
from analysis import Distribution
import plotly.io as pio
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

corpus= Corpus.from_pickle('corpus.pkl')
dist = Distribution(corpus)


@app.route('/base-distribution')
def get_base_dist():
    fig_html = pio.to_html(dist.fig, full_html=False,include_plotlyjs=False, div_id='graph-container')

    # Return the HTML div directly
    return Response(fig_html, mimetype='text/html')
    
    return
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
