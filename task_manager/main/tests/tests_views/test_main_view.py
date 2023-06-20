import pytest
from django.urls import reverse


class TestsMainPage:
    @pytest.mark.django_db
    def test_main_page_views(self, client):
        url = reverse("main")
        response = client.get(url)
        assert response.status_code == 200
