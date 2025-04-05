from google import genai
from google.genai import types

import PIL.Image
import os
import json

image = PIL.Image.open('checkers_page_3_example.jpg')

client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=["You are a chef doing meal prep for a healthy resteraunt. The image will containt coupons from a local store. Your job is to create three healthy meals from some of the items in the coupon and return the meals in the following JSON format. {Meal1 Name: meal1 name, Meal Items: {Item1: Quantity,...}Meal2 Name: meal2 name...} but instead of writing ... finish the meals. The meals are only inspired from the items in the coupons, so please write out a full list of ingredients, even if the ingredients aren't in the coupons.", image]
)

text = response.text
meals = json.loads(text.removeprefix("```json\n").removesuffix("```"))

print(meals)
print(type(meals))