def blog_upload_directory(instance, filename):
    return f'blogs/{instance.id}/{instance.created_at}/'

def call_upload_diretory(instance, filename):
    return f'calls/{instance.id}/{instance.created_at}'

def news_upload_diretory(instance, filename):
    return f'news/{instance.id}/{instance.created_at}'