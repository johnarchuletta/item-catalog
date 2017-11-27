from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, make_response
from flask import session as login_session
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import OperationalError
from db.db_models import Base, Category, Item, User
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError

import json, random, string, httplib2, requests
import mock.data as mock


APP = Flask(__name__)

### Constants #################################################################

CLIENT_ID = json.loads(
    open('client_secret.json', 'r').read()
)['web']['client_id']
APPLICATION_NAME = 'Web Store'

### Database Connection #######################################################

ENGINE = create_engine('sqlite:///db/itemcatalog.db')
Base.metadata.bind = ENGINE
DB_SESSION = sessionmaker(bind=ENGINE)
SESSION = DB_SESSION()

### Public Routes ####################################################################

@APP.route('/')
def index():
    '''Index page route.'''

    try:
        categories = SESSION.query(Category).all()
        items = SESSION.query(Item).all()
    except OperationalError:
        return 'Nothing to show.'

    if 'state' not in login_session:
        state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                        for x in xrange(32))
        login_session['state'] = state

    username = ''
    picture = ''
    user_id = ''

    if 'username' in login_session:
        username = login_session['username']
        picture = login_session['picture']
        user_id = login_session['user_id']

    return render_template(
        'index.pug',
        site_title=APPLICATION_NAME,
        category_name='all',
        categories=categories,
        items=items,
        state=login_session['state'],
        username=username,
        picture=picture,
        user_id=user_id
    )

@APP.route('/<string:category_name>')
def show_category(category_name):
    '''Route for all items in specified category.'''

    if 'state' not in login_session:
        state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                        for x in xrange(32))
        login_session['state'] = state

    username = ''
    picture = ''
    user_id = ''

    if 'username' in login_session:
        username = login_session['username']
        picture = login_session['picture']
        user_id = login_session['user_id']

    try:
        categories = SESSION.query(Category).all()
        category = SESSION.query(Category).filter_by(name=category_name.lower()).one()
        items = SESSION.query(Item).filter_by(category_id=category.id)
        return render_template(
            'index.pug',
            site_title=APPLICATION_NAME,
            category_name=category.name,
            categories=categories,
            items=items,
            state=login_session['state'],
            username=username,
            picture=picture,
            user_id=user_id
        )
    except OperationalError:
        return 'No data.'
    except NoResultFound:
        return 'Category not found.'

@APP.route('/item')
def item():
    if 'state' not in login_session:
        state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                        for x in xrange(32))
        login_session['state'] = state

    username = ''
    picture = ''
    user_id = ''

    if 'username' in login_session:
        username = login_session['username']
        picture = login_session['picture']
        user_id = login_session['user_id']

    try:
        the_item = SESSION.query(Item).filter_by(id=request.args['id']).one()
        return render_template(
            'item.pug',
            site_title=APPLICATION_NAME,
            item=the_item,
            state=login_session['state'],
            username=username,
            picture=picture,
            user_id=user_id,
            hide_login=True
        )
    except OperationalError:
        return 'No data.'
    except NoResultFound:
        return 'Category not found.'

### Protected Routes ##########################################################

@APP.route('/add', methods=['GET', 'POST'])
def add():
    '''Route to add new item to catalog.'''

    if request.method == 'GET':
        try:
            categories = SESSION.query(Category).all()
        except OperationalError:
            return 'Error'

        return render_template(
            'add.pug',
            site_title=APPLICATION_NAME,
            action='add',
            hide_login=True,
            categories=categories
        )
    else:
        if 'username' in login_session:
            category = SESSION.query(Category).filter_by(id=request.form['category']).one()
            user = SESSION.query(User).filter_by(id=login_session['user_id']).one()
            new_item = Item(
                name=request.form['name'],
                description=request.form['description'],
                price=request.form['price'],
                image=request.form['image'],
                category=category,
                user_id=user.id
            )
            SESSION.add(new_item)
            SESSION.commit()
            return redirect('/')
        else:
            return 'Could not complete requested action.'

@APP.route('/edit', methods=['GET', 'POST'])
def edit():
    '''Route to edit an item in catalog.'''

    if request.method == 'GET':
        if 'username' in login_session:
            categories = SESSION.query(Category).all()
            item = SESSION.query(Item).filter_by(id=request.args['id']).one()
            if item.user_id == login_session['user_id']:
                return render_template(
                    'edit.pug',
                    site_title=APPLICATION_NAME,
                    item=item,
                    categories=categories
                )
            else:
                return redirect('/')
        else:
            return redirect('/')
    else:
        if 'username' in login_session:
            item = SESSION.query(Item).filter_by(id=request.args['id']).one()
            category = SESSION.query(Category).filter_by(id=request.form['category']).one()
            item.name = request.form['name']
            item.description = request.form['description']
            item.price = request.form['price']
            item.category = category
            item.image = request.form['image']
            SESSION.commit()
            return redirect('/')
        else:
            return 'You are not logged in.'


@APP.route('/delete', methods=['GET', 'POST'])
def delete():
    '''Route to DELETE supplied item'''

    if request.method == 'GET':
        if 'username' in login_session:
            item = SESSION.query(Item).filter_by(id=request.args['id']).one()

            return render_template(
                'delete.pug',
                site_title=APPLICATION_NAME,
                action='delete',
                hide_login=True,
                item=item)
        else:
            return 'You are not logged in.'
    else:
        if 'username' in login_session:
            item = SESSION.query(Item).filter_by(id=request.args['id']).one()
            if item.user_id == login_session['user_id']:
                SESSION.delete(item)
                SESSION.commit()
                return redirect('/')
            else:
                return 'Could not complete action.'

### API Endpoints #############################################################

@APP.route('/api/v1/categories')
def json_categories():
    categories = SESSION.query(Category).all()
    return jsonify(categories=[i.serialize for i in categories])

@APP.route('/api/v1/items')
def json_items():
    items = SESSION.query(Item).all()
    return jsonify(categories=[i.serialize for i in items])

### Google Authentication Routes ##############################################

@APP.route('/gconnect', methods=['POST'])
def googleSignIn():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['content-type'] = 'application/json'
        return response

    code = request.data

    try:
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['content-type'] = 'application/json'
        return response

    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    http = httplib2.Http()
    result = json.loads(http.request(url, 'GET')[1])

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['content-type'] = 'application/json'
        return response

    gplus_id = credentials.id_token['sub']

    if result['user_id'] != gplus_id:
        response = make_response(json.dumps('Token\'s user ID doesn\'t match given user ID.'), 401)
        response.headers['content-type'] = 'application/json'
        return response

    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps('Token\'s client ID does not match app\'s.', 401))
        response.headers['content-type'] = 'application/json'
        print 'Token\'s client ID does not match app\'s.'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')

    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'), 200)
        response.headers['content-type'] = 'application/json'
        return response

    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['google_id'] = data['id']

    try:
        db_user = SESSION.query(User).filter_by(google_id=data['id']).one()
        login_session['user_id'] = db_user.id
    except NoResultFound:
        new_user = User(
            name=data['name'],
            picture=data['picture'],
            email=data['email'],
            google_id=data['id']
        )
        SESSION.add(new_user)
        SESSION.commit()
        login_session['user_id'] = new_user.id

    response = make_response(json.dumps('Success!'), 200)
    response.headers['content-type'] = 'application/json'

    return response

@APP.route('/gdisconnect')
def googleSignOut():
    if 'access_token' in login_session:
        access_token = login_session['access_token']
    else:
        return 'User not logged in.'

    if access_token is None:
        response = make_response(json.dumps('Current user not connected'), 401)
        response.headers['content-type'] = 'application/json'
        return response

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        return redirect('/')
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['content-type'] = 'application/json'
        return response

@APP.route('/clear-session')
def clear_session():
    login_session.clear()
    return 'Session cleared.'

### Main ######################################################################

if __name__ == '__main__':
    APP.secret_key = 'd3athb3for3surr3nd3r303'
    APP.debug = True
    APP.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')
    APP.jinja_env.auto_reload = True
    APP.config['TEMPLATES_AUTO_RELOAD'] = True
    APP.run(host='0.0.0.0', port=8080)
    