from rest_framework.serializers import ModelSerializer


class BaseCreateUpdateSerializer(ModelSerializer):
    def create(self, validated_data):
        create_model = self.Meta.model
        obj = create_model.objects.create(**validated_data)
        return obj

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance
