from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from json import loads
from .forms import TaskForm, TagForm
from .models import Task, Tag

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
    
    def patch(self, request, pk):
        obj = get_object_or_404(Task, pk)
        dict_from_request = loads(request.body)
        form = TaskForm(initial=obj)
        if form.is_valid() and form.has_changed():
          form.save()
        return self.get(request, pk)

    def delete(self, request, pk):
        obj = get_object_or_404(Task, pk)
        obj.delete()
        return JsonResponse({'status': 'deleted'})


class UndoneTaskListView(View):
    def get(self, request):
        tasks = Task.objects.filter(is_done=False)
        data = [
            {'id': t.id, 'title': t.title, 'is_done': t.is_done}
            for t in tasks
        ]
        return JsonResponse({'data': data})


class TasksByTagView(View):
    def get(self, request, tag_id):
        tag = get_object_or_404(Tag, pk=tag_id)
        tasks = tag.tasks.all()
        data = [
            {'id': t.id, 'title': t.title, 'is_done': t.is_done}
            for t in tasks
        ]
        return JsonResponse({'tag': tag.name, 'data': data})


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

@method_decorator(csrf_exempt, name='dispatch')
class TagDetailView(View):
    def get(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        data = {'id': tag.id, 'name': tag.name}
        return JsonResponse({'data': data})

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

        def patch(self, request, pk):
            obj = get_object_or_404(Tag, pk)
            dict_from_request = loads(request.body)
            form = TagForm(initial=obj)
            if form.is_valid() and form.has_changed():
              form.save()
            return self.get(request, pk)


        def delete(self, request, pk):
            obj = get_object_or_404(Tag, pk)
            obj.delete()
            return JsonResponse({'status': 'deleted'})










        


