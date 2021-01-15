import os
import csv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wesop.settings")

import django

django.setup()

from products.models import (Category,
                             SubCategory,
                             Product,
                             Media,
                             Skin,
                             Feel,
                             Ingredient,
                             Texture,
                             Aroma)


with open("wesop.csv", newline='') as f:
	rows = csv.reader(f, delimiter=',')
	rows = list(rows)[1:]

Category.objects.get_or_create(name=rows[0][0])
SubCategory.objects.get_or_create(name=rows[0][1], category=Category.objects.get(name=rows[1][0]))

for row in rows:
    Product.objects.get_or_create(
                                name=row[2], 
                                size=row[3], 
                                description=row[4],
                                manual=row[8],
                                price=row[9],
                                dosage=row[10],
                                )
for row in rows:
    Media.objects.get_or_create(url=row[13], products=Product.objects.get(name=row[2]))

def make_row_unique_el(row):
    result = []
    for string in row:
        result.extend(string.split(','))

    for index in range(len(result)):
        result[index] = result[index].strip()

    result = list(set(result))
    return result

skin_type_row = [row[5] for row in rows]
skin_type_row_unique = make_row_unique_el(skin_type_row)

feel_row = [row[6] for row in rows]
feel_row_unique = make_row_unique_el(feel_row)

ingredient_row = [row[7] for row in rows]
ingredient_row_unique = make_row_unique_el(ingredient_row)

texture_row = [row[11] for row in rows]
texture_row_unique = make_row_unique_el(texture_row)

aroma_row = [row[12] for row in rows]
aroma_row_unique = make_row_unique_el(aroma_row)

for skin in skin_type_row_unique:
    Skin.objects.get_or_create(name=skin)

for feel in feel_row_unique:
    Feel.objects.get_or_create(name=feel)

for ingre in ingredient_row_unique:
    Ingredient.objects.get_or_create(name=ingre)

for texture in texture_row_unique:
    Texture.objects.get_or_create(name=texture)

for aroma in aroma_row_unique:
    Aroma.objects.get_or_create(name=aroma)

for row in rows:
    product = Product.objects.get(name=row[2])
    skin_arr = row[5].split(',')
    for index in range(len(skin_arr)):
        skin_arr[index] = skin_arr[index].strip()
    
    skin_set = [Skin.objects.get(name=skin) for skin in skin_arr]
    for skin in skin_set:
        skin.products.add(product)
        skin.save()    

def set_many_to_many(rows, index, klass):
    for row in rows:
        product = Product.objects.get(name=row[2])
        field_arr = row[index].split(',')
        for idx in range(len(field_arr)):
            field_arr[idx] = field_arr[idx].strip()
        
        field_set = [klass.objects.get(name=element) for element in field_arr]

        for field in field_set:
            field.products.add(product)
            field.save()
    
set_many_to_many(rows, 6, Feel)
set_many_to_many(rows, 7, Ingredient)
set_many_to_many(rows, 11, Texture)
set_many_to_many(rows, 12, Aroma)

sub_category = SubCategory.objects.get(pk=1)
sub_category.products.add(*Product.objects.all())
