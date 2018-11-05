import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor 

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)

@app.route('/donate/', methods=['GET', 'POST'])
def donate():

    if request.method == 'GET':
        return render_template('create.jinja2')

    if request.method == 'POST':
        try:
            donor = Donor.select().where(Donor.name == request.form['name']).get()
        except Donor.DoesNotExist:
            donor = None

        if donor:
            donation = Donation(donor=donor, value=request.form['donation'])
            donation.save()
            return redirect(url_for('home'))
        else:
            return render_template('create.jinja2', error='Donor not found in database.')
    else:
        return render_template('create.jinja2')
    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

