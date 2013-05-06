from flask import *
from db import *
from itertools import permutations

app = Flask(__name__)

@app.route("/")
def index():
    query = request.args.get('query')
    
    if not query:
        return render_template('index.html')

    query = [x for x in query.split(' ') if x != '']
    query_permutations = list(permutations(query, len(query)))

    results = fstates.find({"fstate": {"$in": query_permutations}}).sort("branching", -1)

    print "Found ", results.count()
    return render_template('results.html', query=query, results=results)




if __name__ == "__main__":
    app.run(debug=True)