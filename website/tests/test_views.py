from website import views
from django import urls
import pytest
from .test_models import Product, Category
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.sessions.models import Session
from bs4 import BeautifulSoup


@pytest.mark.django_db
class TestViews:
    @pytest.fixture
    def setup(self, client):
        """ Init test data from models in test database """
        print("INIT DATA")

        # categories
        self.breakfast = Category.objects.create(name="breakfast")
        self.snacks = Category.objects.create(name="snacks")
        self.chocolate = Category.objects.create(name="chocolate")

        # products
        self.snicker = Product.objects.create(name="snicker", nutriscore="e")
        self.nutella = Product.objects.create(
            name="Nutella",
            desc="Sucre, huile de palme, noisettes 13%, cacao maigre 7,4%, "
                 "lait écrémé en poudre 6,6%, lactoserum en poudre, "
                 "émulsifiants :  lécithines [soja], vanilline",
            photo="https://static.openfoodfacts.org/images/products/301/762/042/9484/front_fr"
                  ".204.400.jpg",
            API_link="https://fr.openfoodfacts.org/produit/3017620429484/nutella-ferrero",
            nutriscore="e", nutrient_100g="salt_100g:0.114:high, "
                                          "fat_100g:31.6:high, "
                                          "sugars_100g:56.8:high, "
                                          "saturated-fat_100g:11:high")

        self.nutella_sub = Product.objects.create(
            name="Nutella_sub",
            desc="Sucre de canne, pâte de _noisettes_ 16 %, huile de tournesol, _lait_ écrémé en "
                 "poudre, cacao 6,5 %, beurre de cacao, lécithine de tournesol, extrait vanille.",
            photo="https://static.openfoodfacts.org/images/products/800/150/500/5592/front_fr"
                  ".62.400.jpg",
            API_link="https://fr.openfoodfacts.org/produit/8001505005592/nocciolata-pate-a-tartiner"
                     "-au-cacao-et-noisettes-rigoni-di-asiago", nutriscore="d",
            nutrient_100g="saturated_fat_100g:6:high, "
                          "fat_100g:30:high, "
                          "salt_100g:0.13:low, "
                          "sugars_100g:51:high ")

        # pruduct-categories
        self.snicker.categories.add(self.snacks)
        self.nutella.categories.add(self.breakfast, self.chocolate)
        self.nutella_sub.categories.add(self.breakfast)

        # authenticated user
        self.user = User.objects.create_user("username", "email@mailer.com", "password123")

        # favorites for user 1
        self.nutella_sub.favorites.add(self.user)

    def test_home(self, client):
        """test homepage render as expected"""
        url = urls.reverse('home')
        resp = client.get(url)
        assert resp.status_code == 200

    def test_legal(self, client):
        """test legal page render as expected"""
        url = urls.reverse('legal')
        resp = client.get(url)
        assert resp.status_code == 200

    def test_register_page(self, client):
        """test register page render as expected"""
        url = urls.reverse('register')
        resp = client.get(url)
        assert resp.status_code == 200

    def test_search_product_detail(self, setup, client):
        """test product detail page for nutella"""
        product_id = self.nutella.id
        url = urls.reverse('website:detail', args=(product_id,))
        resp = client.get(url)
        assert resp.status_code == 200

    def test_none_product_detail(self, setup, client):
        """test product detail page for unexistant product"""
        url = urls.reverse('website:detail', args=(18,))
        resp = client.get(url)
        assert resp.status_code == 404

    def test_data_results(self, setup, rf):
        """if query search in database"""
        request = rf.get('/search/result/?q=nutella')
        resp = views.result(request)
        soup = BeautifulSoup(resp.content, 'html.parser')
        assert resp.status_code == 200
        assert soup.select('div.card')

    def test_OFF_results(self, setup, rf):
        """if query search not in database ask OFF API"""
        request = rf.get('/search/result/?q=coca')
        resp = views.result(request)
        soup = BeautifulSoup(resp.content, 'html.parser')
        assert resp.status_code == 200
        assert soup.select('div.card')

    def test_no_results(self, setup, rf):
        """error message if query search not in database, not in OFF response"""
        request = rf.get('/search/result/?q=pepito')
        resp = views.result(request)
        soup = BeautifulSoup(resp.content, 'html.parser')
        assert resp.status_code == 200
        assert soup.select('p.error')

    def test_anonymous_user_favorites_access(self, setup, rf, client):
        """favorites not visible when user not loged and redirect to login """
        url = urls.reverse('favorites')
        request = rf.get(url)
        request.user = AnonymousUser()
        resp = views.favorites(request)
        assert resp.status_code == 302
        assert resp.url == '/account/login/?next=/account/my-products/'

    def test_authenticated_user_favorites_access(self, setup, rf, client):
        client.post(urls.reverse('login'), {
            'username': "username",
            'password': "password123"
        })
        url = urls.reverse('favorites')
        response = client.get(url)
        assert response.status_code == 200

    def test_login(self, client, setup):
        """test session and redirection when user log in"""
        url = urls.reverse('login')
        resp = client.post(url, {
            'username': "username",
            'password': "password123"
        })
        # Logged in user are redirect to homepage
        assert resp.status_code == 302
        assert resp.url == urls.reverse('home')
        # Logged in users have a session created for them
        assert Session.objects.count() == 1

    def test_logout(self, client, setup):
        """test session and redirection when user log out"""
        url = urls.reverse('logout')
        resp = client.get(url)
        assert resp.status_code == 200
        # There should be no more sessions left after logging out
        assert not Session.objects.exists()

    def test_register_user(self, client):
        """redirect to login if new user is registered"""
        url = urls.reverse('register')
        resp = client.post(url, {
            'username': "toto",
            'password1': "totomp1234",
            'password2': "totomp1234",
            'email': "toto@mail.com"
        })
        # Registered user are redirect to profile
        assert resp.status_code == 302
        assert resp.url == urls.reverse('login')
        # New user added in database
        assert User.objects.get(username="toto")

    def test_authenticated_user_profile_access(self, setup, rf):
        """access profile if authenticated user is logged"""
        url = urls.reverse('profile')
        request = rf.get(url)
        request.user = self.user
        response = views.profile(request)
        assert response.status_code == 200

    def test_anonymous_user_profile_access(self, setup, rf):
        """redirect to login page if no authenticated user is logged"""
        url = urls.reverse('profile')
        request = rf.get(url)
        request.user = AnonymousUser()
        response = views.profile(request)
        assert response.status_code == 302
        assert 'account/login' in response.url




