# kg.py
from flask import Flask, url_for, render_template, request, redirect, session
from kgmodel import Foresatt, Barn, Soknad, Barnehage
from kgcontroller import (
    insert_soknad, commit_all,
    select_alle_barnehager, select_alle_soknader,
    select_barnehage_instans, form_to_object_soknad,
    get_all_data
    )

import dbexcel as db
import altair as alt

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/barnehager')
def barnehager():
    try:
        # Retrieve and render data for barnehager
        information = select_alle_barnehager()
        return render_template('barnehager.html', data=information)
    except KeyError as e:
        return render_template('error.html', message=f"Missing column in barnehage data: {e}")


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
            except KeyError as e:
                return render_template('error.html', message=f"Missing column in barnehage data: {e}")

    return render_template('svar.html', data=information, kglist=barnehage_liste, message=message)


@app.route('/soknader')
def soknader():
    try:
        # Debugging: Log the entire database content before processing
        print("Current state of db.soknad:")
        print(db.soknad)

        # Retrieve and render data for soknader
        all_soknader = select_alle_soknader()
        print("Data extracted for soknader:", all_soknader)  # Log processed data for debugging
        return render_template('soknader.html', soknader=all_soknader)
    except Exception as e:
        return render_template('error.html', message=f"Error processing soknader: {e}")


@app.route('/commit')
def commit():
    try:
        # Commit all data and display confirmation
        data = get_all_data()
        commit_all()
        print(f"Data committed to Excel: {data}")  # Debugging
        return render_template('commit.html', **data)
    except Exception as e:
        return render_template('error.html', message=f"Error committing data: {e}")



@app.route('/statistikk', methods=['GET'])
def statistikk():
    valgt_kommune = "Kristiansand"
    chart = None

    try:
        # Log the entire database's current state
        print("Current db.soknad state:")
        print(db.soknad)

        # Check if 'kommune' column exists
        if 'kommune' not in db.soknad.columns:
            print("Error: 'kommune' column is missing from db.soknad")
            return render_template('statistikk.html', message="Manglende kommune-kolonne i søknadsdata.")

        # Log filtered data
        kommune_data = db.soknad[db.soknad['kommune'] == valgt_kommune]
        print("Filtered data for Kristiansand:")
        print(kommune_data)

        if kommune_data.empty:
            return render_template('statistikk.html', message="Ingen data for valgt kommune.")

        # Log the columns available
        print("Columns in filtered data:")
        print(kommune_data.columns)

        # Validate required year columns
        year_columns = ['y15', 'y16', 'y17', 'y18', 'y19', 'y20', 'y21', 'y22', 'y23']
        if not all(col in kommune_data.columns for col in year_columns):
            print("Missing required statistical columns.")
            return render_template('statistikk.html', message="Manglende nødvendige kolonner i data.")

        kommune_data_melted = kommune_data.melt(
            id_vars='kommune',
            value_vars=year_columns,
            var_name='År',
            value_name='Prosent'
        )
        kommune_data_melted['År'] = kommune_data_melted['År'].str.replace('y', '20')

        print("Melted data for visualization:")
        print(kommune_data_melted)

        # Generate Altair chart
        chart = alt.Chart(kommune_data_melted).mark_line(point=True).encode(
            x=alt.X('År:N', title='År'),
            y=alt.Y('Prosent:Q', title='Prosentandel'),
            tooltip=['År', 'Prosent']
        ).properties(
            title=f'Statistikk for {valgt_kommune}',
            width=800,
            height=400
        ).to_json()

    except Exception as e:
        print(f"Error generating statistics: {e}")
        return render_template('statistikk.html', message=f"Error generating statistics: {e}")

    return render_template('statistikk.html', chart=chart)


if __name__ == '__main__':
    app.run()
