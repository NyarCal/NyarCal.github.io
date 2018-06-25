from flask import Flask,abort,jsonify,request,url_for
app = Flask(__name__, static_url_path = "")

rides = [
    {
        'id': 1,
        'title': u'Add Ride Offers',
        'description': u'Driver, Route, Departure, Fare', 
        'done': False
    },
    {
        'id': 2,
        'title': u'View Ride Offers',
        'description': u'Benz,Nairobi-Kisumu,Kshs.500', 
        'done': False
    }
]
def make_public_ride(ride):
    new_ride = {}
    for field in rides:
        if field == 'id':
            ride['uri'] = url_for('get_task', ride_id = ride['id'], _external = True)
        else:
            new_ride[field] = ride[field]
    return ride

def get_rides():
    return jsonify( { 'rides': map(make_public_ride, rides) } )

@app.route('/getride/api/v1/rides/<int:ride_id>', methods = ['GET'])
def get_ride(ride_id):
    ride = filter(lambda t: t['id'] == ride_id, rides)
    if len(ride) == 0:
        abort(404)
    return jsonify( { 'task': make_public_ride(rides[0]) } )

@app.route('/todo/api/v1.0/rides', methods = ['POST'])
def create_ride():
    if not request.json or not 'title' in request.json:
        abort(400)
    ride = {
        'id': rides[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    rides.append(ride)
    return jsonify( { 'task': make_public_ride(ride) } ), 201

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['PUT'])

def update_ride(ride_id):
    ride = list(filter(lambda t: t['id'] == ride_id, rides))
    if len(ride) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != str:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    ride[0]['title'] = request.json.get('title', ride[0]['title'])
    ride[0]['description'] = request.json.get('description', ride[0]['description'])
    ride[0]['done'] = request.json.get('done', ride[0]['done'])
    return jsonify( { 'tasks': list(map(make_public_ride, rides)) } )
        