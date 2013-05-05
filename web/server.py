from flask import *
from db import *
from itertools import permutations

app = Flask(__name__)

@app.route("/")
@app.route("/<query>")
def index(query=None):
    if not query:
        return "Welcome to fstate - searc engine for particle physics!"

    query = [x for x in query.split(' ') if x != '']
    query_permutations = list(permutations(query, len(query)))

    results = fstates.find({"fstate": {"$in": query_permutations}}).sort("branching", -1)
    
    final_results = []

    for r in results:
        r['scheme'] = [decays.find_one({"decay_id" : x, }) for x in r['scheme']]
        final_results.append(r)

    return render_template('index.html', query=query, results=final_results)

if __name__ == "__main__":
    app.run(debug=True)