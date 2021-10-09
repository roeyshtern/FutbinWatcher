# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound

@blueprint.route('/index')
@login_required
def index():

    return render_template('index.html', segment='index')

@blueprint.route('/add-player.html', methods=['POST'])
def add_player():
    if 'add_player' in request.form:
        
        # read form data
        player_id = request.form['player_id']
        min_price = request.form['min_price']
        max_price = request.form['max_price']

        # Locate user
        #user = User.query.filter_by(username=username).first()
        
        print("Entered: {0} - min - {1} max - {2}".format(player_id, min_price, max_price))

        # Something (user or pass) is not ok
        return render_template( 'index.html', segment='index')

    else:
        return render_template('page-500.html'), 500

@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith( '.html' ):
            template += '.html'

        # Detect the current page
        segment = get_segment( request )

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template( template, segment=segment )

    except TemplateNotFound:
        return render_template('page-404.html'), 404
    
    except:
        return render_template('page-500.html'), 500

# Helper - Extract current page name from request 
def get_segment( request ): 

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment    

    except:
        return None  
