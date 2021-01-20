from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'categories'
    
    def __str__(self):
        return self.name
    
class SubCategory(models.Model):
    name     = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="sub_categories")

    class Meta:
        db_table = 'sub_categories'
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name           = models.CharField(max_length=100)
    size           = models.CharField(max_length=100)
    dosage         = models.CharField(max_length=100)
    description    = models.TextField()
    manual         = models.TextField(null=True)
    price          = models.DecimalField(max_digits=10, decimal_places=2)
    subcategories  = models.ManyToManyField(SubCategory, related_name="products")
    skin_types     = models.ManyToManyField("Skin", related_name="products", null=True)
    feels          = models.ManyToManyField("Feel", related_name="products", null=True)
    ingredients    = models.ManyToManyField("Ingredient", related_name="products", null=True)
    textures       = models.ManyToManyField("Texture", related_name="products", null=True)
    aromas         = models.ManyToManyField("Aroma", related_name="products", null=True)
    
    class Meta:
        db_table = 'products'
    
    def __str__(self):
        return self.name

class Media(models.Model):
    url        = models.URLField(max_length=200, null = True)
    media_type = models.CharField(max_length=50, null=True)
    products   = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="media")
      
    class Meta:
        db_table = 'media'
    
    def __str__(self):
        return f"media_{self.pk}"

class Skin(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'skin'
    
    def __str__(self):
        return self.name

class Feel(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'feels'
    
    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'ingredients'
    
    def __str__(self):
        return self.name

class Texture(models.Model):
    name = models.CharField(max_length=100)
 
    class Meta:
        db_table = 'textures'
    
    def __str__(self):
        return self.name
    
class Aroma(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'aromas'
    
    def __str__(self):
        return self.name

