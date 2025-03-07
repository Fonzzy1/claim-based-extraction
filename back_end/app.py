from flask import Flask, Response, request, jsonify
from flask import Response, jsonify
import io
from models import Corpus
from analysis import Distribution
import plotly.io as pio
from flask_cors import CORS
from models import Text

app = Flask(__name__)
CORS(app, methods=['POST','GET'])

corpus= Corpus.from_pickle('corpus.pkl')
dist = Distribution(corpus)


@app.route('/base-distribution')
def get_base_dist():
    fig_html = pio.to_html(dist.fig, full_html=False,include_plotlyjs=False, div_id='graph-container')

    # Return the HTML div directly
    return Response(fig_html, mimetype='text/html')

@app.route('/analyze', methods=['POST'])
def anylise():
    text = request.get_json()['text']
    text_class = Text(text)
    text_class.analyze_text()
    text_class.evaluate_all()

    stat, p = dist.compare_article(text_class)
    plot = dist.plot_text(text_class)
    


    return jsonify(
        {'p': p,
         'plot': pio.to_html(plot, full_html=False, include_plotlyjs=False, div_id='graph-container'),
         'claims': [claim.__getstate__() for claim in text_class.claims]
         })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
