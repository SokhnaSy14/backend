import flask
import os
import glob
import os
import sys
from flask_cors import CORS
from flask import request, redirect, url_for, jsonify,send_file, send_from_directory, safe_join, abort ,render_template

import requests
import re
import json
import datetime
from datetime import datetime
from datetime import date
import pandas as pd
from recommendation import downloadCV


import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Ahm@ddaba1417",
  database="atos_db",
  autocommit=True
)
cur= mydb.cursor()

app = flask.Flask(__name__)
app.config["DEBUG"] = False
app.config['JSON_SORT_KEYS'] = False

CORS(app)

BASE_PATH = os.path.abspath(os.path.join(__file__, "../.."))
sys.path.append(BASE_PATH+"/recommendation_system/backend/app/")

from recommendation import axe_2_temps_plein, axe_2_temps_partiel

from recommendation import make_mail


import pandas as pd
sql='''#INSERT INTO  prolongementmission (id_prolongement, date_fin_prolongement, id_mission) VALUES (1, DATE  '2021-9-17',1)
SELECT personne.id_personne, firstname, lastname, ad_mail, statutcandidat.libelle_statut AS statut_candidat, date_changement AS date_changement_statut  , changementstatutcandidat.id_demande, mission.date_debut AS debut_mission, mission.date_fin AS fin_mission, prolongementmission.date_fin_prolongement AS fin_prolongement, nom_loc AS localisation
FROM personne
LEFT JOIN changementstatutcandidat ON personne.id_personne=changementstatutcandidat.id_personne
LEFT JOIN 
statutcandidat ON changementstatutcandidat.id_sc=statutcandidat.id_sc
LEFT JOIN mission ON 
changementstatutcandidat.id_demande=mission.id_demande
LEFT JOIN prolongementmission ON prolongementmission.id_mission=mission.id_mission
LEFT JOIN demande ON 
demande.id_demande=mission.id_demande
LEFT JOIN localisation ON demande.id_loc = localisation.id_loc where libelle_statut = "staffe" '''

sql_1='''#INSERT INTO  prolongementmission (id_prolongement, date_fin_prolongement, id_mission) VALUES (1, DATE  '2021-9-17',1)
    SELECT personne.id_personne, firstname, lastname, ad_mail, statutcandidat.libelle_statut AS statut_candidat, date_changement AS date_changement_statut  , changementstatutcandidat.id_demande, mission.date_debut AS debut_mission, mission.date_fin AS fin_mission, prolongementmission.date_fin_prolongement AS fin_prolongement, nom_loc AS localisation
    FROM personne
    LEFT JOIN changementstatutcandidat ON personne.id_personne=changementstatutcandidat.id_personne
    LEFT JOIN 
    statutcandidat ON changementstatutcandidat.id_sc=statutcandidat.id_sc
    LEFT JOIN mission ON 
    changementstatutcandidat.id_demande=mission.id_demande
    LEFT JOIN prolongementmission ON prolongementmission.id_mission=mission.id_mission
    LEFT JOIN demande ON 
    demande.id_demande=mission.id_demande
    LEFT JOIN localisation ON demande.id_loc = localisation.id_loc where libelle_statut = "staffe"  AND charge = "temps partiel" '''



candidates_infos=pd.read_sql(sql,con=mydb)
candidates_infos=candidates_infos.fillna(-1)

candidates_infos_1=pd.read_sql(sql_1,con=mydb)
candidates_infos_1=candidates_infos_1.fillna(-1)



@app.route("/api/check_sanity")
def hello():
    return jsonify("Server running on port {}".format(5001))

@app.route("/assets/<name>",methods=["GET"])
def assets(name):
    return send_file(BASE_PATH+"/app/assets/{}".format(name))

@app.route('/', methods=['POST','GET'])
def root():
    return render_template('index.html') 

#@app.route('/recommandation/', methods=['POST', 'GET'])
#def recomm():
    #post=''
    #comp=''
    #exp=''
    #debut_projet=''
    #dispo=''
    #recomm=[]
    #post = request.form['post']
    
    #comp = request.form['comp']
    
    #exp =int(request.form['exp'])
    
    #debut_projet=date.fromisoformat(request.form['projet'])
    
    #dispo=int(request.form['dispo'])

    #headers = {'Content-Type': 'text/plain',}
    #data = '{"querySearch":"'+comp+'"}'
    #response = requests.post('http://localhost:5000/api/v2/search/rank', headers=headers, data=data)
    #content=json.loads(response.content)
    #candidates=content["final_score"]
        
    #for i, c in enumerate(candidates):
        #id=i+1
        #name=c['name'][8:]
        #score='{} %'.format(c["score"])
        #mail=make_mail(name)
        #recomm.append(axe_2(dispo,mail, debut_projet,score, id))
    #return jsonify(recomm)


@app.route('/api/v1/', methods=['POST', 'GET'])
def recommand():

    post=''
    comp=''
    exp=''
    debut_projet=''
    dispo=''
    lang = ''
    emploi = ''
    recomm=[]
    df_result=[]
    df_recomm=[]
    df_glob=[]
    result=[]
    candidate_info=[]

    if 'post' in request.args and 'comp' in request.args and 'exp' in request.args and 'projet' in request.args and 'dispo' in request.args:

       # Récupération des donnnées fournies dans le formulaire
        post = request.args['post']
    
        comp = request.args.get('comp')
    
        exp =int(request.args.get('exp'))
    
        debut_projet=date.fromisoformat(request.args.get('projet'))
    
        dispo=int(request.args.get('dispo'))

        lang = str(request.args.get('langue')) + ' ' + str(request.args.get('level'))

        emploi = request.args.get('emploi')

# Requete avec  l'Api du moteur de recherche pour récupérer les candidats
        headers = {'Content-Type': 'text/plain',}
        data = '{"querySearch":"'+comp+'"}'
        response = requests.post('http://localhost:5000/api/v2/search/rank', headers=headers, data=data)
        content=json.loads(response.content)
        candidates=content["final_score"]
        exp_glob = content["global_experience"]
        profils = content["Profile"]
        languages = content["Language"]
        
    # Demande d'emploi temps plein
        if emploi=='Temps plein':
            candidate_info = candidates_infos
            for i, c in enumerate(candidates):
                try:
                    res = {}
                    id=i+1
                    name=c['name'][8:]
                    score='{} %'.format(c["score"])
                    mail=make_mail(name)
                    res['glob_exp'] =  int(exp_glob[c['name']])
                    res["profil"] = profils[c['name']]
                    res["language"] = languages[c['name']]
                    firstname= name.lower().split(' ')[0:-1]
                    res['firstname']=''
                    for j in firstname:
                        res['firstname'] = (res['firstname']+' '+j).strip(' ')
                    res['lastname'] = name.lower().split(' ')[-1]
                    df_recomm.append(res)

                    #dataframe des résultats du moteur de recherche
                    df_result = pd.DataFrame(df_recomm)
                    # Concatener résultats moteur de recherche et résultats de requete base de données mysql
                    df_glob = pd.merge(candidate_info, df_result, on = ['firstname', 'lastname'])

                    
                    result = axe_2_temps_plein(df_glob,dispo,mail, debut_projet,score, i+1)
                
                    recomm.append(result)
                except:
                    pass
        
     # Demande d'emploi temps partiel
        if emploi=='Temps partiel':
            candidate_info = candidates_infos_1
            for i, c in enumerate(candidates):
                try:
                    res = {}
                    id=i+1
                    name=c['name'][8:]
                    score='{} %'.format(c["score"])
                    mail=make_mail(name)
                    res['glob_exp'] =  int(exp_glob[c['name']])
                    res["profil"] = profils[c['name']]
                    res["language"] = languages[c['name']]
                    firstname= name.lower().split(' ')[0:-1]
                    res['firstname']=''
                    for j in firstname:
                        res['firstname'] = (res['firstname']+' '+j).strip(' ')
                    res['lastname'] = name.lower().split(' ')[-1]
                    df_recomm.append(res)

                    #dataframe des résultats du moteur de recherche
                    df_result = pd.DataFrame(df_recomm)
                    # Concatener résultats moteur de recherche et résultats de requete base de données mysql
                    df_glob = pd.merge(candidate_info, df_result, on = ['firstname', 'lastname'])

                    
                    result = axe_2_temps_partiel(df_glob,dispo,mail, debut_projet,score, i+1)
                
                    recomm.append(result)
                except:
                    pass
    return jsonify(recomm)





@app.route("/api/v1/file/",methods=["POST"])
def download():
    zipError ={"status":500,"message":"an error occured while trying to zip files! Please retry"}
    req = request.get_json(force=True)
    try:
        docs = req["docs"]
        res = downloadCV(docs)
        if res != -1:
            try:
               return jsonify({"status":200,"message":"File(s) zipped"})
            except FileNotFoundError:
                abort(404)
        else:
            return jsonify(zipError)
    except:
        return jsonify(zipError)

#@app.route("/api/v1/file/",methods=["GET"])
#def getFiles():
     #return send_from_directory(BASE_PATH, filename="output.zip", as_attachment=True)

@app.route("/api/v1/file/",methods=["GET"])
def getFiles():
     #return jsonify("hello")
     return send_file(filename_or_fp="output.zip", as_attachment=True)


app.run(host="0.0.0.0",threaded=False,port='5001', debug=True)
