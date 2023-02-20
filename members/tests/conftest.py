# import pytest
# from django.contrib.auth import get_user_model
# from members.models import User


# @pytest.fixture
# def user_data():
# 	# return {'email': 'user_email', 'name': 'user_name', 'password': 'user_pass543'}
# 	return {'username':'username', 'email': 'test@gmail.com', 'first_name': 'first_name', 'last_name':'last_name', 'state':'New York', 'city':'South Richmond Hill',
# 	 'password': 'user_pass543'}


# @pytest.fixture
# def create_test_user(user_data):
# 	user_model = get_user_model(User)
# 	test_user = user_model.objects.create_user(**user_data)
# 	test_user.set_password(user_data.get('password'))
# 	return test_user


# @pytest.fixture
# def authenticated_user(client, user_data):
# 	user_model = get_user_model()
# 	test_user = user_model.objects.create_user(**user_data)
# 	test_user.set_password(user_data.get('password'))
# 	test_user.save()
# 	client.login(**user_data)
# 	return test_user
