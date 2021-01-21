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
            'description'   : product.description,
            'manual'        : product.manual,
            'price'         : product.price,
            'skin_types'    : [skin.name for skin in product.skin_types.all()],
            'feels'         : [feel.name for feel in product.feels.all()],
            'ingredients'   : [ingredient.name for ingredient in product.ingredients.all()],
            'textures'      : [texture.name for texture in product.textures.all()],
            'aromas'        : [aroma.name for aroma in product.aromas.all()],
            'media'         : [{'url' : media.url,
                                'type': media.media_type} for media in product.media.all()]
            
        }for product in products]
        return JsonResponse({'products': product_list}, status=200)

    def post(self, request):
        try:
            data          = json.loads(request.body)
            name          = data['name']
            category      = data['category']
            subcategories = data['subcategory']
            size          = data['size']
            dosage        = data['dosage']
            manual        = data.get('manual')
            description   = data['description']
            price         = data['price']
            skin_types    = data.get('skin_types')
            feels         = data.get('feels')
            ingredients   = data.get('ingrediendts')
            textures      = data.get('textures')
            aromas        = data.get('aromas')
            medias        = {'url' : data.get('media')['url'], 'type' : data.get('media')['type']}
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

        if Product.objects.filter(name=name).exists():
            return JsonResponse({'message' : 'EXIST_NAME'}, status=400)

        P1 = Product.objects.create(
            category    = category,
            name        = name,
            size        = size,
            dosage      = dosage,
            description = description,
            manual      = manual,
            price       = price
        )
        for subcategory in subcategories:
            S = SubCategory.objects.get(name=subcategory)
            P1.subcategories.add(S)
        for skin_type in skin_types:
            S1 = Skin.objects.get(name=skin_type)
            P1.skin_types.add(S1)
        for feel in feels:
            F1 = Feel.objects.get(name=feel)
            P1.feels.add(F1)
        for ingredient in ingredients:
            I1 = Ingredient.objects.get(name=ingredient)
            P1.ingredients.add(I1)
        for texture in textures:
            T1 = Texture.objects.get(name=texture)
            P1.textures.add(T1)
        for aroma in aromas:
            A1 = Aroma.objects.get(name=aroma)
            P1.aromas.add(A1)
        for media in medias:
            Media.objects.create(url=media['url'], media_type=media['type'], products_id=P1.id)

        return JsonResponse({'message' : 'CREATE_PRODUCT'}, status=200)


class ProductView(View):
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        product_data = {
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
            'feels'         : [feel.name for feel in product.feels.all()],
            'ingredients'   : [ingredient.name for ingredient in product.ingredients.all()],
            'textures'      : [texture.name for texture in product.textures.all()],
            'aromas'        : [aroma.name for aroma in product.aromas.all()],
            'media'         : [{'url'  : media.url,
                                'type' : media.media_type} for media in product.media.all()]
        }
        return JsonResponse({'products':product_data}, status=200)