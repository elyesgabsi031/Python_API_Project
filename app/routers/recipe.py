from fastapi import HTTPException, status,Query,APIRouter,Depends
from .. import schemas, database,oauth2  #has our pydantic model , db conn , jwt auth


 
router = APIRouter(
    tags=['Recipes']
)

#connection to database
conn,cursor = database.establish_connection()


#Get all recipes from db
@router.get("/recipes")
def get_recipes():
    cursor.execute("""SELECT * FROM recipes""")
    recipes = cursor.fetchall()
    
    return {"recipes":recipes}

#post a recipe into the db            
@router.post("/recipes", status_code=status.HTTP_201_CREATED)
def post_recipe(recipe: schemas.Recipe, user_id: int = Depends(oauth2.get_current_user)):
    cursor.execute("""INSERT INTO recipes(name,country,type,ingredients,instructions,cooking_time,difficulty) 
                   VALUES(%s,%s,%s,%s,%s,%s,%s) RETURNING *""",(recipe.name,recipe.country,recipe.type,recipe.ingredients,
                                                    recipe.instructions,recipe.cooking_time,recipe.difficulty))
    new_recipe = cursor.fetchone()
    conn.commit()
    
    return new_recipe
    
#get a recipe with its proper id    
@router.get("/recipes/{id}")
def get_recipe(id : int):
    cursor.execute("""SELECT * FROM recipes WHERE id = %s """,(id,)) 
    recipe = cursor.fetchone()
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"recipe with {id} not found")
    return recipe


#delete a recipe using its id
@router.delete("/recipes/{id}",status_code=204)
def delete_recipe(id: int, user_id: int = Depends(oauth2.get_current_user)):
    cursor.execute(""" DELETE FROM recipes WHERE id = %s returning * """,(id,))
    del_recipe = cursor.fetchone()
    conn.commit()
    if del_recipe == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"recipe with id number {id} not found")
    

#update a recipe using its id
@router.put("/recipes/{id}")
def update_recipe(id : int, recipe: schemas.Recipe, user_id: int = Depends(oauth2.get_current_user) ):
    cursor.execute(""" UPDATE recipes SET name = %s, country= %s, type=%s, ingredients=%s, 
                   instructions=%s, cooking_time=%s, difficulty=%s WHERE id = %s RETURNING *""",(recipe.name,recipe.country,recipe.type,recipe.ingredients,
                                                    recipe.instructions,recipe.cooking_time,recipe.difficulty,id,))
    updated_recipe= cursor.fetchall()    
    conn.commit()

    if updated_recipe == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"recipe with id number {id} not found")
   
    return updated_recipe




#Get recipe by ingredients
@router.get("/search-recipes")
def get_recipes_by_ingredients( ingredients: str = Query(..., title="Ingredients", 
                                                         description="Comma-sep list of ingredients"),):
    
    ingredients_list = [ingredient.strip() for ingredient in ingredients.split(",")]
    query = """SELECT * FROM recipes WHERE"""
    conditions = " AND ".join(["ingredients LIKE %s" for _ in ingredients_list])
    query += f" ({conditions})"

    cursor.execute(query, tuple(f"%{ingredient}%" for ingredient in ingredients_list))

    recipes = cursor.fetchall()

    if not recipes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recipes with the specified ingredients not found",
        )

    return recipes


#get a recipe with country
@router.get("/recipes/country/{country}")
def get_recipe(country : str):
    cursor.execute("""SELECT * FROM recipes WHERE country Like %s """,(country,)) 
    recipes = cursor.fetchall()
    if not recipes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"recipe with {country} not found")
    return recipes