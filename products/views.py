import json, re

from django.views     import View
from django.http      import JsonResponse, HttpResponse
from django.db        import connection
from django.db.models import Prefetch

from products.models import (
    Product,
    Skin,
    Feel,
    Ingredient,
    Aroma,
    SubCategory,
    Category,
    Media,
    Texture,
)

class ProductsView(View):

    def helper_add_many_to_many(array, klass):
        names  = array
        result = [klass.objects.get(name=name) for name in names]
        return result

    def get(self, request):
        try:
            products = Product.objects.prefetch_related(
                'subcategories',
                'skin_types',
                'feels',
                'ingredients',
                'textures',
                'aromas'
            ).all()

            my_product = [{
                    "id"           : product.pk,
                    "name"         : product.name,
                    "category"     : product.subcategories.all()[0].category.name,
                    "subcategories": [subcat.name for subcat in product.subcategories.all()],
                    "size"         : product.size,
                    "dosage"       : product.dosage,
                    "description"  : product.description,
                    "manual"       : product.manual,
                    "price"        : product.price,
                    "skin_types"   : [skin.name for skin in product.skin_types.all()],
                    "feels"        : [feel.name for feel in product.feels.all()],
                    "ingredients"  : [ingredient.name for ingredient in product.ingredients.all()],
                    "textures"     : [texture.name for texture in product.textures.all()],
                    "aromas"       : [aroma.name for aroma in product.aromas.all()],
                    "media"        : [f"{media.url}::{media.media_type}" for media in product.media.all()],
                } for product in products]

            return JsonResponse({"products": my_product}, status=200)
        except:
            return HttpResponse("BAD_REQUEST", status=404)
        
    def post(self, request):
        data        = json.loads(request.body)
        dosage      = data.get('dosage', None)
        skin_types  = data.get('skin_types', None)
        feels       = data.get('feels', None)
        ingredients = data.get('ingredients', None)
        textures    = data.get('textures', None)
        aromas      = data.get('aromas', None)
        manual      = data.get('manual', None)

        try:
            name          = data['name']
            category      = data['category']
            subcategories = data['subcategories']
            size          = data['size']
            description   = data['description']
            price         = data['price']
            media_urls    = data['media']

            if Product.objects.filter(name=name).exists():
                return HttpResponse("ALREADY_EXIST", status=400)

            product = Product.objects.get_or_create(
                name        = name, 
                size        = size, 
                price       = price, 
                description = description,
                dosage      = dosage,
                manual      = manual
                )[0]
            
            subcategory_objs = helper_add_many_to_many(subcategories, SubCategory)
            skin_objs        = helper_add_many_to_many(skin_types, Skin)
            feel_objs        = helper_add_many_to_many(feels, Feel)
            ingredient_objs  = helper_add_many_to_many(ingredients, Ingredient)
            texture_objs     = helper_add_many_to_many(textures, Texture)
            aroma_objs       = helper_add_many_to_many(aromas, Aroma)

            product.subcategories.add(*subcategory_objs)
            product.skin_types.add(*skin_objs)
            product.feels.add(*feel_objs)
            product.ingredients.add(*ingredient_objs)
            product.textures.add(*texture_objs)
            product.aromas.add(*aroma_objs)

            url_arr = media_urls.values()
            for element in url_arr:
                temp            = element.split("::")
                url, media_type = temp[0], temp[1]
                product.media.create(url=url, media_type=media_type)

            product.save()

            subcategory_objs[0].category = Category.objects.get(name=category)

            return HttpResponse("PRODUCT_CREATED", status=201)
            
        except KeyError as e:
            return HttpResponse(e, status=400)

class ProductCategoryView(View):
    def get(self, request):
        try:
            subcategories = SubCategory.objects.prefetch_related('products').all()

            categories = [{
                    "id"           : subcategory.category.id,
                    "type"         : subcategory.category.name,
                    "subcategories": [
                        {
                            "id"         : subcategory.id,
                            "name"       : subcategory.name,
                            "productList": [{
                    "id"      : product.pk,
                    "name"    : product.name,
                    "capacity": product.size,
                    "price"   : product.price,
                } for product in subcategory.products.all()],
                        }
                    ]
                } for subcategory in subcategories]
            
            return JsonResponse({
                "total_cat_sub_prod": [
                    Category.objects.all().count(), 
                    subcategories.count(), 
                    Product.objects.all().count()
                    ],
                "categories"        : categories
                }, status=200)
        except:
            return HttpResponse("BAD_REQUEST", status=404)

class ProductView(View):
    def get_object(self, id):
        try:
            return Product.objects.get(pk=id)
        except:
            return HttpResponse("NOT_FOUND", stauts=404)

    def get(self, request, id):
        product = self.get_object(id)

        product_info = {
            "id"           : product.pk,
            "name"         : product.name,
            "category"     : product.subcategories.all()[0].category.name,
            "subcategories": [subcat.name for subcat in product.subcategories.all()],
            "size"         : product.size,
            "dosage"       : product.dosage,
            "description"  : product.description,
            "manual"       : product.manual,
            "price"        : product.price,
            "skin_types"   : [skin.name for skin in product.skin_types.all()],
            "feels"        : [feel.name for feel in product.feels.all()],
            "ingredients"  : [ingredient.name for ingredient in product.ingredients.all()],
            "textures"     : [texture.name for texture in product.textures.all()],
            "aromas"       : [aroma.name for aroma in product.aromas.all()],
            "media"        : [f"{media.url}::{media.media_type}" for media in product.media.all()],
        }

        return JsonResponse({"product":product_info}, status=200)
        
    def patch(self, request, id):
        data    = json.loads(request.body)
        product = self.get_object(id)

        try:
            media      = data['media']
            pattern    = re.compile('::')
            media_objs = product.media.all()
            
            for index in range(len(media)):
                if media[index]:
                    seperator                    = pattern.search(media[index]).span()
                    url, media_type              = media[index][:seperator[0]], media[index][seperator[1]:]
                    if index < len(media_objs):
                        media_obj            = media_objs[index]
                        media_obj.url        = url
                        media_obj.media_type = media_type
                        media_obj.save()
                    else:
                        Media.objects.get_or_create(url=url, media_type=media_type, products=product)
                else:
                    return HttpResponse("EMPTY_NO_ALLOWED", status=400)
                
            return HttpResponse("SUCCESSFULLY_UPDATED", status=200)
        
        except KeyError as e:
            return HttpResponse(e, status=400)
        
    def delete(self, request, id):
        product = self.get_object(id)
        product.delete()
        
        return HttpResponse("SUCCSSFULLY_DELETED", status=204)

class SkinQueryString(View):
    def get(self, request):
        try:
            data = [value for value in request.GET.values()]
            
            products = [product for product in Product.objects.prefetch_related(Prefetch(
                    'skin_types', queryset=Skin.objects.filter(name__in=data))) if product.skin_types.all()]

            result = [{"id":product.id, "name":product.name} for product in products]    

            return JsonResponse({"products": result}, status=200)
        except KeyError as e:
            return HttpResponse(e, status=400)    