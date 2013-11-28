from flask import *
import pylibmc
from db import *
from itertools import permutations
from datetime import datetime
from copy import deepcopy
from printer import TablePrinter
from json import dumps as json_dump

app = Flask(__name__)
mc = pylibmc.Client(["127.0.0.1"], binary=True,
                     behaviors={"tcp_nodelay": True,
                                "ketama": True})

def cache_key(query):
    return str(" ".join(query))


def do_search(query):
    # Set conversion is done for duplicate removing
    query_permutations = [" ".join(x) for x in set(permutations(query, len(query)))]

    # Cache check
    if cache_key(query) in mc:
        return mc[cache_key(query)]

    result = sorted(list(fstates.find(
            {"fstate": {"$in": query_permutations}}, 
            {"_id": False})),  key=lambda x: -x['branching'][0])

    for q in query_permutations:
        mc[cache_key(q)] = result

    return result


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/howto-search")
def howtosearch():
    return render_template('HowToSearch.html')


@app.route("/")
def index():
    query = request.args.get('query')
    
    if not query:
        return render_template('index.html')

    query = [x for x in query.split(' ') if x != '']

    start = datetime.now()
    results = do_search(query)
    end = datetime.now()
    
    return render_template('results.html', query=request.args.get('query'), results=results, timing=(end - start))


@app.route('/<query>.json')
def json(query):
    if not query:
        return redirect('/')

    query = [x for x in query.split(' ') if x != '']

    start = datetime.now()
    result = do_search(query)
    end = datetime.now()

    
    return Response(json_dump({'result' : result, 'time': str(end-start)}), mimetype='application/json')


format = [
    ('Branching',       'branching',   15),
    ('Scheme',          'scheme',       120),
]


@app.route('/<query>.txt')
def txt(query):
    if not query:
        return redirect('/')

    query = [x for x in query.split(' ') if x != '']

    start = datetime.now()
    result = do_search(query)
    end = datetime.now()

    for r in result:
        r['branching'] = "%0.4g" % r['branching'][0]
    
    return Response(TablePrinter(format, ul='-')(result), mimetype='text/plain')

if __name__ == "__main__":
    app.run(debug=True)