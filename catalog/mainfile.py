from flask import Flask, render_template, url_for
from flask import request, redirect, flash, make_response, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, PenDrivesCompanyName, PenDriveName, PenDriveUser
from flask import session as login_pdsession_pduser
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import requests
import datetime
import httplib2
import json

engine = create_engine('sqlite:///pendrives.db',
                       connect_args={'check_same_thread': False}, echo=True)
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json',
                            'r').read())['web']['client_id']
applicationname = "PenDrives Store"

DBSession = sessionmaker(bind=engine)
session = DBSession()
# Create anti-forgery globalstate token
pendrives = session.query(PenDrivesCompanyName).all()


# login to the pendrives store
@app.route('/login')
def showUserLogin():

    globalstate = ''.join(random.choice(string.ascii_uppercase + string.digits)
                          for x in range(32))
    login_pdsession_pduser['globalstate'] = globalstate
    # "session globalstate is %s" % login_pdsession_pduser['globalstate']
    pendrives = session.query(PenDrivesCompanyName).all()
    pdcm = session.query(PenDriveName).all()
    return render_template('login.html',
                           STATE=globalstate, pendrives=pendrives, pdcm=pdcm)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate globalstate token is written here
    if request.args.get('globalstate') != login_pdsession_pduser[
                                         'globalstate']:
        reply = make_response(json.dumps(
                             'Invalid globalstate parameter.'), 401)
        reply.headers['Content-Type'] = 'application/json'
        return reply
    #  authorization code should be obtained
    code = request.data

    try:
        # Upgrading the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        reply = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        reply.headers['Content-Type'] = 'application/json'
        return reply

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        reply = make_response(json.dumps(result.get('error')), 500)
        reply.headers['Content-Type'] = 'application/json'
        return reply

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        reply = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        reply.headers['Content-Type'] = 'application/json'
        return reply

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        reply = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        reply.headers['Content-Type'] = 'application/json'
        return reply

    spa_apa_tok = login_pdsession_pduser.get('access_token')
    spa_pap_tik = login_pdsession_pduser.get('gplus_id')
    if spa_apa_tok is not None and gplus_id == spa_pap_tik:
        reply = make_response(json.dumps(
                             'Current user already connected.'), 200)
        reply.headers['Content-Type'] = 'application/json'
        return reply

    # Store the access token in the session for later use.
    login_pdsession_pduser['access_token'] = credentials.access_token
    login_pdsession_pduser['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_pdsession_pduser['username'] = data['name']
    login_pdsession_pduser['picture'] = data['picture']
    login_pdsession_pduser['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    pduser_id = getUserID(login_pdsession_pduser['email'])
    if not pduser_id:
        pduser_id = createUser(login_pdsession_pduser)
    login_pdsession_pduser['pduser_id'] = pduser_id

    output = ''
    output += '<h1>Welcome, '
    output += login_pdsession_pduser['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_pdsession_pduser['picture']
    output += ' " style = "width: 300px; height: 300px; border-radius: 150px;'
    '-webkit-border-radius: 150px; -moz-border-radius: 150px;"> '
    flash("you are currently logged in as %s" % login_pdsession_pduser
          ['username'])
    print ("done!")
    return output


# User Helper Functions
def createUser(login_pdsession_pduser):
    Users100 = PenDriveUser(pdusername=login_pdsession_pduser['username'],
                            email=login_pdsession_pduser['email'],
                            picture=login_pdsession_pduser['picture'])
    session.add(Users100)
    session.commit()
    user = session.query(PenDriveUser).filter_by(email=login_pdsession_pduser[
                                                'email']).one()
    return user.id


def getUserInfo(pduser_id):
    user = session.query(PenDriveUser).filter_by(id=pduser_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(PenDriveUser).filter_by(email=email).one()
        return user.id
    except Exception as error:
        print(error)
        return None

# DISCONNECT - Revoke user's token and reset their login_pdsession_pduser


@app.route('/')
@app.route('/home')
def home():
    '''home function'''
    pendrives = session.query(PenDrivesCompanyName).all()
    return render_template('myhome.html', pendrives=pendrives)


@app.route('/PenDriveStore')
def PenDriveStore():
    ''' PenDrive Category for admins'''
    try:
        if login_pdsession_pduser['username']:
            name = login_pdsession_pduser['username']
            pendrives = session.query(PenDrivesCompanyName).all()
            pdpdcc = session.query(PenDrivesCompanyName).all()
            pdcm = session.query(PenDriveName).all()
            return render_template('myhome.html', pendrives=pendrives,
                                   pdpdcc=pdpdcc, pdcm=pdcm, uname=name)
    except:
        return redirect(url_for('showUserLogin'))


@app.route('/PenDriveStore/<int:pdccid>/AllCompanys')
def showPds(pdccid):
    '''Showing pendrives based on PenDrive category'''
    pendrives = session.query(PenDrivesCompanyName).all()
    pdpdcc = session.query(PenDrivesCompanyName).filter_by(id=pdccid).one()
    pdcm = session.query(PenDriveName).filter_by(
                                       pendrivecompanyid=pdccid).all()
    try:
        if login_pdsession_pduser['username']:
            return render_template('showPds.html', pendrives=pendrives,
                                   pdpdcc=pdpdcc, pdcm=pdcm,
                                   uname=login_pdsession_pduser['username'])
    except:
        return render_template('showPds.html',
                               pendrives=pendrives, pdpdcc=pdpdcc, pdcm=pdcm)


@app.route('/PenDriveStore/insertPdCompany', methods=['POST', 'GET'])
def insertPdCompany():
    ''' Add New pendrives'''
    if request.method == 'POST':
        company = PenDrivesCompanyName(pdusername=request.form['pdusername'],
                                       pduser_id=login_pdsession_pduser[
                                                'pduser_id'])
        session.add(company)
        session.commit()
        return redirect(url_for('PenDriveStore'))
    else:
        return render_template('insertPdCompany.html', pendrives=pendrives)


@app.route('/PenDriveStore/<int:pdccid>/edit', methods=['POST', 'GET'])
def changepdgroup(pdccid):
    ''' Add New pendrives'''
    editedpds = session.query(PenDrivesCompanyName).filter_by(id=pdccid).one()
    creator = getUserInfo(editedpds.pduser_id)
    user = getUserInfo(login_pdsession_pduser['pduser_id'])
    ''' If logged in user != item owner redirect them'''
    '''if creator.id != login_pdsession_pduser['pduser_id']:
        flash("You cannot edit this PenDrive Category."
              "This is belongs to %s" % creator.pdusername)
        return redirect(url_for('PenDriveStore'))'''
    if request.method == "POST":
        if request.form['pdusername']:
            editedpds.pdusername = request.form['pdusername']
        session.add(editedpds)
        session.commit()
        flash("Pendrive Category Edited Successfully")
        return redirect(url_for('PenDriveStore'))
    else:
        '''pendrives is global variable we can them in entire application'''
        return render_template('changepdgroup.html',
                               pdbb=editedpds, pendrives=pendrives)


@app.route('/PenDriveStore/<int:pdccid>/delete', methods=['POST', 'GET'])
def removepdgroup(pdccid):
    '''Delete pendrive Category'''
    pdbb = session.query(PenDrivesCompanyName).filter_by(id=pdccid).one()
    creator = getUserInfo(pdbb.pduser_id)
    user = getUserInfo(login_pdsession_pduser['pduser_id'])
    ''' If logged in user != item owner redirect them'''
    '''if creator.id != login_pdsession_pduser['pduser_id']:
        flash("You cannot Delete this Pendrive Category."
              "This is belongs to %s" % creator.pdusername)
        return redirect(url_for('PenDriveStore'))'''
    if request.method == "POST":
        session.delete(pdbb)
        session.commit()
        flash("PenDrive Category Deleted Successfully")
        return redirect(url_for('PenDriveStore'))
    else:
        return render_template('removepdgroup.html',
                               pdbb=pdbb, pendrives=pendrives)

######
# Add New pendrive Name Details


@app.route('/PenDriveStore/addCompany/insertpddetails/<string:cppname>/add',
           methods=['GET', 'POST'])
def insertpddetails(cppname):
    pdpdcc = session.query(PenDrivesCompanyName).filter_by(
                                                 pdusername=cppname).one()
    # See if the logged in user is not the owner of pendrive
    creator = getUserInfo(pdpdcc.pduser_id)
    user = getUserInfo(login_pdsession_pduser['pduser_id'])
    # If logged in user != item owner redirect them
    '''if creator.id != login_pdsession_pduser['pduser_id']:
        flash("You can't add new Pendrive edition"
              "This is belongs to %s" % creator.pdusername)
        return redirect(url_for('showPds', pdccid=pdpdcc.id))'''
    if request.method == 'POST':
        pdusername = request.form['pdusername']
        drives_number = request.form['drives_number']
        item_capacity = request.form['item_capacity']
        drive_name = request.form['drive_name']
        item_color = request.form['item_color']
        transferspeed = request.form['transferspeed']
        item_cost = request.form['item_cost']
        warranty = request.form['warranty']
        pendrivedetails = PenDriveName(pdusername=pdusername,
                                       drives_number=drives_number,
                                       item_capacity=item_capacity,
                                       drive_name=drive_name,
                                       item_color=item_color,
                                       transferspeed=transferspeed,
                                       item_cost=item_cost,
                                       warranty=warranty,
                                       date=datetime.datetime.now(),
                                       pendrivecompanyid=pdpdcc.id,
                                       pduser_id=login_pdsession_pduser[
                                           'pduser_id'])
        session.add(pendrivedetails)
        session.commit()
        return redirect(url_for('showPds', pdccid=pdpdcc.id))
    else:
        return render_template('insertpddetails.html',
                               cppname=pdpdcc.pdusername, pendrives=pendrives)

######
# Edit Pendrive details


@app.route('/PenDriveStore/<int:pdccid>/<string:pdpdname>/edit',
           methods=['GET', 'POST'])
def editPenDrive(pdccid, pdpdname):
    pdbb = session.query(PenDrivesCompanyName).filter_by(id=pdccid).one()
    pendrivedetails = session.query(PenDriveName).filter_by(
                                                 pdusername=pdpdname).one()
    '''See if the logged in user is not the owner of pendrive'''
    creator = getUserInfo(pdbb.pduser_id)
    user = getUserInfo(login_pdsession_pduser['pduser_id'])
    # If logged in user != item owner redirect them
    '''if creator.id != login_pdsession_pduser['pduser_id']:
        flash("You can't edit this PENDRIVE edition"
              "This is belongs to %s" % creator.pdusername)
        return redirect(url_for('showPds', pdccid=pdbb.id))'''
    ''' POST methods'''
    if request.method == 'POST':
        pendrivedetails.pdusername = request.form['pdusername']
        pendrivedetails.drives_number = request.form['drives_number']
        pendrivedetails.item_capacity = request.form['item_capacity']
        pendrivedetails.drive_name = request.form['drive_name']
        pendrivedetails.item_color = request.form['item_color']
        pendrivedetails.transferspeed = request.form['transferspeed']
        pendrivedetails.item_cost = request.form['item_cost']
        pendrivedetails.warranty = request.form['warranty']
        pendrivedetails.date = datetime.datetime.now()
        session.add(pendrivedetails)
        session.commit()
        flash("pendrive Edited Successfully")
        return redirect(url_for('showPds', pdccid=pdccid))
    else:
        return render_template('editPenDrive.html',
                               pdccid=pdccid, pendrivedetails=pendrivedetails,
                               pendrives=pendrives)

#####
# Delte pendrive Edit


@app.route('/PenDriveStore/<int:pdccid>/<string:pdpdname>/delete',
           methods=['GET', 'POST'])
def deletePenDrive(pdccid, pdpdname):
    pdbb = session.query(PenDrivesCompanyName).filter_by(id=pdccid).one()
    pendrivedetails = session.query(PenDriveName).filter_by(
                                                  pdusername=pdpdname).one()
    # See if the logged in user is not the owner of pendrive
    creator = getUserInfo(pdbb.pduser_id)
    user = getUserInfo(login_pdsession_pduser['pduser_id'])
    # If logged in user != item owner redirect them
    '''if creator.id != login_pdsession_pduser['pduser_id']:
        flash("You can't delete this Pendrive edition"
              "This is belongs to %s" % creator.pdusername)
        return redirect(url_for('showPds', pdccid=pdbb.id))'''
    if request.method == "POST":
        session.delete(pendrivedetails)
        session.commit()
        flash("Deleted Pendrive Successfully")
        return redirect(url_for('showPds', pdccid=pdccid))
    else:
        return render_template('deletePenDrive.html',
                               pdccid=pdccid, pendrivedetails=pendrivedetails,
                               pendrives=pendrives)

####
# Logout from current user


@app.route('/logout')
def logout():
    access_token = login_pdsession_pduser['access_token']
    print ('In gdisconnect access token is %s', access_token)
    print ('User name is: ')
    print (login_pdsession_pduser['username'])
    if access_token is None:
        print ('Access Token is None')
        replyy = make_response(
            json.dumps('Current user not connected....'), 401)
        response.headers['Content-Type'] = 'application/json'
        return reply
    access_token = login_pdsession_pduser['access_token']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = \
        h.request(uri=url, method='POST', body=None,
                  headers={'content-type':
                           'application/x-www-form-urlencoded'})[0]

    print (result['status'])
    if result['status'] == '200':
        del login_pdsession_pduser['access_token']
        del login_pdsession_pduser['gplus_id']
        del login_pdsession_pduser['username']
        del login_pdsession_pduser['email']
        del login_pdsession_pduser['picture']
        reply = make_response(json.dumps('disconnected user..'), 200)
        reply.headers['Content-Type'] = 'application/json'
        return redirect(url_for('showUserLogin'))
        # return reply
    else:
        reply = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        reply.headers['Content-Type'] = 'application/json'
        return reply

#####
# Json Dispalys all details about the items and their values


@app.route('/PenDriveStore/JSON')
def allPenDrivesJSON():
    pendrivecategories = session.query(PenDrivesCompanyName).all()
    category_dict = [c.serialize for c in pendrivecategories]
    for c in range(len(category_dict)):
        pendrives = [i.serialize for i in session.query(
            PenDriveName).filter_by(
                pendrivecompanyid=category_dict[c]["id"]).all()]
        if pendrives:
            category_dict[c]["pendrive"] = pendrives
    return jsonify(PenDrivesCompanyName=category_dict)

# displays only the companies names of pendrives


@app.route('/PenDriveStore/pendriveCategories/JSON')
def categoriesJSON():
    pendrives = session.query(PenDrivesCompanyName).all()
    return jsonify(pendriveCategories=[c.serialize for c in pendrives])

# displays details only about pendrives


@app.route('/PenDriveStore/pendrives/JSON')
def itemsJSON():
    items = session.query(PenDriveName).all()
    return jsonify(pendrives=[i.serialize for i in items])

# it displays information about all companies


@app.route('/PenDriveStore/<path:pendrive_name>/pendrives/JSON')
def categoryItemsJSON(pendrive_name):
    pendriveCategory = session.query(PenDrivesCompanyName).filter_by(
        pdusername=pendrive_name).one()
    pendrives = session.query(PenDriveName).filter_by(
        pendrivecompany=pendriveCategory).all()
    return jsonify(pendriveEdtion=[i.serialize for i in pendrives])

'''it displays information about a pendrive and its model'''


@app.route('/PenDriveStore/<path:pendrive_name>/<path:edition_name>/JSON')
def ItemJSON(pendrive_name, edition_name):
    pendriveCategory = session.query(PenDrivesCompanyName).filter_by(
        pdusername=pendrive_name).one()
    pendriveEdition = session.query(PenDriveName).filter_by(
           pdusername=edition_name, pendrivecompany=pendriveCategory).one()
    return jsonify(pendriveEdition=[pendriveEdition.serialize])

if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host='127.0.0.1', port=8000)
