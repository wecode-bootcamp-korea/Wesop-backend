from django.views   import View
from django.http    import JsonResponse, HttpResponse

from products.models import Product

class ProductListView(View):
    def get(self, request):
        try:
            products = Product.objects.all()

            my_product = []
            for product in products:
                subcategories    = product.subcategories.all()
                subcategory_info = {f"subcategory_{i}": subcat.name for i,subcat in enumerate(subcategories)}
                
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

                product_info = {
                    "id"           : product.pk,
                    "name"         : product.name,
                    "size"         : product.size,
                    "dosage"       : product.dosage,
                    "description"  : product.description,
                    "manual"       : product.manual,
                    "price"        : product.price,
                    "subcategories": subcategory_info,
                    "skin_types"   : skin_info,
                    "feels"        : feel_info,
                    "ingredients"  : ingredient_info,
                    "textures"     : texture_info,
                    "aromas"       : aroma_info,
                }
                my_product.append(product_info)

            return JsonResponse({
                "products": my_product
            }, status=200)

        except:
            return HttpResponse("BAD_REQUEST", status=404)

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

        product_info = {
            "id"           : product.pk,
            "name"         : product.name,
            "size"         : product.size,
            "dosage"       : product.dosage,
            "description"  : product.description,
            "manual"       : product.manual,
            "price"        : product.price,
            "subcategories": subcategory_info,
            "skin_types"   : skin_info,
            "feels"        : feel_info,
            "ingredients"  : ingredient_info,
            "textures"     : texture_info,
            "aromas"       : aroma_info,
        }

        return JsonResponse({
            "product":product_info
        }, status=200)
            
    
    
        
        