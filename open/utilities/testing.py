import uuid


def generate_random_uuid_as_string():
    generated_uuid = uuid.uuid4()
    return generated_uuid.__str__()


def get_instance_uuid_as_string(instance):
    # typing this always is super annoying
    return instance.uuid.__str__()
