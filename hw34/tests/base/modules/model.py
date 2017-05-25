from core.models import Todo


class ModelModule:
    def create_todo(self, title, **kwargs):
        params = {
            'title': title
        }
        params.update(kwargs)
        return Todo.objects.create(**params)
