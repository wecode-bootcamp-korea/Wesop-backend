import json

from django.views   import View
from django.http    import JsonResponse, HttpResponse

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
                            

class ProductListView(View):
    def get(self, request):
        try:
            products = Product.objects.all()

            my_product = []
            for product in products:

                subcategories    = product.subcategories.all()
                subcategory_info = {f"subcategory_{i}": subcat.name for i, subcat in enumerate(subcategories)}
                
                if subcategories:
                    category = subcategories[0].category.name

                skin_types = product.skin_types.all()
                skin_info  = {f"type_{i}": skin.name for i, skin in enumerate(skin_types)}

                feels     = product.feels.all()
                feel_info = {f"feel_{i}": feel.name for i, feel in enumerate(feels)}
                
                ingredients     = product.ingredients.all()
                ingredient_info = {f"ingredient_{i}": ingredient.name for i, ingredient in enumerate(ingredients)}
                
                textures     = product.textures.all()
                texture_info = {f"texture_{i}": texture.name for i, texture in enumerate(textures)}
                
                aromas     = product.aromas.all()
                aroma_info = {f"aroma_{i}": aroma.name for i, aroma in enumerate(aromas)}
                
                media      = product.media.all()
                media_info = {f"url_{i}": f"{media.url}::{media.media_type}" for i, media in enumerate(media)}

                product_info = {
                    "id"           : product.pk,
                    "name"         : product.name,
                    "category"     : category,
                    "subcategories": subcategory_info,
                    "size"         : product.size,
                    "dosage"       : product.dosage,
                    "description"  : product.description,
                    "manual"       : product.manual,
                    "price"        : product.price,
                    "skin_types"   : skin_info,
                    "feels"        : feel_info,
                    "ingredients"  : ingredient_info,
                    "textures"     : texture_info,
                    "aromas"       : aroma_info,
                    "media"        : media_info,
                }
                my_product.append(product_info)

            return JsonResponse({
                "products": my_product
            }, status=200)

        except:
            return HttpResponse("BAD_REQUEST", status=404)

class ProductNavView(View):
    def get(self, request):
        try:
            subcategories = SubCategory.objects.all()
            categories = []
        
            for subcategory in subcategories:
                products = subcategory.products.all()

                product_list = [{
                    "id": product.pk,
                    "name": product.name,
                    "capacity": product.size,
                    "price": product.price,
                } for product in products]

                category = subcategory.category
                

                product_info = {
                    "id": category.id,
                    "type": category.name,
                    "subcategories": [
                        {
                            "id":subcategory.id,
                            "name":subcategory.name,
                            "productList": product_list,
                        }
                    ]
                }
                categories.append(product_info)
            
            return JsonResponse({
            "categories": categories
        }, status=200)

        except:
            return HttpResponse("BAD_REQUEST", status=404)


            
            # products = Product.objects.all()

            # categories = []
            # for product in products:

            #     subcategories    = product.subcategories.all()
            #     subcategory_info = {f"subcategory_{i}": subcat.name for i, subcat in enumerate(subcategories)}
                
            #     if subcategories:
            #         category = subcategories[0].category.name

            #     skin_types = product.skin_types.all()
            #     skin_info  = {f"type_{i}": skin.name for i, skin in enumerate(skin_types)}

            #     feels     = product.feels.all()
            #     feel_info = {f"feel_{i}": feel.name for i, feel in enumerate(feels)}
                
            #     ingredients     = product.ingredients.all()
            #     ingredient_info = {f"ingredient_{i}": ingredient.name for i, ingredient in enumerate(ingredients)}
                
            #     textures     = product.textures.all()
            #     texture_info = {f"texture_{i}": texture.name for i, texture in enumerate(textures)}
                
            #     aromas     = product.aromas.all()
            #     aroma_info = {f"aroma_{i}": aroma.name for i, aroma in enumerate(aromas)}
                
            #     media      = product.media.all()
            #     media_info = {f"url_{i}": f"{media.url}::{media.media_type}" for i, media in enumerate(media)}

                
                    

          

class ProductRetrieveView(View):
    def get_object(self, id):
        try:
            return Product.objects.get(pk=id)
        except:
            return HttpResponse("NOT_FOUND", stauts=404)

    def get(self, request, id):
        product = self.get_object(id)

        subcategories    = product.subcategories.all()
        subcategory_info = {f"subcategory_{i}": subcat.name for i,subcat in enumerate(subcategories)}

        category = subcategories[0].category.name
        
        skin_types = product.skin_types.all()
        skin_info  = {f"type_{i}": skin.name for i, skin in enumerate(skin_types)}

        feels     = product.feels.all()
        feel_info = {f"feel_{i}": feel.name for i, feel in enumerate(feels)}
        
        ingredients     = product.ingredients.all()
        ingredient_info = {f"ingredient_{i}": ingredient.name for i, ingredient in enumerate(ingredients)}
        
        textures     = product.textures.all()
        texture_info = {f"texture_{i}": texture.name for i, texture in enumerate(textures)}
        
        aromas     = product.aromas.all()
        aroma_info = {f"aroma_{i}": aroma.name for i, aroma in enumerate(aromas)}

        media      = product.media.all()
        media_info = {f"url_{i}": f"{media.url}::{media.media_type}" for i, media in enumerate(media)}

        product_info = {
            "id"           : product.pk,
            "name"         : product.name,
            "category"     : category,
            "subcategories": subcategory_info,
            "size"         : product.size,
            "dosage"       : product.dosage,
            "description"  : product.description,
            "manual"       : product.manual,
            "price"        : product.price,
            "skin_types"   : skin_info,
            "feels"        : feel_info,
            "ingredients"  : ingredient_info,
            "textures"     : texture_info,
            "aromas"       : aroma_info,
            "media"        : media_info,
        }

        return JsonResponse({
            "product":product_info
        }, status=200)

def helper_add_many_to_many(dic, klass):
    names = dic.values()
    result = []
    for name in names:
        obj_klass = klass.objects.get(name=name)
        result.append(obj_klass)
    
    return result

class ProductCreateView(View):
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
                )
            
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
        


# class ProductDetailView(View):
#     def get_object(self, id):
#         try:
#             return product.objects.get(pk=id)
#         except:
#             return HttpResponse("NOT_FOUND", status=404)
    
#     def get(self, request, id):
#         data = json.loads(request.body)
#         try:
            
#             product = Product.objects.filter(pk=id, )
           

