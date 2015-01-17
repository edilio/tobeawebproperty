from rest_framework import serializers
from haweb.apps.core.models import City, ZipCode, Tenant, Contract, Unit


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City


class ZipCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZipCode


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant


class ContractSerializer(serializers.ModelSerializer):
    order_on = serializers.CharField(source='tenant.order_on', read_only=True)

    class Meta:
        model = Contract


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit