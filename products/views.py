from django.views    import View
from django.http     import JsonResponse

from products.models import (
    Category,
    SubCategory,
    Product,
    Media,
    Skin,
    Feel,
    Ingredient,
    Texture,
    Aroma,
)

class ProductListView(View):
    def get(self, request):
        products = Product.objects.all()
        product_list = [{
            'id'            : product.id,
            'name'          : product.name,
            'category'      : [subcategory.category.name for subcategory in product.subcategories.all()],
            'subcatergory'  : [subcategory.name for subcategory in product.subcategories.all()],
            'size'          : product.size,
            'dosage'        : product.dosage,
            'manual'        : product.manual,
            'price'         : product.price,
            'skin_types'    : [skin.name for skin in product.skin_types.all()],
            'ingredients'   : [ingredient.name for ingredient in product.ingredients.all()],
            'textures'      : [texture.name for texture in product.textures.all()],
            'aromas'        : [aroma.name for aroma in product.aromas.all()],
            'media'         : [{'url' : media.url,
                                'type': media.media_type} for media in product.media.all()]
            
        }for product in products]
        return JsonResponse({'products': product_list}, status=200)

class ProductView(View):
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        product_data={
            'id'            : product.id,
            'name'          : product.name,
            'category'      : [subcategory.category.name for subcategory in product.subcategories.all()],
            'subcategories' : [subcategory.name for subcategory in product.subcategories.all()],
            'size'          : product.size,
            'dosage'        : product.dosage,
            'description'   : product.description,
            'manual'        : product.manual,
            'price'         : product.price,
            'skin_types'    : [skin.name for skin in product.skin_types.all()],
            'ingredients'   : [ingredient.name for ingredient in product.ingredients.all()],
            'textures'      : [texture.name for texture in product.textures.all()],
            'aromas'        : [aroma.name for aroma in product.aromas.all()],
            'media'         : [{'url'  : media.url,
                                'type' : media.media_type} for media in product.media.all()]
        }
        return JsonResponse({'products':product_data}, status=200)
