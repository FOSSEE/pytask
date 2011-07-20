import os
def get_file_path(instance, filename):
        if instance.task.parent:
            path='%d/%d' % (instance.task.parent.id, instance.task.id)
        return os.path.join('pytask', path, filename)
