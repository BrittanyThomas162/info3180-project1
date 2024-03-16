"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""

import os
from app import app, db
from flask import render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from app.models import Property
from app.forms import NewPropertyForm
from operator import length_hint


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")


@app.route('/properties/create', methods=['POST', 'GET'])
def create():
    form = NewPropertyForm()
       
    if form.validate_on_submit():

        title = form.title.data
        numBed = form.numBed.data
        numBath = form.numBath.data
        location = form.location.data
        price = form.price.data
        prop_type = form.prop_type.data
        description =  form.description.data

        photo = form.photo.data
        filename=secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        property = Property(title=title, numBed=numBed, numBath=numBath, location=location, price=price, prop_type=prop_type, description=description, photo=filename)
        
        db.session.add(property)
        db. session.commit()

        flash('New property successfully added','success')
        return redirect(url_for('displayProperty'))
        
    flash_errors(form)
    return render_template('createProperty.html', form=form)
    

@app.route('/properties')
def displayProperty():
    images = get_uploaded_images()
    properties= Property.query.all()

    if not properties:
        flash('No properties available.', 'warning')  

    return render_template('listProperties.html', images=images, properties=properties)

def get_uploaded_images():
    rootdir = app.config['UPLOAD_FOLDER']
    photo_lst = []
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if file.endswith(('.jpg', '.jpeg', '.png')):
                photo_lst.append(file)
    return photo_lst

@app.route('/uploads/<filename>')
def get_image(filename):
    rootdir = app.config['UPLOAD_FOLDER']
    return send_from_directory(os.path.join(os.getcwd(), rootdir), filename)    


@app.route('/properties/<propertyid>')
def viewProperty(propertyid):
    property_info = Property.query.get_or_404(propertyid)
    return render_template('indProperty.html', property_info=property_info)


###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
