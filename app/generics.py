__author__ = 'chitrankdixit'

class ModelViewSet(object):
    """
        This is the model viewset just like Django rest framework
    """
    queryset = None
    serializer = None
    pagination = None


    def get_object(self):
        pass

    def get_queryset(self):
        pass

    def list(self):
        pass

    def create(self):
        pass

    def update(self):
        pass

    def partial_update(self):
        pass

    def delete(self):
        pass

    def retrieve(self, id):
        pass



