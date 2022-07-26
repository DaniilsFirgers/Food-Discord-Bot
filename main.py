import discord
import os
import requests
import json
import random
from keep_alive import keep_alive

client = discord.Client()

def load_categories():
    categories_url = 'https://www.themealdb.com/api/json/v1/1/categories.php'
    
    response = requests.get(categories_url).json()
    categories = [response['categories'][n]['strCategory'] for n in range(0,len(response['categories']))]
    return categories

def get_recipe(category):

    meals_id_url = 'https://www.themealdb.com/api/json/v1/1/filter.php?c={0}'.format(category)
    response_1 = requests.get(meals_id_url).json()

    ids = [response_1['meals'][n]['idMeal'] for n in range(0, len(response_1['meals']))]
    random_meal_id = random.choice(ids)

    meal_recipe_url = 'https://www.themealdb.com/api/json/v1/1/lookup.php?i={0}'.format(random_meal_id)
    response_2 = requests.get(meal_recipe_url).json()
    recipe_dict ={
        'name': response_2['meals'][0]['strMeal'],
        'instructions': response_2['meals'][0]['strInstructions'],
        'ingredients': {response_2['meals'][0][f'strIngredient{n}']:response_2['meals'][0][f'strMeasure{n}'] for n in range(1, 20)
                        if response_2['meals'][0][f'strIngredient{n}'] != None
                        if response_2['meals'][0][f'strIngredient{n}'] != ""}
    }
    return recipe_dict



@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content
  
  if message.content.startswith('hello'):
    await message.channel.send('Hello!')
  if any(category in msg.title() for category in load_categories()):
    recipe = get_recipe(msg.title())
    await message.channel.send('Dish name: {0}\n\n'.format(recipe['name']))
    await message.channel.send('Recipe: {0}\n\n'.format(recipe['instructions']))
    await message.channel.send('Ingredients:\n\n')
    for k,v in recipe['ingredients'].items():
      await message.channel.send(f"{k}: {v}")
  await message.channel.send(f'Please enter one of the keywords to get a new recipe for a certain category:{load_categories()}')    
    

keep_alive()
client.run(os.environ['TOKEN'])

