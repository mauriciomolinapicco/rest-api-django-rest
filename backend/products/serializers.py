from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Product
from . import validators

class ProductSerializer(serializers.ModelSerializer):
    my_discount = serializers.SerializerMethodField(read_only=True)
    url = serializers.SerializerMethodField(read_only=True)
    email = serializers.EmailField(write_only=True)
    title = serializers.CharField(validators=[validators.validate_title_no_example, 
                                              validators.unique_product_title])
    
    # basically a copy of the title but with other reference. I can play around and modify it
    name = serializers.CharField(source='title',read_only=True) 

    class Meta:
        model = Product
        fields = [
            'url',
            'pk',
            'name',
            'email',
            'title',
            'content',
            'price',
            'sale_price',
            'my_discount',
        ]

    """lo paso a validators.py"""
    # def validate_title(self, value):
    #     request = self.context.get('request')
    #     user = request.user
    #     qs = Product.objects.filter(user=user, title__iexact=value) #valido que sea del mismo usuario
    #     if qs.exists():
    #         raise serializers.ValidationError(f"{value} is already a product name")
    #         #el producto no se crea cuando salta este error
    #     return value

    #overwriting the default method to handle the email
    def create(self, validated_data):
        # By default, DRF does this when i POST data.
        # return Product.objects.create(**validated_data)
        email = validated_data.pop('email')
        obj = super().create(validated_data)
        print(email, obj)
        return obj
    

    def update(self, instance, validated_data):
        email = validated_data.pop('email')
        #i pop the email out because it doesnt belong as an atribute, it is a write only that DOESNT gets saved
        return super().update(instance, validated_data)
    

    def get_my_discount(self, obj):
        if not hasattr(obj, 'id'): # si obj no tiene el atributo id
            return None
        if not isinstance(obj, Product):
            return None
        return obj.get_discount()

    def get_url(self, obj):
        # forma manual y errada de hacerlo:
        # return f"/api/products/{obj.pk}"
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("product-detail", kwargs={"pk":obj.pk}, request=request)
        #now if i change my url i dont have to manually update


class SecondaryProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'title',
            'content',
            'price',
            'sale_price',
        ]