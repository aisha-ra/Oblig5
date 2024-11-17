# kg.py
from flask import Flask, url_for, render_template, request, redirect, session, send_file
from kgmodel import Foresatt, Barn, Soknad, Barnehage
from kgcontroller import (
    insert_soknad, commit_all,
    select_alle_barnehager, select_alle_soknader,
    select_barnehage_instans, form_to_object_soknad,
    get_all_data
)
import matplotlib.pyplot as plt
import io

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/barnehager')
def barnehager():
    information = select_alle_barnehager()
    return render_template('barnehager.html', data=information)


@app.route('/behandle', methods=['GET', 'POST'])
def behandle():
    if request.method == 'POST':
        sd = request.form
        print(f"Form submission received: {sd}")  # Debugging
        soknad_obj = form_to_object_soknad(sd)
        insert_soknad(soknad_obj)
        session['information'] = sd
        return redirect(url_for('svar'))
    else:
        return render_template('soknad.html')


@app.route('/svar')
def svar():
    information = session.get('information', {})
    if not information:
        return redirect(url_for('index'))
    
    priorities = information.get('liste_over_barnehager_prioritert_5', '')
    barnehage_liste = []
    message = "AVSLAG: Ingen ledige plasser på de valgte barnehager."
    
    if priorities:
        kgpr = priorities.split(',')
        for kgid in kgpr:
            try:
                kgid_int = int(kgid)
                barnehage_instans = select_barnehage_instans(kgid_int)
                if barnehage_instans and barnehage_instans.barnehage_ledige_plasser > 0:
                    barnehage_liste.append(barnehage_instans)
                    message = "Tilbud (høyest prioritert øverst):"
            except ValueError:
                print(f"Invalid kindergarten ID: {kgid}")  # Debugging
                
    return render_template('svar.html', data=information, kglist=barnehage_liste, message=message)


@app.route('/soknader')
def soknader():
    all_soknader = select_alle_soknader()
    return render_template('soknader.html', soknader=all_soknader)


@app.route('/commit')
def commit():
    data = get_all_data()
    commit_all()
    print(f"Data committed to Excel: {data}")  # Debugging
    return render_template('commit.html', **data)


@app.route('/statistikk')
def statistikk():
    ages = [1, 2]
    percentages = [30, 45]

    plt.figure(figsize=(8, 4))
    plt.bar(ages, percentages, color='blue')
    plt.xlabel('Age')
    plt.ylabel('Percentage of Children in Barnehage')
    plt.title('Barnehage Attendance Statistics for Ages 1-2')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return send_file(img, mimetype='image/png')
