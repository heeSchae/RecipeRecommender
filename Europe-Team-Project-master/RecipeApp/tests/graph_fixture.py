"""
"""

from pathlib import Path
from glob import glob


class RecipeQuery:
    def __init__(self, neo4j_driver):

        self.graph = neo4j_driver
        self.query_paths = self.get_query_paths(Path("data\\01_Queries"))
        self.query_results = self.get_query_results(Path("data\\01_Queries"))

    def get_query_paths(self, query_path):
        queries = (glob((query_path / '*/*.cypher').as_posix()))
        return queries

    def get_query_results(self, query_path):
        results = (glob((query_path / '*/*.json').as_posix()))
        return results

    def get_file(self, file_path):

        with open(file_path, mode='r', newline='\n') as f:
            out_file = f.read()

        return out_file


class PyNeoGraphUI:

    def get_matching_recipes(self, main_ingredients, side_ingredients):
        """
        """

        results = [
            {
                "result[0..10]": [
                    {
                        "recipeName": "stuffed peppers with sausage",
                        "recipeID": 434234
                    },
                    {
                        "recipeName": "strip salad",
                        "recipeID": 41284
                    },
                    {
                        "recipeName": "fresh tomato and roasted garlic salad dressing",
                        "recipeID": 108091
                    },
                    {
                        "recipeName": "spinach and mushroom pizza",
                        "recipeID": 39912
                    },
                    {
                        "recipeName": "linguine with tomatoes and basil",
                        "recipeID": 110808
                    },
                    {
                        "recipeName": "zucchini packets for the grill",
                        "recipeID": 41087
                    },
                    {
                        "recipeName": "roasted tomato salad",
                        "recipeID": 63172
                    },
                    {
                        "recipeName": "linguini alla cecca",
                        "recipeID": 27118
                    },
                    {
                        "recipeName": "pasta w  garlic and veggies",
                        "recipeID": 46991
                    }
                ]
            }
        ]

        results = results[0]["result[0..10]"]
        results = json.dumps(results)
        results = {'data': results}

        return results

    def get_content_based_recipes(self, user_id, main_ingredients, side_ingredients):

        results = [
            {
                "result[0..10]": [  # TODO: change to 0..10 in UI
                    {
                        "recipeName": "zucchini packets for the grill",
                        "recipeID": 41087
                    },
                    {
                        "recipeName": "nancy duke s ratatouille",
                        "recipeID": 93260
                    }
                ]
            }
        ]

        results = results[0]["result[0..10]"]
        results = json.dumps(results)
        results = {'data': results}

        return results

    def get_collaborative_recipes(self, user_id, main_ingredients, side_ingredients):

        results = [
            {
                "result[0..10]": [
                    {
                        "recipeName": "fresh tomato and roasted garlic salad dressing",
                        "recipeID": 108091
                    },
                    {
                        "recipeName": "zucchini marinara   diabetic",
                        "recipeID": 86077
                    },
                    {
                        "recipeName": "so easy pasta with fresh herbs and cold tomato",
                        "recipeID": 139450
                    },
                    {
                        "recipeName": "savory garbanzo beans over couscous",
                        "recipeID": 50730
                    },
                    {
                        "recipeName": "roasted tomato salad",
                        "recipeID": 63172
                    },
                    {
                        "recipeName": "azteca soup adopted",
                        "recipeID": 3614
                    },
                    {
                        "recipeName": "tofu parmesan",
                        "recipeID": 23997
                    },
                    {
                        "recipeName": "quick   easy chicken in wine sauce",
                        "recipeID": 89598
                    },
                    {
                        "recipeName": "grecian lamb with vegetables",
                        "recipeID": 89997
                    }
                ]
            }
        ]

        results = results[0]["result[0..10]"]
        results = json.dumps(results)
        results = {'data': results}

        return results

    def get_additional_ingredients(self, main_ingredients, side_ingredients):

        results = [
            {
                "res[0..10]": [
                    {
                        "ingredientID": 5010,
                        "ingredientName": "onion"
                    },
                    {
                        "ingredientID": 5006,
                        "ingredientName": "olive oil"
                    },
                    {
                        "ingredientID": 6270,
                        "ingredientName": "salt"
                    },
                    {
                        "ingredientID": 5319,
                        "ingredientName": "pepper"
                    },
                    {
                        "ingredientID": 7655,
                        "ingredientName": "water"
                    },
                    {
                        "ingredientID": 6276,
                        "ingredientName": "salt and pepper"
                    },
                    {
                        "ingredientID": 5180,
                        "ingredientName": "parmesan cheese"
                    },
                    {
                        "ingredientID": 6335,
                        "ingredientName": "scallion"
                    },
                    {
                        "ingredientID": 840,
                        "ingredientName": "butter"
                    }
                ]
            }
        ]

        results = results[0]["res[0..10]"]
        results = json.dumps(results)
        results = {'data': results}

        return results

    def get_relevant_ingredients(self, recipe_id):

        results = [
            {
                "ingredientName": "basil",
                "ingredientID": 382
            },
            {
                "ingredientName": "parmesan cheese",
                "ingredientID": 5180
            },
            {
                "ingredientName": "red wine vinegar",
                "ingredientID": 6009
            },
            {
                "ingredientName": "olive oil",
                "ingredientID": 5006
            },
            {
                "ingredientName": "garlic",
                "ingredientID": 3184
            },
            {
                "ingredientName": "frozen pea",
                "ingredientID": 3046
            },
            {
                "ingredientName": "tomato",
                "ingredientID": 7213
            }
        ]

        results = json.dumps(results)
        results = {'data': results}

        return results

    def get_alternative_ingredients(self, recipe_id):

        results = [
            {
                "ingredientName": "basil",
                "ingredientID": 382,
            },
            {
                "ingredientName": "parmesan cheese",
                "ingredientID": 5180
            },
            {
                "ingredientName": "red wine vinegar",
                "ingredientID": 6009
            }
        ]

        results = json.dumps(results)
        results = {'data': results}

        return results

    def get_relevant_ratings(self, user_id, recipe_id):
        """
        """

        results = [
            {
                "result[0..10]": [
                    {
                        "rating": "5.0",
                        "userID": 4407
                    },
                    {
                        "rating": "5.0",
                        "userID": 4760
                    },
                    {
                        "rating": "5.0",
                        "userID": 10
                    },
                    {
                        "rating": "0.0",
                        "userID": 317
                    },
                    {
                        "rating": "5.0",
                        "userID": 325
                    },
                    {
                        "rating": "5.0",
                        "userID": 358
                    },
                    {
                        "rating": "4.0",
                        "userID": 395
                    },
                    {
                        "rating": "4.0",
                        "userID": 8321
                    },
                    {
                        "rating": "5.0",
                        "userID": 5132
                    }
                ]
            }
        ]

        results = results[0]["result[0..10]"]
        results = json.dumps(results)
        results = {'data': results}

        return results

    def get_recipe_details(self, recipe_id):

        results = [
            {
                "steps": "['heat oven to 350 degrees', 'brush the garlic cloves with 1 teaspoon of the oil , reserving the remaining oil', 'roast the oiled garlic cloves in a pan until golden and soft , about 10 to 15 minutes', 'watch carefully so garlic does not get over-brown or burn', 'carefully remove pan from oven and cool', 'when cool enough to handle , squeeze out the garlic pulp', 'combine the pulp with the reserved olive oil and rest of the ingredients in a blender', 'blend until smooth and use the dressing on any mixed garden salad', 'refrigerate leftover']",
                "calorieLevel": "2",
                "numberOfIngredients": 7,
                "nutritionDetials": "{'calories': 587.2, 'total fat': 84.0, 'sugar': 35.0, 'sodium': 1.0, 'protein': 9.0, 'saturated fat': 38.0, 'carbohydrates': 7.0}",
                "tags": "['30-minutes-or-less', 'time-to-make', 'course', 'main-ingredient', 'cuisine', 'preparation', 'occasion', 'north-american', 'low-protein', 'healthy', 'salads', 'fruit', 'vegetables', 'canadian', 'oven', 'refrigerator', 'dinner-party', 'holiday-event', 'picnic', 'salad-dressings', 'food-processor-blender', 'dietary', 'low-sodium', 'low-cholesterol', 'low-carb', 'healthy-2', 'ontario', 'low-in-something', 'citrus', 'lemon', 'onions', 'tomatoes', 'to-go', 'equipment', 'small-appliance', 'presentation', 'served-cold']",
                "avgRating": 4.46,
                "numberOfRatings": 13
            }
        ]

        results = json.dumps(results)
        results = {'data': results}

        return results
