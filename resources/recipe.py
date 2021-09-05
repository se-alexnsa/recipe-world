from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.recipe import RecipeModel


class Recipe(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('ingredients',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('method',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    @jwt_required()
    def get(self, name):
        recipe = RecipeModel.find_by_name(name)
        if recipe:
            return recipe.json()
        return {'message': 'recipe not found'}, 404

    def post(self, name):
        if RecipeModel.find_by_name(name):
            return {'message': "An recipe with name '{}' already exists.".format(name)}, 400

        data = Recipe.parser.parse_args()

        recipe = RecipeModel(**data)

        try:
            recipe.save_to_db()
        except:
            return {"message": "An error occurred inserting the recipe."}, 500

        return recipe.json(), 201

    def delete(self, name):
        recipe = RecipeModel.find_by_name(name)
        if recipe:
            recipe.delete_from_db()
            return {'message': 'Recipe deleted.'}
        return {'message': 'Recipe not found.'}, 404

    def put(self, name):
        data = Recipe.parser.parse_args()

        recipe = RecipeModel.find_by_name(name)

        if recipe:
            recipe.name = data['name']
        else:
            recipe = RecipeModel(**data)

        recipe.save_to_db()

        return recipe.json()


class RecipeList(Resource):
    def get(self):
        return {'recipes': list(map(lambda x: x.json(), RecipeModel.query.all()))}
