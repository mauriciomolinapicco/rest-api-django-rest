from .models import Product
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# def validate_title(value):
#     qs = Product.objects.filter(title__iexact=value)
#     if qs.exists():
#         raise serializers.ValidationError(f"{value} is already a product name")
#         #el producto no se crea cuando salta este error
#     return value

def validate_title_no_example(value):
    if "example" in value.lower():
        raise serializers.ValidationError(f"Example is not allowed")
    return value

unique_product_title = UniqueValidator(queryset=Product.objects.all())
