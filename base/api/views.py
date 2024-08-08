from django.http import JsonResponse
from ..models import Post

def routes(request):
    routes = [
        'GET /api/posts',
        'GET /api/post/:id'
    ]
    return JsonResponse(routes, safe=False)

def posts(request):
    posts = Post.objects.all()
    posts_dict = []
    for p in posts:
        posts_dict.append({
            'title': p.title,
            'text': p.text,
            'id': p.id
        })

    return JsonResponse(posts_dict, safe=False)

def post(request, id):
    post = Post.objects.get(id=id)
    post_dict = {
            'title': post.title,
            'text': post.text,
            'id': post.id
    }
    return JsonResponse(post_dict, safe=False)