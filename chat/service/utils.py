import os
def file_upload_path(instance, filename):
    if filename.endswith(('.mp4', '.avi', '.mov')):
        return os.path.join('root', 'videos', filename)
    return os.path.join('root', 'pictures', filename)