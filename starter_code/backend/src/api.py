import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS, cross_origin

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth, requires_scope

drinks_per_page = 10

def paginate_drinks(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * drinks_per_page
    end = start + drinks_per_page
    formatted_drinks = [question.format() for question in selection]
    current_drinks = formatted_drinks[start:end]
    return current_drinks

app = Flask(__name__)
setup_db(app)
CORS(app)

db_drop_and_create_all()

@app.route("/drinks", methods=["GET"])
        # no permissions required
def get_all_drinks():
    try:
        drinks = Drink.query.order_by(Drink.id).all()
        drink_paginated= paginate_drinks(request, drinks)
        return jsonify({
                "success": True,
                "drinks": [drink.short() for drink in drink_paginated ]
                },200)
    except Exception:
        abort(400)
    # '''
    # @TODO implement endpoint
    #     GET /drinks-detail
    #         it should require the 'get:drinks-detail' permission
    #         it should contain the drink.long() data representation
    #     returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
    #         or appropriate status code indicating reason for failure
    # '''
@app.route("/drinks", methods=["GET"])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def get_drinks_details():
    if requires_scope("get:drinks-detail"):
            try:
                drinks = Drink.query.order_by(Drink.id).all()
                drink_paginated= paginate_drinks(request, drinks)
                return jsonify(
                    {
                    "success": True,
                    "drinks": [drink.long() for drink in drink_paginated ]
                    }, 200)
            except Exception:
                abort(400)
    else:
        abort(401)        
    # '''
    #     @TODO implement endpoint
    #     POST /drinks
    #         it should create a new row in the drinks table
    #         it should require the 'post:drinks' permission
    #         it should contain the drink.long() data representation
    #     returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
    #         or appropriate status code indicating reason for failure
    # '''
@app.route("/drinks", methods=["POST"])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def drink_post():
    if requires_scope("post:drinks"):
        body = request.get_json()
        new_drink_title = body.get("title",None)
        new_drink_recipe = body.get("recipe",None)
        drink = Drink(
                    title= new_drink_title,
                    recipe= new_drink_recipe
                    )
        try:
            drink.insert()
            return jsonify(
                    {
                        "success": True,
                        "newly_created_drink": drink.long()
                    }, 200)
        except Exception:
                abort(422)
    else:
        abort(401)

    # '''
    # @TODO implement endpoint
    #     PATCH /drinks/<id=drinks_id>
    #         where <id> is the existing model id
    #         it should respond with a 404 error if <id> is not found
    #         it should update the corresponding row for <id>
    #         it should require the 'patch:drinks' permission
    #         it should contain the drink.long() data representation
    #     returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
    #         or appropriate status code indicating reason for failure
    # '''

@app.route('/drinks/<int:drink_id>', methods=["PATCH"])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def update_drink(drink_id):
    if requires_scope("patch:drinks"):
        try:
            drinks_id = Drink.query.filter_by(Drink.id==drink_id).one_or_none()
            if drink_id is None:
                    abort(404)
            else:   
                body = request.get_json()
                if 'title' in body:
                    drinks_id.title=body['titlle']
                if 'recipe' in body:
                    drinks_id.recipe=body['recipe']
                            
                drinks_id.update()
                return jsonify({
                        "success": True,
                        "drinks": [drinks_id.long()]
                        }, 200
                    )
        except Exception:
            abort(400)  
    else:
        abort(401)          

    # '''
    # @TODO implement endpoint
    #     DELETE /drinks/<id>
    #         where <id> is the existing model id
    #         it should respond with a 404 error if <id> is not found
    #         it should delete the corresponding row for <id>
    #         it should require the 'delete:drinks' permission
    #     returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
    #         or appropriate status code indicating reason for failure
    # '''

@app.route("/drinks/<int:drink_id>", methods=["DELETE"])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def delete_drink(drink_id):
    if requires_scope("delete:drinks"):
        try:
            drink = Drink.query\
                    .filter(Drink.id == drink_id)\
                    .one_or_none()
            if drink is None:
                    abort(404)
            else:
                drink.delete()

            return jsonify(
                    {
                    "success": True,
                    "deleted": drink.id,
                    },200
                    )
        except Exception:
                abort(422)
    else:
        abort(401)
    ## Error Handling

@app.errorhandler(404)
def not_found(error):
    return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"}), 404

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"}), 422
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"}), 400

@app.errorhandler(500)
def internal_service_error(error):
    return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"}), 500

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
            "success": False,
            "error": 401,
            "message": "unauthorized"
    }), 401

    # '''
    # @TODO implement error handler for AuthError
    #     error handler should conform to general task above 
    # '''
@app.errorhandler(AuthError)
def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response


