
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework import permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import generics,viewsets,filters,status
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from blog.models import Post
from .serializers import PostSerializer
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated, IsAuthenticatedOrReadOnly, BasePermission, IsAdminUser, DjangoModelPermissions


class PostUserWritePermission(BasePermission):
    message = 'Editing posts is restricted to the author only.'

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user




# class PostList(generics.ListCreateAPIView):
#     permission_classes = [IsAuthenticated]
#     queryset = Post.postobjects.all()
#     serializer_class = PostSerializer


# class PostDetail(generics.RetrieveUpdateDestroyAPIView, PostUserWritePermission):
#     permission_classes = [PostUserWritePermission]
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer



# class PostList(viewsets.ViewSet):
#     permission_classes = [IsAuthenticated]
#     queryset = Post.postobjects.all()

#     def list(self,request):
#         serializer_class = PostSerializer(self.queryset,many=True)
#         return Response(serializer_class.data)

#     def retrieve(self,request,pk=None):
#         post = get_object_or_404(self.queryset,pk=pk)
#         serializer_class = PostSerializer(post)
#         return Response(serializer_class.data)


class PostList(generics.ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

class PostDetail(generics.RetrieveAPIView):
  
    serializer_class = PostSerializer

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')
        return get_object_or_404(Post, slug=item)



# Post Search

class PostListDetailfilter(generics.ListAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter]
    # '^' Starts-with search.
    # '=' Exact matches.
    # '@' full text search only with postgres .
    search_fields = ['^slug']


# post admin
# class CreatePost(generics.CreateAPIView):
#     serializer_class = PostSerializer
#     queryset = Post.objects.all()
#     permission_classes = [permissions.IsAuthenticated]

class CreatePost(APIView):
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request, format=None):
        print(request.data)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
# collect the data first to be able to edit it 
class AdminPostDetail(generics.RetrieveAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]

class EditPost(generics.UpdateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]

class DeletePost(generics.RetrieveDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]
