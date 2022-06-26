from requests import request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from telesearch.models import Product, Channel, Category, ProductImages
from .serializers import ProductSerializer, ChannelSerializer, CategorySerializer, ImageSerializer
from rest_framework import generics
from django.db.models import Q
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, SearchHeadline, TrigramSimilarity
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@api_view(['GET'])
def getProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def postProducts(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
def getChannels(request):
    channels = Channel.objects.all()
    serializer = ChannelSerializer(channels, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def postChannels(request):
    serializer = ChannelSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
def getCategories(request):
    catgeories = Category.objects.all()
    serializer = CategorySerializer(catgeories, many=True)
    return Response(serializer.data)


class ChannelAPI(generics.RetrieveAPIView):
    lookup_field = "pk"
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer

    def put(self, request, pk):
        channel = self.get_object()
        serializer = ChannelSerializer(channel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class ChannelsAPI(APIView):
    def get(self, request):
        id = request.query_params.get('id', None)
        channels = Channel.objects.all()
        if id:
            channels = channels.filter(id=id)
        serializer = ChannelSerializer(channels, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ChannelSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


# indvisual product views


class ProductAPI(generics.RetrieveAPIView):
    lookup_field = "slug"
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # update product

    def put(self, request, slug):
        product = self.get_object()
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class ImageAPIView(generics.ListCreateAPIView):
    queryset = ProductImages.objects.all()
    serializer_class = ImageSerializer

    def list(self, request, *args, **kwargs):

        id = self.request.GET.get('id')
        print(id)
        if id:
            queryset = ProductImages.objects.filter(product=id)
            serializer_class = ImageSerializer(queryset, many=True)
            return Response(serializer_class.data)
        else:
            queryset = ProductImages.objects.all()
            serializer_class = ImageSerializer(queryset, many=True)
            return Response(serializer_class.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        success = True
        serializer = ImageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            success = False
        if success:
            # return Response(response, status=status.HTTP_201_CREATED)

            return Response({
                'status': 1,
                'message': 'Success',
                'Data': serializer.data,
            })

          # returnResponse(response,status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'status': 0,
            'message': 'Error!',
        })


# update product views

# Main Products View


class ProductsAPI(APIView):
    def get(self, request):
        s = request.GET.get('s')
        sort = request.GET.get('sort')

        category = request.GET.get('category')

        products = Product.objects.all()
        print(products.count())

       # search engine using trigram word similarity and search query s in title and description and category name
        if s:
            vector = SearchVector('title', weight='A') + SearchVector('description', weight='B') + \
                SearchVector('category__name', weight='C') + \
                SearchVector('channel__name', weight='D')
            query = SearchQuery(s)
            products = products.annotate(search=vector).filter(search=query)
            products = products.annotate(
                rank=SearchRank(vector, query)).order_by('-rank')
            products = Product.objects.annotate(similarity=TrigramSimilarity('title', s) + TrigramSimilarity('description', s) + TrigramSimilarity(
                'category__name', s) + TrigramSimilarity('channel__name', s) + TrigramSimilarity('category__related_name', s)).filter(similarity__gt=0.2).order_by('-similarity')

        if sort == 'asc':
            products = products.order_by('price')
        elif sort == 'desc':
            products = products.order_by('-price')
        elif sort == 'new':
            products = products.order_by('-created_date')
        elif sort == 'old':
            products = products.order_by('created_date')

        p = Paginator(products, 10)
        page = request.GET.get('page')
        product = p.get_page(page)

        total = products.count()

        serializer = ProductSerializer(product, many=True)
        return Response({'total': total, 'data': serializer.data, 'current_page': product.number, 'total_pages': p.num_pages, 'has_next': product.has_next(), 'has_previous': product.has_previous()})

    def post(self, request):
      # check if a product with the same title already exists
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)
