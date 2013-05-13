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

    query = [x for x in query.split(' ') if x != '']
    query_permutations = list(permutations(query, len(query)))


    start = datetime.now()

    results = list(fstates.find({"fstate": {"$in": query_permutations}}))

    end = datetime.now()
    
    results = sorted(results, key=lambda x: -x['branching'][0])
    

    print 'Time for query "{}" - {}'.format(request.args.get('query'), end - start)
    
    return render_template('results.html', query=" ".join(query), results=results, timing=(end - start))


if __name__ == "__main__":
    app.run(debug=True)