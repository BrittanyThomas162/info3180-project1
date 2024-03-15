"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""

import os
from app import app, db
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app.models import Property
from app.forms import NewPropertyForm


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

'''The add new property form must be created using Flask-WTF and contain
the following fields:
1. Text fields for title, number of bedrooms, number of
bathrooms, location and price.
2. Select (option) field for type (whether House or Apartment)
3. Textarea field for a short description.
4. File upload field called photo which accepts the image of the
Property.

Upon submission, the form should make a POST request and validate the
user input to prevent bad data. A unique id should be generated (e.g. an
auto incrementing id field in your model) and also the filename of the
photo for the new property should be saved in the database. All of this
input must be stored in a PostgreSQL database.'''
'''1. "/properties/create" For displaying the form to add a new
property. (See Figure 1)'''
@app.route('/properties/create', methods=['POST', 'GET'])
def create():
    pass
    form = NewPropertyForm()
    
    '''if request.method == 'GET':
        return render_template("createProperty.html",form=form)
  
    if request.method == 'POST' and form.validate_on_submit():
        
        #photo =  myform.photo.data  
        #filename = secure_filename(photo.filename)  '''
       
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
    else:
        flash('Property was not added','danger')
        
    flash_errors(form)
    return render_template('createProperty.html', form=form)
    

'''2. "/properties" For displaying a list of all properties in the
database. (See Figure 2)'''
@app.route('/properties')
def displayProperty():
    pass


'''
3. "/properties/<propertyid>" For viewing an individual property
by the specific property id.'''
@app.route('/properties/<propertyid>')
def viewProperty():
    pass


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
