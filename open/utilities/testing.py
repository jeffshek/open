import uuid

from rest_framework.test import APIRequestFactory, force_authenticate


def generate_random_uuid_as_string():
    generated_uuid = uuid.uuid4()
    return generated_uuid.__str__()


def get_instance_uuid_as_string(instance):
    # typing this always is super annoying
    return instance.uuid.__str__()


def create_api_request_context(url, user, data):
    """
    Sometimes useful if you need to skip using an APIClient and directly test with a request

    There's an edge case where some DRF Fields think they should be required, but passes in tests, but not in production
    """
    factory = APIRequestFactory()
    request = factory.post(url, data)
    request.user = user
    force_authenticate(request, user=user)
    context = {"request": request}
    return context
