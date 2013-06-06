from flask import *
from db import *
from itertools import permutations
from datetime import datetime
from copy import deepcopy
from printer import TablePrinter

app = Flask(__name__)


def do_search(query):
    workq = []
    for i in query:
        if i not in workq:
            workq.append(i)
    if len(query)==len(workq):
        return list(fstates.find(
            {"fstate": {
                        "$all": query, 
                        "$size": len(query)}}, 
            {'_id': False}))
    done = []
    lst = []
    a = []
    for k in permutations(query):
        if k not in done:
            a = list(fstates.find( {"fstate": k }, {'_id': False}))
            lst += a
            done.append(k)
    return lst
    

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/HowToSearch")
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
    
    return render_template('results.html', query=" ".join(query), results=results, timing=(end - start))


@app.route('/<query>.json')
def json(query):
    if not query:
        return redirect('/')

    query = [x for x in query.split(' ') if x != '']

    start = datetime.now()
    result = sorted(do_search(query), key=lambda x: -x['branching'][0])
    end = datetime.now()

    
    return Response(result, mimetype='application/json')


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