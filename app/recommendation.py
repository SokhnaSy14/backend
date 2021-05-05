import re
from datetime import date
import pandas as pd


#
ecore_file=[]
for line in open("C:\\Users\\a800161\\Downloads\\recommendation_system\\model.ecore"):
    line=line.strip().strip('\n')
    line=re.sub(r'[<>?]','',line)
    line=line.split()
    ecore_file.append(line)
tables=[]
tables_index=[]
for i, line in enumerate(ecore_file):
    if 'eClassifiers' in line :
        for word in line:
            if word.startswith('name='):
                tables.append(word.strip('name=').strip('"').lower())
        tables_index.append(i)  
ecore_file
tables_index 
tables
len(tables) 


tables_attributs=[]
type_att=[]
for i,j  in zip(tables_index,tables):
    tab={}
    tab_att=[]
    typ_att=[]
    for line in ecore_file[i:]:
        if 'eStructuralFeatures' in line and 'xsi:type="ecore:EAttribute"' in line :
            for word in line:
                w=''
                typ=''
                if word.startswith('name='):
                    w=word.strip('name=').strip('"')
                    tab_att.append(w)
                if word.startswith('http:'):
                    typ=word.strip('').strip('/').split('/')[-1].strip('E').strip('"')
                    typ_att.append(typ)
        tab[j]=tab_att   
        if '/eClassifiers' in line:
            break
    tables_attributs.append(tab)
    type_att.append(typ_att)
tables_attributs



def type_conversion(liste):
    liste=[word.replace('Long','BIGINT') for word in liste]
    liste=[word.replace('String','VARCHAR(255)') for word in liste]
    liste=[word.replace('Date','DATE') for word in liste]
    liste=[word.replace('Int','INT') for word in liste]
    return liste 

for i, liste in enumerate(type_att):
    type_att[i]=type_conversion(liste)
type_att


tables # tables names
type_att # attributs types
tables_attributs # each table and its attributs

create_tables=[]
ids=['id_sp','id_sc','id_sd','id_loc','id_contact']
for i in range(len(tables)):
    attributs=''
    att=list(tables_attributs[i].values())[0]
    for j, k in zip(att,type_att[i]):
        attributs=attributs+' '+j+' '+k+','
        attributs=attributs.strip(' ')
    for w in att:
        if 'id_' in w and w[3:] in tables and w[3:]!=tables[i]:
            attributs=attributs+' '+'FOREIGN KEY ({}) REFERENCES {}({})'.format(w,w[3:],w)+','
        if 'id_' in w  and w[3:]==tables[i]:
            attributs=attributs+' '+'PRIMARY KEY ({})'.format(w)+','
            
        if w=='id_sp' and tables[i]=='subpractice':
            attributs=attributs+' '+'PRIMARY KEY ({})'.format(w)+','
        if w=='id_sp' and tables[i]!='subpractice':
            attributs=attributs+' '+'FOREIGN KEY ({}) REFERENCES subpractice({})'.format(w,w)+','
            
        if w=='id_sc' and tables[i]=='statutcandidat':
            attributs=attributs+' '+'PRIMARY KEY ({})'.format(w)+','
        if w=='id_sc' and tables[i]!='statutcandidat':
            attributs=attributs+' '+'FOREIGN KEY ({}) REFERENCES statutcandidat({})'.format(w,w)+','
        
        if w=='id_sd' and tables[i]=='statutdemande':
            attributs=attributs+' '+'PRIMARY KEY ({})'.format(w)+','
        if w=='id_sd' and tables[i]!='statutdemande':
            attributs=attributs+' '+'FOREIGN KEY ({}) REFERENCES statutdemande({})'.format(w,w)+','
            
        if w=='id_loc' and tables[i]=='localisation':
            attributs=attributs+' '+'PRIMARY KEY ({})'.format(w)+','
        if w=='id_loc' and tables[i]!='localisation':
            attributs=attributs+' '+'FOREIGN KEY ({}) REFERENCES localisation({})'.format(w,w)+','
        
        if w=='id_contact' and tables[i]=='contactclient':
            attributs=attributs+' '+'PRIMARY KEY ({})'.format(w)+','
        if w=='id_contact' and tables[i]!='contactclient':
            attributs=attributs+' '+'FOREIGN KEY ({}) REFERENCES contactclient({})'.format(w,w)+','
        
        if w=='id_procedure' and tables[i]=='proceduremission':
            attributs=attributs+' '+'PRIMARY KEY ({})'.format(w)+','
        if w=='id_procedure' and tables[i]!='proceduremission':
            attributs=attributs+' '+'FOREIGN KEY ({}) REFERENCES proceduremission({})'.format(w,w)+','
        
        if w=='id_prolongement' and tables[i]=='prolongementmission':
            attributs=attributs+' '+'PRIMARY KEY ({})'.format(w)+','
        if w=='id_prolongement' and tables[i]!='prolongementmission':
            attributs=attributs+' '+'FOREIGN KEY ({}) REFERENCES prolongementmission({})'.format(w,w)+','
            
    create_tables.append(attributs)
    

for i,j  in enumerate(create_tables):
    create_tables[i]='CREATE TABLE {}({})'.format(tables[i], j.strip(','))
create_tables
    


# ### Create tables of atos_db

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Ahm@ddaba1417",
  database="atos_db"
 # autocommit=True
)

cur= mydb.cursor()
for exp in create_tables:
    try:
        cur.execute(exp)
    except:
        continue
            
def make_mail(name):
    firstname=''
    lastname=''
    mail=''
    name=name.lower().split(' ')
    if len(name)==2:
        firstname=name[0]
        lastname=name[1]
        mail=name[0]+'.'+name[1]+'@atos.net'
        
        
    else:
        for j in name[0:-1]:
            firstname=firstname+' '+j
            mail=mail+j+'-'
        mail=mail.strip('-')+'.'+name[-1]+'@atos.net'
        lastname=lastname+name[-1]
    return mail
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






# Dataframe CV + batabase

import requests
import json
headers = {'Content-Type': 'text/plain',}
data = '{"querySearch":"java"}'
response = requests.post('http://localhost:5000/api/v2/search/rank', headers=headers, data=data)
content=json.loads(response.content)
candidates=content["final_score"]
exp_glob = content["global_experience"]
profils = content["Profile"]
languages = content["Language"]

df_recomm = []
#inf = candidates_infos[(candidates_infos['firstname']=='f') & (candidates_infos['lastname']=='l') ]
for i, c in enumerate(candidates):
    res = {}
    id=i+1
    name=c['name'][8:]
    score='{} %'.format(c["score"])
    
    #res = axe_2(dispo,mail, debut_projet,score, id)
    res['glob_exp'] =  int(exp_glob[c['name']])
    res["profil"] = profils[c['name']]
    res["language"] = languages[c['name']]
    #res['name'] = name.lower()
    res['firstname']= name.lower().split(' ')[0:-1][0]
    res['lastname'] = name.lower().split(' ')[-1]
    df_recomm.append(res)
df_result = pd.DataFrame(df_recomm)
df_glob = pd.merge(candidates_infos, df_result, on = ['firstname', 'lastname'])

# ### Recommendation function

def axe_2_temps_plein(df_glob,alpha, mail,debut_projet,score, id):
    import datetime
    firstname=list(df_glob[df_glob['ad_mail']==mail]['firstname'])[0]
    lastname=list(df_glob[df_glob['ad_mail']==mail]['lastname'])[0]
    fullname='CV ATOS '+firstname[0].upper()+firstname[1:]+' '+lastname.upper()
    #statut=list(df_glob[df_glob['ad_mail']==mail]['statut_candidat'])
    fin_mission=df_glob[df_glob['ad_mail']==mail]['fin_mission']
    fin_prolongement=df_glob[df_glob['ad_mail']==mail]['fin_prolongement']
    localisation=df_glob[df_glob['ad_mail']==mail]['localisation']
    profil=df_glob[df_glob['ad_mail']==mail]['profil']
    today = date.today()
    max_fin_mission = (df_glob[df_glob['ad_mail']==mail]['fin_mission']).max()
    max_fin_prolongement = (df_glob[df_glob['ad_mail']==mail]['fin_prolongement']).max()
   # max_fin_prolongement = df_glob[df_glob['ad_mail']==mail][['fin_mission','fin_prolongement' ]].max(axis='columns').iloc[1]
#     last_mission = list((df_glob[df_glob['ad_mail']==mail]['fin_mission']).sort_values())[-1]
#     last_prolongement = list((df_glob[df_glob['ad_mail']==mail]['fin_prolongement']).sort_values())[-1]
    index_max_fin_mission = df_glob[(df_glob['fin_mission']==max_fin_mission) & (df_glob['ad_mail']==mail) ]['localisation'].index
    index_max_fin_prolongement = df_glob[(df_glob['fin_prolongement']==max_fin_prolongement) & (df_glob['ad_mail']==mail) ]['localisation'].index

    # Pas de prolongement de mission
    if max_fin_prolongement== -1:
        dif=debut_projet-max_fin_mission
        if dif>=datetime.timedelta(weeks=0):
            if max_fin_mission > today:
                return {'ID': id, 'Fullname':fullname, 'ad_mail':mail, 'Statut':'Disponible', 'Score':score, 'Job_type': 'Temps plein', 'Dispo': str(max_fin_mission), 'commentaire': '{}  en cours de mission  à  {} '.format(profil[index_max_fin_mission].iloc[0],localisation[index_max_fin_mission].iloc[0]) }
            else:
                return {'ID': id, 'Fullname':fullname, 'ad_mail':mail, 'Statut':'Disponible', 'Score':score, 'Job_type': 'Temps plein', 'Dispo': str(max_fin_mission), 'commentaire': '{}  était en mission  à  {} '.format(profil[index_max_fin_mission].iloc[0],localisation[index_max_fin_mission].iloc[0]) }
                
        elif dif<=datetime.timedelta(weeks=0) and abs(dif)<=datetime.timedelta(weeks=alpha):
            return {'ID': id, 'Fullname':fullname, 'ad_mail':mail, 'Statut':'Bientôt disponible'  , 'Score':score, 'Job_type': 'Temps plein', 'Dispo': str(max_fin_mission), 'commentaire': '{}  en cours de mission à  {} qui sera terminée {} aprés le début du projet demandé '.format(profil[index_max_fin_mission].iloc[0],localisation[index_max_fin_mission].iloc[0],abs(dif)) .replace('days', 'jours').replace('day', 'jour') }
        else:
            return {'ID': id, 'Fullname':fullname, 'ad_mail':mail, 'Statut':'Indisponible', 'Score':score, 'Job_type': 'Temps plein', 'Dispo': str(max_fin_mission), 'commentaire': '{}  mission en cours à  {} '.format(profil[index_max_fin_mission].iloc[0],localisation[index_max_fin_mission].iloc[0])}
    
    # Avec prolongement de mission
    else: 
        
        if max_fin_mission > max_fin_prolongement:
            dif=debut_projet-max_fin_mission
            if dif>=datetime.timedelta(weeks=0):
                if max_fin_mission > today:
                    return {'ID': id, 'Fullname':fullname, 'ad_mail':mail, 'Statut':'Disponible', 'Score':score, 'Job_type': 'Temps plein', 'Dispo': str(max_fin_mission), 'commentaire': '{}  en cours de mission  à  {} '.format(profil[index_max_fin_mission].iloc[0],localisation[index_max_fin_mission].iloc[0]) }
                else:
                    return {'ID': id, 'Fullname':fullname, 'ad_mail':mail, 'Statut':'Disponible', 'Score':score, 'Job_type': 'Temps plein', 'Dispo': str(max_fin_mission), 'commentaire': '{}  était en mission  à  {} '.format(profil[index_max_fin_mission].iloc[0],localisation[index_max_fin_mission].iloc[0]) }
                
            elif dif<=datetime.timedelta(weeks=0) and abs(dif)<=datetime.timedelta(weeks=alpha):
                return {'ID': id, 'Fullname':fullname, 'ad_mail':mail, 'Statut':'Bientôt disponible'  , 'Score':score, 'Job_type': 'Temps plein', 'Dispo': str(max_fin_mission), 'commentaire': '{}  en cours de mission à  {} qui sera terminée {} aprés le début du projet demandé '.format(profil[index_max_fin_mission].iloc[0],localisation[index_max_fin_mission].iloc[0],abs(dif)) .replace('days', 'jours').replace('day', 'jour') }
            else:
                return {'ID': id, 'Fullname':fullname, 'ad_mail':mail, 'Statut':'Indisponible', 'Score':score, 'Job_type': 'Temps plein', 'Dispo': str(max_fin_mission), 'commentaire': '{}  mission en cours à  {} '.format(profil[index_max_fin_mission].iloc[0],localisation[index_max_fin_mission].iloc[0])}
    
        
        
        else:
            dif=debut_projet-max_fin_prolongement
            if dif>=datetime.timedelta(weeks=0):
                if max_fin_prolongement > today:
                    return {'ID': id, 'Fullname':fullname, 'ad_mail':mail, 'Statut':'Disponible', 'Score':score, 'Job_type': 'Temps plein', 'Dispo': str(max_fin_prolongement), 'commentaire': '{}  en cours de mission  à  {} '.format(profil[index_max_fin_prolongement].iloc[0],localisation[index_max_fin_prolongement].iloc[0]) }
                else:
                    return {'ID': id, 'Fullname':fullname, 'ad_mail':mail, 'Statut':'Disponible', 'Score':score, 'Job_type': 'Temps plein', 'Dispo': str(max_fin_prolongement), 'commentaire': '{}  était en mission  à  {} '.format(profil[index_max_fin_prolongement].iloc[0],localisation[index_max_fin_prolongement].iloc[0]) }
                
            elif dif<=datetime.timedelta(weeks=0) and abs(dif)<=datetime.timedelta(weeks=alpha):
                return {'ID': id, 'Fullname':fullname, 'ad_mail':mail, 'Statut':'Bientôt disponible'  , 'Score':score, 'Job_type': 'Temps plein', 'Dispo':str(max_fin_prolongement), 'commentaire': '{}  en cours de mission à  {} qui sera terminée {} aprés le début du projet demandé '.format(profil[index_max_fin_prolongement].iloc[0],localisation[index_max_fin_prolongement].iloc[0],abs(dif)) .replace('days', 'jours').replace('day', 'jour') }
            else:
                return  {'ID': id, 'Fullname':fullname, 'ad_mail':mail, 'Statut':'Indisponible', 'Score':score, 'Job_type': 'Temps plein', 'Dispo': str(max_fin_prolongement), 'commentaire': '{}  mission en cours à  {} '.format(profil[index_max_fin_prolongement].iloc[0],localisation[index_max_fin_prolongement].iloc[0])}
    
            
def axe_2_temps_partiel(df_glob,alpha, mail,debut_projet,score, id):
    import datetime
    firstname=list(df_glob[df_glob['ad_mail']==mail]['firstname'])[0]
    lastname=list(df_glob[df_glob['ad_mail']==mail]['lastname'])[0]
    fullname='CV ATOS '+firstname[0].upper()+firstname[1:]+' '+lastname.upper()
    #statut=list(df_glob[df_glob['ad_mail']==mail]['statut_candidat'])
    fin_mission=df_glob[df_glob['ad_mail']==mail]['fin_mission']
    fin_prolongement=df_glob[df_glob['ad_mail']==mail]['fin_prolongement']
    localisation=df_glob[df_glob['ad_mail']==mail]['localisation']
    profil=df_glob[df_glob['ad_mail']==mail]['profil']
    today = date.today()
    max_fin_mission = (df_glob[df_glob['ad_mail']==mail]['fin_mission']).max()
    max_fin_prolongement = (df_glob[df_glob['ad_mail']==mail]['fin_prolongement']).max()
   # max_fin_prolongement = df_glob[df_glob['ad_mail']==mail][['fin_mission','fin_prolongement' ]].max(axis='columns').iloc[1]
#     last_mission = list((df_glob[df_glob['ad_mail']==mail]['fin_mission']).sort_values())[-1]
#     last_prolongement = list((df_glob[df_glob['ad_mail']==mail]['fin_prolongement']).sort_values())[-1]
    index_max_fin_mission = df_glob[(df_glob['fin_mission']==max_fin_mission) & (df_glob['ad_mail']==mail) ]['localisation'].index
    index_max_fin_prolongement = df_glob[(df_glob['fin_prolongement']==max_fin_prolongement) & (df_glob['ad_mail']==mail) ]['localisation'].index

    # Pas de prolongement de mission
    if max_fin_prolongement== -1:
        dif=debut_projet-max_fin_mission
        if dif>=datetime.timedelta(weeks=0):
            if max_fin_mission > today:
                return {'ID': id, 'Fullname':fullname, 'ad_mail':mail, 'Statut':'Disponible', 'Score':score, 'Job_type': 'Temps partiel', 'Dispo': str(max_fin_mission), 'commentaire': '{}  en cours de mission  à  {} '.format(profil[index_max_fin_mission].iloc[0],localisation[index_max_fin_mission].iloc[0]) }
            else:
                return {'ID': id, 'Fullname':fullname, 'ad_mail':mail, 'Statut':'Disponible', 'Score':score, 'Job_type': 'Temps partiel', 'Dispo': str(max_fin_mission), 'commentaire': '{}  était en mission  à  {} '.format(profil[index_max_fin_mission].iloc[0],localisation[index_max_fin_mission].iloc[0]) }
                
        elif dif<=datetime.timedelta(weeks=0) and abs(dif)<=datetime.timedelta(weeks=alpha):
            return {'ID': id, 'Fullname':fullname, 'ad_mail':mail, 'Statut':'Bientôt disponible'  , 'Score':score, 'Job_type': 'Temps partiel', 'Dispo': str(max_fin_mission), 'commentaire': '{}  en cours de mission à  {} qui sera terminée {} aprés le début du projet demandé '.format(profil[index_max_fin_mission].iloc[0],localisation[index_max_fin_mission].iloc[0],abs(dif)) .replace('days', 'jours').replace('day', 'jour') }
        else:
            return {'ID': id, 'Fullname':fullname, 'ad_mail':mail, 'Statut':'Indisponible', 'Score':score, 'Job_type': 'Temps partiel', 'Dispo': str(max_fin_mission), 'commentaire': '{}  mission en cours à  {} '.format(profil[index_max_fin_mission].iloc[0],localisation[index_max_fin_mission].iloc[0])}
    
    # Avec prolongement de mission
    else: 
        
        if max_fin_mission > max_fin_prolongement:
            dif=debut_projet-max_fin_mission
            if dif>=datetime.timedelta(weeks=0):
                if max_fin_mission > today:
                    return {'ID': id, 'Fullname':fullname, 'ad_mail':mail, 'Statut':'Disponible', 'Score':score, 'Job_type': 'Temps partiel', 'Dispo': str(max_fin_mission), 'commentaire': '{}  en cours de mission  à  {} '.format(profil[index_max_fin_mission].iloc[0],localisation[index_max_fin_mission].iloc[0]) }
                else:
                    return {'ID': id, 'Fullname':fullname, 'ad_mail':mail, 'Statut':'Disponible', 'Score':score, 'Job_type': 'Temps partiel', 'Dispo': str(max_fin_mission), 'commentaire': '{}  était en mission  à  {} '.format(profil[index_max_fin_mission].iloc[0],localisation[index_max_fin_mission].iloc[0]) }
                
            elif dif<=datetime.timedelta(weeks=0) and abs(dif)<=datetime.timedelta(weeks=alpha):
                return {'ID': id, 'Fullname':fullname, 'ad_mail':mail, 'Statut':'Bientôt disponible'  , 'Score':score, 'Job_type': 'Temps partiel', 'Dispo': str(max_fin_mission), 'commentaire': '{}  en cours de mission à  {} qui sera terminée {} aprés le début du projet demandé '.format(profil[index_max_fin_mission].iloc[0],localisation[index_max_fin_mission].iloc[0],abs(dif)) .replace('days', 'jours').replace('day', 'jour') }
            else:
                return {'ID': id, 'Fullname':fullname, 'ad_mail':mail, 'Statut':'Indisponible', 'Score':score, 'Job_type': 'Temps partiel', 'Dispo': str(max_fin_mission), 'commentaire': '{}  mission en cours à  {} '.format(profil[index_max_fin_mission].iloc[0],localisation[index_max_fin_mission].iloc[0])}
    
        
        
        else:
            dif=debut_projet-max_fin_prolongement
            if dif>=datetime.timedelta(weeks=0):
                if max_fin_prolongement > today:
                    return {'ID': id, 'Fullname':fullname, 'ad_mail':mail, 'Statut':'Disponible', 'Score':score, 'Job_type': 'Temps partiel', 'Dispo': str(max_fin_prolongement), 'commentaire': '{}  en cours de mission  à  {} '.format(profil[index_max_fin_prolongement].iloc[0],localisation[index_max_fin_prolongement].iloc[0]) }
                else:
                    return {'ID': id, 'Fullname':fullname, 'ad_mail':mail, 'Statut':'Disponible', 'Score':score, 'Job_type': 'Temps partiel', 'Dispo': str(max_fin_prolongement), 'commentaire': '{}  était en mission  à  {} '.format(profil[index_max_fin_prolongement].iloc[0],localisation[index_max_fin_prolongement].iloc[0]) }
                
            elif dif<=datetime.timedelta(weeks=0) and abs(dif)<=datetime.timedelta(weeks=alpha):
                return {'ID': id, 'Fullname':fullname, 'ad_mail':mail, 'Statut':'Bientôt disponible'  , 'Score':score, 'Job_type': 'Temps partiel', 'Dispo':str(max_fin_prolongement), 'commentaire': '{}  en cours de mission à  {} qui sera terminée {} aprés le début du projet demandé '.format(profil[index_max_fin_prolongement].iloc[0],localisation[index_max_fin_prolongement].iloc[0],abs(dif)) .replace('days', 'jours').replace('day', 'jour') }
            else:
                return  {'ID': id, 'Fullname':fullname, 'ad_mail':mail, 'Statut':'Indisponible', 'Score':score, 'Job_type': 'Temps partiel', 'Dispo': str(max_fin_prolongement), 'commentaire': '{}  mission en cours à  {} '.format(profil[index_max_fin_prolongement].iloc[0],localisation[index_max_fin_prolongement].iloc[0])}

import os
import glob
import ntpath
from zipfile import ZipFile
from os.path import basename

def CV_to_download(docs):
    BASE_PATH = os.path.abspath(os.path.join(__file__, "../.."))
    base_dir = BASE_PATH+"/data/cv/*.*" 
    files = sorted(glob.glob(base_dir))
    #output_dir = "output.zip"
    path_names=[]
    Docs=[]
    for doc in docs:
        Docs.append(doc.lower())

    for file_name in files:
        name = ntpath.basename(file_name).split(".")[0].lower()
        if name in Docs:
            path_names.append(file_name)
    if len(path_names)!=0:
        return path_names
    else :
        print('No  files found ')
        return -1


def downloadCV(docs):
    BASE_PATH = os.path.abspath(os.path.join(__file__, "../.."))
    base_dir = BASE_PATH+"/data/cv/*.*"  
    files = sorted(glob.glob(base_dir))
    output_dir = "output.zip"
    names=[]
    Docs=[]
    for doc in docs:
        
        Docs.append(doc.lower())
    # printing the list of all files to be zipped 
    
    try:
        print('Following files will be zipped:') 
        with ZipFile('output.zip','w') as zip: 
            # writing each file one by one            
            for file_name in files:
                name = ntpath.basename(file_name).split(".")[0].lower()
                if name in Docs:
                    print(name) 
                    zip.write(file_name,basename(file_name))
        print('All files zipped successfully!')
        return 1
    except:
        print("An error occured")
        return -1
