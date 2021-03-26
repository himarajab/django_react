
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import generics,viewsets,filters
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
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    # display posts only created by this user
    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(author=user)

class PostDetail(generics.ListAPIView):
    # permission_classes = [PostUserWritePermission]
    # queryset= Post.objects.all()
    serializer_class = PostSerializer
    
    # what we mean by get a single object
    # def get_object(self,queryset=None,**kwargs):
    #     # get objects by it's slug instead of id
    #     item = self.kwargs.get('pk')
    #     return get_object_or_404(Post,slug=item)

    # def get_queryset(self):
    #     # filter posts based on their slug
    #     slug = self.kwargs['pk']
    #     print(slug)
    #     return Post.objects.filter(slug=slug)
    
    def get_queryset(self):
        # get parmeter for the url 
        slug = self.request.query_params.get('slug',None) 
        return Post.objects.filter(slug=slug)



# Post Search


class PostListDetailfilter(generics.ListAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter]
    # '^' Starts-with search.
    # '=' Exact matches.
    # '@' full text search only with postgres .
    search_fields = ['^slug']
