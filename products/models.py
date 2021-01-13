from django.db import models

class Category(models.Model):
    name  = models.CharField(max_length=20)

    class Meta:
        db_table = 'categories'
    
    def __str__(self):
        return self.name
    
class SubCategory(models.Model):
    name     = models.CharField(max_length=20)
    category = models.ForeignKey(Category_type, on_delete=models.CASCADE, related_name="sub_categories")

    class Meta:
        db_table = 'sub_categories'
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name        = models.CharField(max_length=20)
    size        = models.CharField(max_length=20)
    dosage      = models.CharField(max_length=20)
    description = models.TextField()
    manual      = models.TextField()
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    subcategories  = models.ManyToManyField(SubCategory, related_name="products")
    
    class Meta:
        db_table = 'products'
    
    def __str__(self):
        return self.name

class Media(models.Model):
    image_url  = models.CharField(max_length=200)
    video_url  = models.CharField(max_length=200)
    products   = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="media")
    
      
    class Meta:
        db_table = 'media'
    
    def __str__(self):
        return f"media_{self.pk}"

class Skin(models.Model):
    name      = models.CharField(max_length=20)
    products  = models.ManyToManyField(Product, related_name="skin_types")
    
    class Meta:
        db_table = 'skin_types'
    
    def __str__(self):
        return self.name

class Feel(models.Model):
    name     = models.CharField(max_length=20)
    products = models.ManyToManyField(Product, related_name="feels")

    class Meta:
        db_table = 'feels'
    
    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name     = models.CharField(max_length=20)
    products = models.ManyToManyField(Product, related_name="ingredients")

    class Meta:
        db_table = 'ingredients'
    
    def __str__(self):
        return self.name

class Texture(models.Model):
    name     = models.CharField(max_length=20)
    products = models.ManyToManyField(Product, related_name="textures")

    class Meta:
        db_table = 'textures'
    
    def __str__(self):
        return self.name
    
class Aroma(models.Model):
    name     = models.CharField(max_length=20)
    products = models.ManyToManyField(Product, related_name="aromas")

    class Meta:
        db_table = 'aromas'
    
    def __str__(self):
        return self.name

