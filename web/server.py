from flask import *
from db import *
from itertools import permutations
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def index():
    query = request.args.get('query')
    
    if not query:
        return render_template('index.html')

    start = datetime.now()
    query = [x for x in query.split(' ') if x != '']
    query_permutations = list(permutations(query, len(query)))

    results = fstates.find({"fstate": {"$in": query_permutations}}).sort("branching", -1)

    html =  render_template('results.html', query=" ".join(query), results=results)
    
    end = datetime.now()
    print 'Time for query "{}" - {}'.format(request.args.get('query'), end - start)
    
    return html


if __name__ == "__main__":
    app.run(debug=True)