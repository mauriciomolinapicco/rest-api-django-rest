from rest_framework import generics, mixins
from .models import Product
from .serializers import ProductSerializer
from api.mixins import StaffEditorPermissionMixin

from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404


class ProductListCreateAPIView(
        StaffEditorPermissionMixin,
        generics.ListCreateAPIView
        ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # authentication_classes = [
    #     authentication.SessionAuthentication,
    #     TokenAuthentication
    #### -->> Dont need it anymore since i setted it up in settings.py 

    # dont need this since i have StaffEditorPermissionMixin
    # permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]

    def perform_create(self, serializer):
        # al email lo estoy accediendo desde el serializer pero lo podria hacer desde aca
        # email = serializer.validated_data.pop('email') 
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None 
        if content is None:
            content = title
        serializer.save(user=self.request.user, content=content)
    
    def get_queryset(self, *args, **kwargs):
        """
            Estoy filtrando por user, para cada user devuelvo el queryset de los productos 
            que tengan a este usuario asociado
            LO PUEDO ABSTRAER EN mixins.py
        """
        request = self.request
        user = self.request.user
        qs = super().get_queryset(*args, **kwargs)
        if not user.is_authenticated:
            return Product.objects.none()
        return qs.filter(user=request.user)


class ProductDetailAPIView(
            StaffEditorPermissionMixin,
            generics.RetrieveAPIView
                           ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self, *args, **kwargs):
        """
        al igual que en list create devuelvo el producto solo si el usuario es quien lo creo
        """
        request = self.request
        user = self.request.user
        qs = super().get_queryset(*args, **kwargs)
        if not user.is_authenticated:
            return Product.objects.none()
        return qs.filter(user=request.user)



class ProductUpdateAPIView(
        StaffEditorPermissionMixin,
        generics.UpdateAPIView
    ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title



class ProductDestroyAPIView(
        StaffEditorPermissionMixin,
        generics.DestroyAPIView
        ):
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
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
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


    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            content = 'Im doing really cool stuff now'
            instance.save(content=content)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



#just for theretical purpouse
class ProductListAPIView(generics.ListAPIView):
    ''' Not gonna use this one. It is included in ListCreate'''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer