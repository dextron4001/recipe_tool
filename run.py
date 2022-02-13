import os
import json

def recipe_data(recipe):
    obj = {
        "name" : recipe["name"],
        "rating" : recipe["rating"]
        }
    return obj

recipe_library = []
potential_ingredients = {}

# load recipes
for filename in os.listdir("recipes"):
    f = os.path.join("recipes", filename)
    if os.path.isfile(f):
         with open(f) as json_file:
            data = json.load(json_file)
            recipe_library.append(data)

# analyse recipes
for item in recipe_library:
    item["required ingredients"] = len(item["ingredients"])
    item['available ingredients'] = 0
    for i in item["ingredients"]:
        i['available'] = False
        if str(i["name"]) in potential_ingredients:
            recipe_list = potential_ingredients[str(i["name"])]
            recipe_list.append(recipe_data(item))
            potential_ingredients[str(i["name"])] = recipe_list
        else: 
            potential_ingredients[str(i["name"])] = [recipe_data(item)]

print("=========================================================")
print("Hello Jad these are the ingredients you can choose from :")
for key in potential_ingredients.keys():
  print(f"* {key}")

avialable_ingredients = ["spaghetti", "onion","pesto"] #input()
print("-----------------------------------------")
print("These are the ingredients you chose : ")
for i in avialable_ingredients:
  print(f"* {i}")


# check recipes you can make:
recipes_search = recipe_library
possible_recipes = []
possible_names = []
print("------------------------------------------------------")
print(f"checking a total of {len(recipes_search)} recipes")

for i in avialable_ingredients:
    for e,r in enumerate(recipes_search):
        for ing in r['ingredients']:
            if i == ing['name']:
                r['available ingredients'] = r['available ingredients'] + 1 
                ing['available'] = True
        r['remaining ingredients'] = r['required ingredients'] - r['available ingredients']
        # get possible recipes
        if r['remaining ingredients'] == 0:
            if r['name'] not in possible_names:
                possible_recipes.append(r)
                possible_names.append(r["name"])
                recipes_search.pop(e)

print("=========================================================================")
print("    ")
print('With what you have available you can cook these great recipes :')
possible_recipes = sorted(possible_recipes, key=lambda d: d['rating'], reverse=True) 
for i in possible_recipes:
  print(f"* {i['name']} ({i['rating']})") # these need to be sorted 
print("     ")
print("=========================================================================")
print("     ")
print("with a couple of extra items you could also cook up : ")


recipes_search = sorted(recipes_search, key=lambda d: d['remaining ingredients'])
other_recipes = []
#while len(other_recipes) < 3 or len(other_recipes) < len(recipes_search) :
for e,r in enumerate(recipes_search):
    required_ingredients = []
    for i in r['ingredients']:
        if not i['available']:
            required_ingredients.append(i['name'])
    r['required_ingredients'] = required_ingredients
    other_recipes.append(r)

for i in other_recipes:
    print(f"* {i['name']} ({i['rating']})")
    print("you just need:")
    for r in i['required_ingredients']:
      print(f'* {r}')
    print("-------------")

