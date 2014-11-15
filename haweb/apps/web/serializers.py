from rest_framework import serializers
from . models import Career, ResourceForm, FAQ, HelpfulLink, Content


class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career


class ResourceFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceForm


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ


class HelpfulLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpfulLink


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
