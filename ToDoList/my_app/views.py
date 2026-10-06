from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from json import loads
from .forms import TaskForm, TagForm
from .models import Task, Tag

#GET /tasks/
@method_decorator(csrf_exempt, name='dispatch')
class TaskListView(View):
    def get(self, request):
        tasks = Task.objects.all()
        task_list = []
        for task in tasks:
            task_list.append({
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'is_done': task.is_done,
                'performer_id': task.performer_id.username if task.performer_id else None,
            })
        obj = {'data': task_list}
        return JsonResponse(obj)

    #POST /tasks/
    def post(self, request):
        raw_json = request.body
        new_data = loads(raw_json)
        form = TaskForm(new_data)
        if form.is_valid():
            form.save()
            return self.get(request)
        else:
            return JsonResponse(
                {'status': 'error', 'code': 400, 'errors': form.errors},
                status=400
            )

#GET /tasks/<int:pk>/
@method_decorator(csrf_exempt, name='dispatch')
class TaskDetailView(View):
    def get(self, request, pk):
        obj = get_object_or_404(Task, pk=pk)
        data = {
            'id': obj.id,
            'title': obj.title,
            'description': obj.description,
            'is_done': obj.is_done,
            'performer_id': obj.performer_id.username if obj.performer_id else None,
            'tags': [tag.name for tag in obj.tags.all()],
        }
        return JsonResponse({'data': data})

    #PUT /tasks/<int:pk>/
    def put(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        dict_from_request = loads(request.body)
        form = TaskForm(dict_from_request, instance=task)
        if form.is_valid():
            form.save()
            return self.get(request, pk)
        else:
            return JsonResponse(
                {'status': 'error', 'code': 400, 'errors': form.errors},
                status=400
            )
    
    #PATCH /tasks/<int:pk>/
    def patch(self, request, pk):
        obj = get_object_or_404(Task, pk=pk)
        data = loads(request.body)
        if 'title' in data:
            obj.title = data['title']
        if 'description' in data:
            obj.description = data['description']
        if 'is_done' in data:
            obj.is_done = data['is_done']
        obj.save()
        return self.get(request, pk)

    #DELETE /tasks/<int:pk>/
    def delete(self, request, pk):
        obj = get_object_or_404(Task, pk=pk)
        obj.delete()
        return JsonResponse({'status': 'deleted'})

#GET /tasks/undone/
class UndoneTaskListView(View):
    def get(self, request):
        tasks = Task.objects.filter(is_done=False)
        data = [
            {'id': t.id, 'title': t.title, 'is_done': t.is_done}
            for t in tasks
        ]
        return JsonResponse({'data': data})

#GET /tasks/by-tag/<int:tag_id>/
class TasksByTagView(View):
    def get(self, request, tag_id):
        tag = get_object_or_404(Tag, pk=tag_id)
        tasks = tag.tasks.all()
        data = [
            {'id': t.id, 'title': t.title, 'is_done': t.is_done}
            for t in tasks
        ]
        return JsonResponse({'tag': tag.name, 'data': data})

#GET /tags/
@method_decorator(csrf_exempt, name='dispatch')
class TagListView(View):
    def get(self, request):
        tags = Tag.objects.all()
        tag_list = []
        for tag in tags:
            tag_list.append({
                'id': tag.id,
                'name': tag.name,
            })
        obj = {'data': tag_list}
        return JsonResponse(obj)

    #POST /tags/
    def post(self, request):
        raw_json = request.body
        new_data = loads(raw_json)
        form = TagForm(new_data)
        if form.is_valid():
            form.save()
            return self.get(request)
        else:
            return JsonResponse(
                {'status': 'error', 'code': 400, 'errors': form.errors},
                status=400
            )

#GET /tags/<int:pk>/
@method_decorator(csrf_exempt, name='dispatch')
class TagDetailView(View):
    def get(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        data = {'id': tag.id, 'name': tag.name}
        return JsonResponse({'data': data})

    #PUT /tags/<int:pk>/
    def put(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        dict_from_request = loads(request.body)
        form = TagForm(dict_from_request, instance=tag)
        if form.is_valid():
            form.save()
            return self.get(request, pk)
        else:
            return JsonResponse(
                {'status': 'error', 'code': 400, 'errors': form.errors},
                status=400
            )

    #PATCH /tags/<int:pk>/
    def patch(self, request, pk):
        obj = get_object_or_404(Tag, pk=pk)
        data = loads(request.body)
        if 'name' in data:
            obj.name = data['name']
        obj.save()
        return self.get(request, pk)
    
    #DELETE /tags/<int:pk>/
    def delete(self, request, pk):
        obj = get_object_or_404(Task, pk=pk)
        obj.delete()
        return JsonResponse({'status': 'deleted'})










        


