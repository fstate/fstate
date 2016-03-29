from flask import *
from flask.ext.htpasswd import HtPasswdAuth

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
from createdatabase.config import br_cutoff, max_decay_chain
import threading
import thread

app = Flask(__name__)
app.config['FLASK_HTPASSWD_PATH'] = '.htpasswd'
app.config['FLASK_SECRET'] = 'Security Secret'

htpasswd = HtPasswdAuth(app)


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
    print br_cutoff
    print max_decay_chain
    return render_template('about.html')


@app.route("/howto-search")
def howtosearch():
    p_list = []
    for p in Particle.objects():
        p_list.append(p.to_print())
    return render_template('HowToSearch.html', p_list = p_list)

@app.route("/knowndecays/<query>")
def knowndecays(query):
    d_list = []
    for d in Decay.objects(father = query.replace("__","/"), primal_decay = True):
        d_list.append(d.to_dict())
    for d in d_list:
        d['branching'] = nice_br(d['branching'])
    return render_template('SingleParticle.html', particle = query.replace("__","/"), d_list = d_list)


#@app.route("/results/<query>")
#def showResults(query):


@app.route("/")
def index():
    query = request.args.get('query')
    
    if not query:
        return render_template('index.html', br_cutoff = str(br_cutoff), max_decay_chain = max_decay_chain)

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

    p_list = []
    for p in Particle.objects():
        p_list.append(p.to_dict()["name"])

    if document["mother"] not in p_list:
        return render_template("physics-not-added.html", reason = "Mother particle is unknown. Add it to the db or use drop-down menu")

    for d in document["daughters"]:
        if d not in p_list:
            return render_template("physics-not-added.html", reason = "One of the daughter ("+d+") particles is unknown. Add it to the db or use drop-down menu")

    try:
        b = float(document["br_frac"])
        if (b>1) or (b<0):
            return render_template("physics-not-added.html", reason = "Branching fraction should be in range (0, 1)")
    except:
        return render_template("physics-not-added.html", reason = "Branching fraction should be a number in range (0, 1)")

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

    try:
        m = float(document["mass"])
        if m<0:
            return render_template("physics-not-added.html", reason = "Particles shouldn't have negative mass")
    except:
        return render_template("physics-not-added.html", reason = "Particle mass should be a number")

    try:
        e = float(document["charge"])
    except:
        return render_template("physics-not-added.html", reason = "Particle charge should be a number")


    new_physics.insert_one(document)

    return render_template("physics-added.html")

def getNewPhysics(t, status):
    """Returns all rows of the new_physics table with type t as a list"""
    rows = new_physics.find({"type": t, "status":status})
    return [i for i in rows]

def user_key_from_document(document):
    try:
        return "{} --> {}".format(document["father"], ' '.join(document["daughters"]))
    except:
        print "Failed to create user key, returning empty"
        return ""

def addDecayLive(document):
    """Spawns a thread that calls the add_decay method to insert the decay specified by document to the live fstate decays table"""
    t=threading.Thread(target=add_decay, args=(document["father"], 
                                        {"branching":document["branching"], 
                                        "daughters":document["daughters"]}, "","", document["daughters"], False))
    t.start()

def addParticleLive(document):
    """Adds decay specified by document to the live fstate decays table"""
    save_particle_to_db(name = document["name"],
                        charge = document["charge"],
                        mass = document["mass"],
                        antiparticle = document["antiparticle"])
    pass

def delete_decays_by_key(key):
    for d in Decay.objects(user_keys__contains = key):
        #print("Deleting decay:")
        #d.printdecay()
        d.delete()

#@login_required
@app.route("/admin_panel/reconsider/<table>/<id>")
@htpasswd.required
def reconsiderNewPhys(table,id, user):
    for ret in new_physics.find({"_id":ObjectId(id), "type": table}):
        if ret["status"]=="declined":
            return rmNewPhys(table,id, user=user, status="pending")
        if table == 'decay':
            if ret["status"]=="approved":
                document = {"father":ret['mother'], 
                        "branching":ret["br_frac"], 
                         "daughters":ret["daughters"]}
                user_key = user_key_from_document(document)
                if user_key != "":
                    thread.start_new_thread(delete_decays_by_key, (user_key,))
                    return rmNewPhys(table,id,user=user, status="pending")
                else:
                    err = "Failed to create user key for decay"
                    return Response(json_dump({'result' : False, "err": str(err)}), mimetype='application/json')
        else:
            return rmNewPhys(table,id,user=user, status="pending")

@app.route("/admin_panel/rm/<table>/<id>")
@htpasswd.required
def rmNewPhys(table,id, user, status = "declined"):
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

@app.route("/admin_panel/delete/<table>/<id>")
@htpasswd.required
def spamNewPhys(table,id, user, status = "declined"):
    """also accepts post arguments that let you remove a preliminary decay/particle or add it to the live table"""
    try:
        ret=new_physics.remove({"_id":ObjectId(id), "type": table})
        if ret['n'] == 1:
            return Response(json_dump({'result' : True, "err": ""}), mimetype='application/json')
        else:
            return Response(json_dump({'result' : False, "err": "%i rows removed" % ret['n'] }), mimetype='application/json') 
    except Exception as err:
        return Response(json_dump({'result' : False, "err": str(err)}), mimetype='application/json')


@app.route("/admin_panel/add/<table>/<id>")
@htpasswd.required
def addNewPhys(table,id,user):
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
            return rmNewPhys(table,id,user=user, status="approved")
        if table == 'decay':
            document = {"father":ret['mother'], 
                        "branching":ret["br_frac"], 
                        "daughters":ret["daughters"]}
            addDecayLive(document)
            print("Adding decay, may take some time.")
            return rmNewPhys(table,id,user=user, status="approved")

@app.route("/admin_panel")
@htpasswd.required
def adminPanel(user):
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
