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
from parrticleparser.particle_model import Particle
from createdatabase.save_decay import add_decay
from parrticleparser.save_particle import save_particle_to_db
import thread

app = Flask(__name__)
# mc = pylibmc.Client(["127.0.0.1"], binary=True,
#                      behaviors={"tcp_nodelay": True,
#                                 "ketama": True})

def cache_key(query):
    return str(" ".join(query))

@app.route("/add-physics")
def add_physics():
    p_list = []
    for p in Particle.objects():
        p_list.append(p.to_print())
    return render_template('AddPhysics.html', p_list = p_list)

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
    p_list = []
    for p in Particle.objects():
        p_list.append(p.to_print())
    return render_template('HowToSearch.html', p_list = p_list)

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
    p_list = {}
    for p in Particle.objects():
        p_list[p.to_dict()["name"]]=p.to_print()

    return Response(json_dump({'result' : result, 'time': str(end-start), 'p_list':p_list}), mimetype='application/json')

@app.route('/queries/<query>.json')
def p_json(query):
    if query=="null":
        p_names = []
        for p in Particle.objects():
            p_names.append(p.name)
        return Response(json_dump({'p_names':p_names}), mimetype='application/json')
    p_names = []
    last = query.split(" ")[-1]
    n_tot=10
    for p in Particle.objects():
        if last == p.name[0:len(last)]:
            p_names.append(query[:-len(last)]+p.name)
            n_tot-=1
        if n_tot<1:
            break
    return Response(json_dump({'p_names':p_names}), mimetype='application/json')



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
    
    document = {"type": "decay", "mother": "", "daughters": [], "source": "", "comment": "", "br_frac": "", "status":"pending"}

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
    document = {"type": "particle", "name": "", "mass": "", "source": "", "comment": "", "charge" : "", "antiparticle": "", "status":"pending"}

    document["name"] = request.form["new_particle_name"]
    document["mass"] = request.form["new_particle_mass"]
    document["source"] = request.form["new_particle_source"]
    document["comment"] = request.form["new_particle_comment"]
    document["charge"] = request.form["new_particle_charge"]
    document["antiparticle"] = request.form["new_particle_antiparticle"]

    new_physics.insert_one(document)

    return render_template("physics-added.html")

def getNewPhysics(t, status):
    """Returns all rows of the new_physics table with type t as a list"""
    rows = new_physics.find({"type": t, "status":status})
    return [i for i in rows]


def addDecayLive(document):
    """Adds decay specified by document to the live fstate decays table"""
    thread.start_new_thread(add_decay, (document["father"], 
                                        {"branching":document["branching"], 
                                        "daughters":document["daughters"]}, "", document["daughters"]))
    pass

def addParticleLive(document):
    """Adds decay specified by document to the live fstate decays table"""
    save_particle_to_db(name = document["name"],
                        charge = document["charge"],
                        mass = document["mass"],
                        antiparticle = document["antiparticle"])
    pass

@app.route("/admin_panel/rm/<table>/<id>")
def rmNewPhys(table,id, status = "declined"):
    """also accepts post arguments that let you remove a preliminary decay/particle or add it to the live table"""
    try:
        #ret=new_physics.remove({"_id":ObjectId(id), "type": table})
        ret=new_physics.update({"_id":ObjectId(id), "type": table}, 
                                {'$set':{'status': status}})
        if ret['n'] == 1:
            return Response(json_dump({'result' : True, "err": ""}), mimetype='application/json')
        else:
            return Response(json_dump({'result' : False, "err": "%i rows removed" % ret['n'] }), mimetype='application/json') 
    except Exception as err:
        return Response(json_dump({'result' : true, "err": str(err)}), mimetype='application/json')

@app.route("/admin_panel/add/<table>/<id>")
def addNewPhys(table,id):
    for ret in new_physics.find({"_id":ObjectId(id), "type": table}):
        if table == 'particle':
            if not ret["antiparticle"] == "":
                document = {"name": ret["name"],
                            "charge": int(ret["charge"]),
                            "mass": float(ret["mass"])*1000,
                            "antiparticle": ret["antiparticle"]}
            else:
                document = {"name": ret["name"],
                            "charge": int(ret["charge"]),
                            "mass": float(ret["mass"])*1000,
                            "antiparticle": ret["name"]}
            addParticleLive(document)
            print("Particle added")
            return rmNewPhys(table,id, "approved")
        if table == 'decay':
            document = {"father":ret['mother'], 
                        "branching":ret["br_frac"], 
                        "daughters":ret["daughters"]}
            addDecayLive(document)
            print("Adding decay, may take some time.")
            return rmNewPhys(table,id, "approved")

@app.route("/admin_panel")
def adminPanel():
    """Renders admin panel"""
    decs_pending = getNewPhysics("decay","pending")
    particles_pending = getNewPhysics("particle","pending")
    decs_approved = getNewPhysics("decay","approved")
    particles_approved = getNewPhysics("particle","approved")
    decs_declined = getNewPhysics("decay","declined")
    particles_declined = getNewPhysics("particle","declined")
    return render_template("admin_panel.html", decs_pending=decs_pending, particles_pending=particles_pending, 
                                               decs_approved=decs_approved, particles_approved=particles_approved,
                                               decs_declined=decs_declined, particles_declined=particles_declined)

## -------- Bobak's Code -------- ##


if __name__ == "__main__":
    app.run(debug=True)