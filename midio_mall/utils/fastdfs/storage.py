from django.core.files.storage import Storage
class MyStorage(Storage):

    def open(self,name,mode='rb'):
        pass

    def save(self, name, content, max_length=None):
        pass
    def url(self,name):
        return "http://192.168.44.130:8888/" + name