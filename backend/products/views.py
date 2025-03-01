from rest_framework import generics, mixins
from .models import Product
from .serializers import ProductSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None 
        if content is None:
            content = title
        serializer.save(content=content)
        

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = 'pk'
     

class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title



class ProductDestroyAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    
    def perform_destroy(self, instance):
        super().perform_destroy(instance)


# SAME BUT IN FUNCTION BASED VIEW
@api_view(['GET', 'POST'])
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method
    if method == 'GET':
        if pk is not None:
            # detail view
            obj = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(obj, many=False).data
            return Response(data)
        else:
            #list view
            qs = Product.objects.all()
            data = ProductSerializer(qs, many=True).data
            return Response(data)
    
    if method == 'POST':
        #create method
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content') or None
            if content is None:
                content = title
            serializer.save(content=content)
            return Response(serializer.data)


#ALL IN ONE VIEW
class ProductMixinView(mixins.ListModelMixin, 
                       mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       generics.GenericAPIView
                       ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get(self, request, pk=None,*args, **kwargs):
        print(args, kwargs, pk)
        if pk is not None: 
            # si hay un pk significa que es get para un detail y no para la lista de todos
            return self.retrieve(request, *args, **kwargs)
        
        return self.list(request, *args, **kwargs) 
        #usar mixins me da acceso a estas funciones .list y .retrieve
    

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = 'I can do a bunch of cool stuff and im getting good!'
        serializer.save(content=content)



#just for theretical purpouse
class ProductListAPIView(generics.ListAPIView):
    ''' Not gonna use this one. It is included in ListCreate'''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer