from django.http import JsonResponse
import json

def api_home(request, *args, **kwargs):
    print(request)
    body = request.body
    data = {}
    try:
        data = json.loads(body)
    except Exception as e:
        pass
    
    data['params'] = dict(request.GET)
    data['headers'] = dict(request.headers)
    data['content-type'] = request.content_type
    return JsonResponse(data)