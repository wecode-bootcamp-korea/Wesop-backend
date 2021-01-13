from django.db import models


class Order(models.Model):
    user     = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='orders')
    state    = models.ForeignKey('State',     on_delete=models.CASCADE, related_name='orders')
    checkout = models.ForeignKey('CheckOut',  on_delete=models.CASCADE, related_name='orders')

    class Meta:
        db_table = 'orders'
    
    def __str__(self):
        return f'order_{self.pk}'


class OrderProduct(models.Model):
    
    order    = models.ForeignKey(Order,              on_delete=models.CASCADE, related_name='order_prouducts') 
    product  = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='products')
    quantity = models.IntegerField()

    class Meta:
        db_table = 'order_products'
    
    def __str__(self):
        return f'{self.product.name}_order'

class State(models.Model):

    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'states'
    
    def __str__(self):
        return self.name

class CheckOut(models.Model):

    class Meta:
        db_table = 'checkouts'
    
    def __str__(self):
        return f'checkout_{self.pk}'
