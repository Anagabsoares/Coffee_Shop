import os
import sys
sys.path.append(os.getcwd())
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from database.models import setup_db, Drink
from auth.auth import AuthError, requires_auth


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    def after_request(response):

      response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization, true")
      response.headers.add(
            "Acess-Control-Allow-Methods", "GET, POST, DELETE,PATCH, OPTIONS"
        )
      return response

    @app.route('/login-results')  
    def login_results():
   
        return "Welcome to Coffee Shop!"


    @app.route("/drinks", methods=["GET"])
    # no permissions required
    def get_all_drinks():
        drinks = Drink.query.all()
        try:
            return (
                json.dumps(
                    {"success": True, "drinks": [drink.short() for drink in drinks]}
                ),
                200
            )
        except:
            abort(400)

    """
        @TODO implement endpoint
        POST /drinks
            it should create a new row in the drinks table
            it should require the 'post:drinks' permission
            it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
            or appropriate status code indicating reason for failure
    """

    @app.route("/drinks-post", methods=["POST"])
    @requires_auth("post:drinks")
    def drink_post(jwt):
        body = dict(request.form or request.json or request.data)
        new_drink_title = body.get("title", None)
        new_recipe_drink = body.get("recipe", None)
        try:
            drink = Drink(title=new_drink_title, recipe=json.dumps([new_recipe_drink]))
            drink.insert()
            return(
                 json.dumps({"success": True, "newly_created_drink": drink.long()}), 200)
            

        except Exception:
            abort(422)

    """
    @TODO implement endpoint
        GET /drinks-detail
            it should require the 'get:drinks-detail' permission
            it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
            or appropriate status code indicating reason for failure
    """

    @app.route("/drinks-detail", methods=["GET"])
    @requires_auth("get:drinks-detail")
    def drinks_detail(jwt):
        drinks = Drink.query.all()
        try:
            return (
                json.dumps(
                    {"success": True, "drinks": [drink.long() for drink in drinks]}
                ),
                200,
            )
        except Exception:
            abort(400)

    """
    @TODO implement endpoint
        PATCH /drinks/<id=drinks_id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should update the corresponding row for <id>
            it should require the 'patch:drinks' permission
            it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
            or appropriate status code indicating reason for failure
    """

    @app.route("/drinks-update/<int:id>", methods=["PATCH"])
    @requires_auth("patch:drinks")
    def update_drinks(jwt, id):
            id = id
            drink = Drink.query.filter(Drink.id==id).one_or_none()

            if drink is None:
                abort(404)
            try:
                body = dict(request.form or request.json or request.data)
                updated_recipe = body.get("recipe", None)
                updated_title = body.get("title", None)

                if updated_recipe:
                    drink.recipe = json.dumps(updated_recipe)
                if updated_title:
                    drink.title = updated_title

                drink.update()
                return (json.dumps({"success": True, "drinks": drink.long()}), 200)

            except Exception:
                abort(422)

    """
    @TODO implement endpoint
        DELETE /drinks/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should delete the corresponding row for <id>
            it should require the 'delete:drinks' permission
        returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
            or appropriate status code indicating reason for failure
    """

    @app.route("/drinks-delete/<int:drink_id>", methods=["DELETE"])
    @requires_auth("delete:drinks")
    def delete_drink(jwt, drink_id):
       
        drink = Drink.query.filter(Drink.id ==drink_id).one_or_none()

        if drink is None:
            abort(404)

        else:     
            try:
                drink.delete()

                return( json.dumps(
                        {
                            "success": True,
                            "deleted": drink.id,
                        }),200)
            
            except Exception:
                abort(400)

    ## Error Handling

    @app.errorhandler(404)
    def not_found(error):
        return (
                json.dumps({"success": False, "error": 404, "message": "Not found"}),
                 404)

    @app.errorhandler(422)
    def unprocessable(error):
        return(
            json.dumps({"success": False, "error": 422, "message": "unprocessable"}),
            422)
        

    @app.errorhandler(400)
    def bad_request(error):
        return( 
            json.dumps({"success": False, "error": 400, "message": "bad request"}),
         400)

    @app.errorhandler(500)
    def internal_service_error(error):
        return(
            json.dumps(
                {"success": False, "error": 500, "message": "internal server error"}),
            500)
       
    @app.errorhandler(401)
    def unauthorized_error(error):
        return (
            json.dumps(
                {"success": False, "error": 401, "message": "unauthorized"}),
            401)   

    """
    @TODO implement error handler for AuthError
        error handler should conform to general task above 
    """

    @app.errorhandler(AuthError)
    def auth_error(error):
        response = jsonify(error.error)
        response.status_code = error.status_code
        return response

    return app
