from flask import *
from flask.ext.cache import Cache
from db import *
from itertools import permutations
from datetime import datetime
from copy import deepcopy
from printer import TablePrinter
from json import dumps as json_dump

app = Flask(__name__)
cache = Cache()
cache.init_app(app, config={'CACHE_TYPE': 'simple'})


@cache.memoize()
def do_search(query):
    if len(query) == len(set(query)):
        # Search without duplicates
        return list(fstates.find(
            {"fstate": {
                        "$all": query, 
                        "$size": len(query)}}, 
            {'_id': False}))
    else:
        # convertion to set is done for removing duplicates.
        query_permutations = list(set(permutations(query, len(query))))
 
        return sorted(list(
        fstates.find(
             {"fstate": {"$in": query_permutations}}, 
             {'_id': False})
        ), key=lambda x: -x['branching'][0])
    


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

    results = sorted(do_search(query), key=lambda x: -x['branching'][0])

    end = datetime.now()
    

    print 'Time for query "{}" - {}'.format(request.args.get('query'), end - start)
    
    return render_template('results.html', query=request.args.get('query'), results=results, timing=(end - start))


@app.route('/<query>.json')
def json(query):
    if not query:
        return redirect('/')

    query = [x for x in query.split(' ') if x != '']

    start = datetime.now()
    result = sorted(do_search(query), key=lambda x: -x['branching'][0])
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

    result = sorted(do_search(query), key=lambda x: -x['branching'][0])

    end = datetime.now()

    for r in result:
        r['branching'] = "%0.4g" % r['branching'][0]
    
    return Response(TablePrinter(format, ul='-')(result), mimetype='text/plain')

if __name__ == "__main__":
    app.run(debug=True)