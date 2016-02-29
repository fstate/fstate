from flask import *
# import pylibmc
from db import *
from itertools import permutations
from datetime import datetime
from copy import deepcopy
from printer import TablePrinter
from json import dumps as json_dump
from bson import ObjectId
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from createdatabase.decay_model import Decay
from createdatabase.save_decay import add_decay
from particleparser.save_particle import save_particle_to_db
import thread

app = Flask(__name__)
# mc = pylibmc.Client(["127.0.0.1"], binary=True,
#                      behaviors={"tcp_nodelay": True,
#                                 "ketama": True})

def cache_key(query):
    return str(" ".join(query))

@app.route("/add-physics")
def add_physics():
    return render_template('AddPhysics.html')

def do_search(query):
    # Set conversion is done for duplicate removing
    query_permutations = [" ".join(x) for x in set(permutations(query, len(query)))]

    # Cache check
    # if cache_key(query) in mc:
    #     return mc[cache_key(query)]
    #Decay.objects(fstate_in = query_permutations)
    #for d in Decay.objects(fstate__in = query_permutations):
    #    d.printdecay()
        #json_dump(d.to_json)
    #result = sorted(Decay.objects(fstate__in = query_permutations),  key=lambda x: -x['branching'])
    result = []
    for d in Decay.objects(fstate__in = query_permutations):
        result.append(d.to_dict())

    #result = sorted(list(fstates.find(
    #        {"fstate": {"$in": query_permutations}}, 
    #        {"_id": False})),  key=lambda x: -x['branching'][0])

    # for q in query_permutations:
    #     mc[cache_key(q)] = result

    return result


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/howto-search")
def howtosearch():
    return render_template('HowToSearch.html')

#@app.route("/results/<query>")
#def showResults(query):


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

def nice_br(br):
    e = 0
    if br>1:
        return str(br).split(".")[0]+"."+str(br).split(".")[1][1]
    while br<1:
        e+=1
        br*=10
    return str(br).split(".")[0]+"."+str(br).split(".")[1][0]+"e-"+str(e)

@app.route('/results/<query>.json')
def json(query):
    if not query:
        return redirect('/')

    query = [x for x in query.split(' ') if x != '']

    start = datetime.now()
    result = do_search(query)
    end = datetime.now()   
    for r in result:
        r['branching'] = nice_br(r['branching'])
        #r['branching'] = "%0.4g" % r['branching']       

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
        r['branching'] = nice_br(r['branching'])
        #r['branching'] = "%0.4g" % r['branching']
        #r['branching'] = "%0.4g" % r['branching'][0]
    
    return Response(TablePrinter(format, ul='-')(result), mimetype='text/plain')


## -------- Bobak's Code -------- ##

@app.route("/add_decay", methods=["POST"])
def addDecay():
    """Adds POST data to new_physics collection, displays a thank you message"""
    request.get_data()
    
    document = {"type": "decay", "mother": "", "daughters": [], "source": "", "comment": "", "br_frac": ""}

    document["mother"] = request.form["mother"]
    document["source"] = request.form["decay_source"]
    document["comment"] = request.form["decay_comment"]
    document["br_frac"] = request.form["branching_fraction"]

    for i in request.form:
        if "daughter" in i:
            document["daughters"].append(request.form[i])


    new_physics.insert_one(document)

    return render_template("physics-added.html")

@app.route("/add_particle", methods=["POST"])
def addParticle():
    """Adds POST data to new_physics collection, displays a thank you message"""
    request.get_data()
    print(request.form)
    document = {"type": "particle", "name": "", "mass": "", "source": "", "comment": "", "charge" : "", "antiparticle": ""}

    document["name"] = request.form["new_particle_name"]
    document["mass"] = request.form["new_particle_mass"]
    document["source"] = request.form["new_particle_source"]
    document["comment"] = request.form["new_particle_comment"]
    document["charge"] = request.form["new_particle_charge"]
    document["antiparticle"] = request.form["new_particle_antiparticle"]

    new_physics.insert_one(document)

    return render_template("physics-added.html")

def getNewPhysics(t):
    """Returns all rows of the new_physics table with type t as a list"""
    rows = new_physics.find({"type": t})
    return [i for i in rows]

def addDecayLive(document):
    """Adds decay specified by document to the live fstate decays table"""
    #Ilya: I don't know waht the document is, but it should contain:
    # - name of decayed particle (father)
    # - branching of the decay (branching)
    # - list of daughter particles (list_of_daughters)
    #After it, decay should be saved by this command:
    #thread.start_new_thread(add_decay, (father, {"branching":branching, "daughters":list_of_daughters))
    #for example:
    #thread.start_new_thread(add_decay, ("anti-B0", {"branching":0.0493, "daughters":["e-",
    #                                                       "nu_e~",
    #                                                       "nu_tau",
    #                                                       "gamma"
    #                                                   ]}))
    #The process of adding the decay is moved to separate thread to run in the background.
    pass

@app.route("/admin_panel/rm/<table>/<id>")
def rmNewPhys(table,id):
    """also accepts post arguments that let you remove a preliminary decay/particle or add it to the live table"""
    try:
        ret=new_physics.remove({"_id":ObjectId(id), "type": table})
        if ret['n'] == 1:
            return Response(json_dump({'result' : True, "err": ""}), mimetype='application/json')
        else:
            return Response(json_dump({'result' : False, "err": "%i rows removed" % ret['n'] }), mimetype='application/json') 
    except Exception as err:
        return Response(json_dump({'result' : true, "err": str(err)}), mimetype='application/json')

@app.route("/admin_panel")
def adminPanel():
    """Renders admin panel"""
    decs = getNewPhysics("decay")
    particles = getNewPhysics("particle")
    return render_template("admin_panel.html", decs=decs, particles=particles)

## -------- Bobak's Code -------- ##


if __name__ == "__main__":
    app.run(debug=True)