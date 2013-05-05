from flask import *
from db import *

app = Flask(__name__)

@app.route("/")
@app.route("/<query>")
def index(query=None):
    if not query:
        return "Welcome to fstate - searc engine for particle physics!"
    
    results = fstates.find({'fstate': query.split(' ')}).sort("branching", -1)
    final_results = []


    for r in results:
        r['scheme'] = [decays.find_one({"decay_id" : x, }) for x in r['scheme']]
        final_results.append(r)
    
    return render_template('index.html', query=query, results=final_results)

if __name__ == "__main__":
    app.run(debug=True)