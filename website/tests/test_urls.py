from django.urls import resolve, reverse


class TestUrls:

    def test_home(self):
        """test homepage"""
        path = reverse('home')
        assert resolve(path).view_name == 'home'

    def test_search_result(self):
        """test search result page"""
        path = reverse('result')
        assert resolve(path).view_name == 'result'

    def test_favorites(self):
        """test favorites page"""
        path = reverse('favorites')
        assert resolve(path).view_name == 'favorites'
