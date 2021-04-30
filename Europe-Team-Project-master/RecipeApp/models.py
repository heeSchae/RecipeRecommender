# -*- coding: utf-8 -*-
"""
    Module Level Docstring

    Q1 - matching recipes (inputs are ingredients-id)
    Q2 - matching recipes - content based (inputs are ingredients-id and user-id)
    Q3 - matching recipes - collaborative (inputs are ingredients-id and user-id)
    Q4 - additional ingredients (inputs are ingredients-id)
    Q5 - recipe-related and alternative ingredients (input is recipe-id)
    Q6 - recipe details (input is recipe-id)
    Q6.1 - recipe details for reviews (input is recipe-id)
    Q7 - recipe ratings (input is recipe-id)
"""

import json
import pandas as pd
from py2neo import Graph


def get_csv_dict(path='data/ingredient_autocomplete.csv'):
    ingredients = pd.read_csv(path, header=0).to_dict()
    return ingredients


def get_users(path='data/user_list.csv'):
    users = pd.read_csv(path, header=0).to_dict()
    return users


class PyNeoGraph:

    def __init__(self, debug=False):
        if not debug:
            self.driver = Graph(bolt=True, host='localhost')

    def test_conn(self):
        query = """
                MATCH (n) 
                RETURN n LIMIT 5
                """
        results = self.driver.run(query).to_data_frame()

        if results.size == 5:
            return True
        else:
            return False

    def close(self):
        self.driver.close()

    def get_neo4j_id(self, node="i:INGREDIENT", in_list=None):
        """
            Args:
                node(str): string in Cypher node format
                    (i:INGREDIENT) etc
                in_list(list): list of raw ids to match nodes

            Returns:
                ids(list): list of neo4j id properties for nodes
        """

        node_var, label = f"{node}".split(':')

        query = f"""
            MATCH ({node})
            WHERE {node_var}.{label.lower()} IN {in_list}
            RETURN id({node_var})
        """

        return self.driver.run(query).to_series().to_list()

    def get_matching_recipes(self, main_ingredients, side_ingredients):
        """
        Args:
            main_ingredients(list[str]): list of main_ingredient raw_ids and names
                ['7213&tomato'] etc
            side_ingredients(list[int]): list of side_ingredient raw_ids and names

        Returns:
            results(list[dict]): list of matching recipes
        """

        if side_ingredients[0] == '':
            side_ingredients = main_ingredients
        main = [int(i.split('&')[0]) for i in main_ingredients]
        side = [int(i.split('&')[0]) for i in side_ingredients]

        query = """
        //Q1_Matching Recipes
        MATCH 
            (i:INGREDIENT)<-[:CONTAINS]-(r:RECIPE)
        WITH
            r, collect(DISTINCT i.ingredient) AS ingredients,
            $main_ingredients AS main, $side_ingredients AS side
        WHERE 1=1
            and all(x IN main WHERE (x IN ingredients))
            and any(x IN side WHERE (x IN ingredients))
        WITH r.name as RecipeName, r.recipe as ID
        ORDER BY size([x IN side WHERE x IN ingredients]) DESC, r.n_ingredients
        WITH collect({ recipeName:RecipeName, recipeID:ID }) AS result
        RETURN result[0..10]
        """

        params = {"main_ingredients": main,
                  "side_ingredients": side}

        res = self.driver.run(query, params)

        results = res.data()

        results = results[0]["result[0..10]"]
        results = json.dumps(results)
        results = {'data': results}

        return results

    def get_content_based_recipes(self, user_id, main_ingredients, side_ingredients):
        """
        Args:
            user_id(int): id of the user
            main_ingredients(list[str]): list of main_ingredient raw_ids and names
                ['7213&tomato'] etc
            side_ingredients(list[int]): list of side_ingredient raw_ids and names

        Returns:
            results(list[dict]): list of matching recipes with content-based filtering
        """

        query = """       
        //Q2_Content based filtering
        MATCH //Find recipes similar to recpies rated by user (ID) #2203 and get their ingredients.
        (u:USER{user:$user})-[:RATED]->(r:RECIPE)-[s:SIMILAR]->(r2:RECIPE)-[:CONTAINS]->(i:INGREDIENT)
        WITH//save user_id, user rated recipes ( r ) and recipes similar to ( r ) along with a list of their aggregate ingredients
        u,r,r2,collect(DISTINCT i.ingredient) AS ingredients, count(r2.recipe) AS recipeCount, s.sim_score AS score, $main_ingredients AS main, $side_ingredients AS side
        WHERE 1=1 //filter only for recipes containing ALL main & ANY of the side ingredients
        and all(x IN main WHERE (x IN ingredients)) //all main
        and any(x IN side WHERE (x IN ingredients)) //any side
        WITH //return user_id, user_name, recipe rated by user, recommended recipe, similarity score and ingredient list in recommended recipe and calc number of matching ingredients in each recpie (no_sideIngr)
        u.user as user_id, r2.name as RecipeName, r.recipe as ID1, r2.recipe AS ID, r.name AS Name,ingredients, size([x IN side WHERE x IN ingredients]) as No_SideIngr, score
        ORDER BY No_SideIngr DESC, score DESC
        WITH collect({ recipeName:RecipeName, recipeID:ID }) AS result
        RETURN result[0..10]
        """

        if side_ingredients[0] == '':
            side_ingredients = main_ingredients
        main = [int(i.split('&')[0]) for i in main_ingredients]
        side = [int(i.split('&')[0]) for i in side_ingredients]

        params = {"main_ingredients": main,
                  "side_ingredients": side,
                  "user": user_id}
        res = self.driver.run(query, params).data()

        results = res[0]["result[0..10]"]
        results = json.dumps(results)
        results = {'data': results}

        return results

    def get_collaborative_recipes(self, user_id, main_ingredients, side_ingredients):
        """
        Args:
            user_id(int): id of the user
            main_ingredients(list[str]): list of main_ingredient raw_ids and names
                ['7213&tomato'] etc
            side_ingredients(list[int]): list of side_ingredient raw_ids and names

        Returns:
            results(list[dict]): list of matching recipes with collaborative filtering
        """

        query = """           
            //Q3_Collaborative filter
            MATCH (r:RECIPE)<-[:RATED]-(u2:USER)<-[s:SIMILAR]-(u:USER {user:$user}) 
            WITH r, count(r.recipe) AS recipeCount, s.sim_score AS score 
            ORDER BY recipeCount DESC, score DESC 
            WITH (r) MATCH (r)-[:CONTAINS]->(i:INGREDIENT) 
            WITH r, collect(DISTINCT i.ingredient) AS ingredients,$main_ingredients AS main, $side_ingredients AS side MATCH (r) 
            WHERE 1=1 
                and all(x IN main WHERE (x IN ingredients)) 
                and any(x IN side WHERE (x IN ingredients)) 
            WITH r.recipe AS ID, r.name AS RecipeName, size([x IN side WHERE x IN ingredients]) as No_SideIngr 
            ORDER BY No_SideIngr DESC LIMIT 10
            WITH collect({ recipeName:RecipeName, recipeID:ID }) AS result
            RETURN result[0..10]
                """

        if side_ingredients[0] == '':
            side_ingredients = main_ingredients
        main = [int(i.split('&')[0]) for i in main_ingredients]
        side = [int(i.split('&')[0]) for i in side_ingredients]

        params = {"main_ingredients": main,
                  "side_ingredients": side,
                  "user": user_id}
        res = self.driver.run(query, params).data()

        results = res[0]["result[0..10]"]
        results = json.dumps(results)
        results = {'data': results}
        return results

    def get_additional_ingredients(self, main_ingredients, side_ingredients):
        """
        Args:
            main_ingredients(list[str]): list of main_ingredient raw_ids and names
                ['7213&tomato'] etc
            side_ingredients(list[int]): list of side_ingredient raw_ids and names

        Returns:
            results(list[dict]): list of related ingredients based on similarity
        """
        if side_ingredients[0] == '' and len(side_ingredients) <= 1:
            ingredients = main_ingredients
        else:
            ingredients = main_ingredients + side_ingredients
        ingredients = [int(i.split('&')[0]) for i in ingredients]

        query = """
                //Q4_Probable_ingredient
                WITH $ingredients AS ingredients	// Ingredient input list
                MATCH p=(r:RECIPE)-[:CONTAINS]->(other:INGREDIENT)
                USING SCAN r:RECIPE
                WHERE all(i in ingredients 
                    WHERE exists((r)-[:CONTAINS]-(:INGREDIENT{ingredient:i})))
                AND NOT other.ingredient IN ingredients
                WITH count(p) AS ingrCount, other
                ORDER BY ingrCount DESC
                WITH collect({ingredientName:other.name, ingredientID:other.ingredient}) AS result
                RETURN result[0..10]
                """

        params = {"ingredients": ingredients}
        res = self.driver.run(query, params).data()

        results = res[0]["result[0..10]"]
        results = json.dumps(results)
        results = {'data': results}
        return results

    def get_relevant_ingredients(self, recipe_id):
        """
        Args:
            recipe_id(int): id of the recipe

        Returns:
            results(dict): dict of related ingredients
        """

        query = """
                //Q5_Ingredients in a recipe
                MATCH (i:INGREDIENT)<-[:CONTAINS]-(r:RECIPE), (a:INGREDIENT)<-[s:SIMILAR]-(i:INGREDIENT)
                WHERE r.recipe = $recipe_id
                RETURN i.name as ingredientName, i.ingredient as ingredientID, collect(Distinct a.name) as alternateIngredient
                """

        params = {"recipe_id": recipe_id}
        results = self.driver.run(query, params).data()

        results = json.dumps(results)
        results = {'data': results}
        return results

    def get_relevant_ratings(self, recipe_id):
        """
        Args:
            recipe_id(int): id of the recipe

        Returns:
            results(dict): dict of related ratings
        """

        query = """//07_Recipe ratings
                MATCH (r:RECIPE)<-[o:RATED]-(u:USER)
                WITH r, u.user as user, o.rating AS rating
                WHERE r.recipe=$recipe_id
                WITH collect({ userID:user, rating:rating }) AS result
                RETURN result[0..10]
                """

        params = {"recipe_id": recipe_id}
        res = self.driver.run(query, params).data()

        results = res[0]['result[0..10]']
        results = json.dumps(results)
        results = {'data': results}
        return results

    def get_recipe_details(self, recipe_id):
        """
        Args:
            recipe_id(int): id of the recipe

        Returns:
            results(dict): dict of recipe details
        """

        query = """                  
                //Q6_Recipe_details
                MATCH (r:RECIPE)
                WHERE r.recipe = $recipe_id
                RETURN DISTINCT r.steps as steps, 
                r.n_ingredients as numberOfIngredients, r.nutrition_dict as nutritionDetials, r.tags as tags
                """

        params = {'recipe_id': recipe_id}
        results = self.driver.run(query, params).data()
        results = json.dumps(results)
        results = {'data': results}
        return results

    def get_recipe_details_ratings(self, recipe_id):
        """
        Args:
            recipe_id(int): id of the recipe

        Returns:
            results(dict): dict of recipe details for rating information
        """

        query = """                
                //Q6.1_Recipe_details
                MATCH (u:USER)-[o:RATED]->(r:RECIPE)
                WHERE r.recipe = $recipe_id
                RETURN round(avg(tointeger(o.rating)),2) as avgRating, count(o.rating) as numberOfRatings
                """

        params = {'recipe_id': recipe_id}
        results = self.driver.run(query, params).data()
        results = json.dumps(results)
        results = {'data': results}
        return results
