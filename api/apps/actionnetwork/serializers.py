from django.utils.timezone import now

from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Campaign, Person


class CampaignSerializer(serializers.ModelSerializer):
    group = serializers.CharField(source="action_group.name")
    url = serializers.SerializerMethodField()

    class Meta:
        model = Campaign
        fields = ['title', 'resource_name', 'group', 'url']

    def __init__(self, *args, **kwargs):
        # Instantiate the superclass normally

        exclude = kwargs.pop('exclude', None)

        # Instantiate the superclass normally
        super(CampaignSerializer, self).__init__(*args, **kwargs)

        if exclude is not None:
            # Drop any fields that are specified in the `exclude` argument.
            exclude = set(exclude)
            for field_name in exclude:
                self.fields.pop(field_name)
    
    def get_url(self, instance):
        request = self.context.get('request')

        if not request:
            # When use serializer in shell command hasnt request 
            return 'shell'
        
        return reverse(instance.resource_name, kwargs={"campaign_id": instance.id}, request=request)


class PersonSerializer(serializers.ModelSerializer):
    email_address = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)

    class Meta:
        model = Person
        fields = '__all__'
    
    def validate(self, data):
        if not data.get('email_address') and not data.get('phone_number'):
            raise serializers.ValidationError("email_address or phone_number is required.")
        
        return data


class ActionSerializerMixin(serializers.ModelSerializer):
    person = PersonSerializer()

    class Meta:
        exclude = ['api_response_json', 'campaign', 'created_date']

    def create(self, validated_data):
        person_data = validated_data.pop('person')
        
        ## TODO: Melhorar serialização de objetos
        # targets = validated_data.pop('targets')
        
        instance = self.Meta.model.objects.create(**validated_data, **person_data, created_date=now())

        ## TODO: Melhorar serialização de objetos
        # if hasattr(instance, 'targets') and targets:
        #     instance.targets.set(targets)

        return instance