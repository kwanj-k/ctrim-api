from django.urls import reverse,resolve

class TestUrl:

    def test_list_and_create_url(self):
        path = reverse('list')
        assert resolve(path).view_name == 'list'

    def test_detail_url(self):
        path = reverse('details',kwargs={'pk':1})
        assert resolve(path).view_name == 'details'