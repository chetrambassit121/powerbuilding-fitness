import pytest
from django import urls
from django.contrib.auth import get_user_model


'''
python test command .... python manage.py test
coverage command .... coverage run manage.py test
coverage report command .... coverage report
coverage run --source='social' manage.py test && coverage report && coverage html
'''

'''pytest'''
pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("param", [("post-list"),])
def test_render_views(client, param):
    temp_url = urls.reverse(param)
    resp = client.get(temp_url)
    assert resp.status_code == 200
