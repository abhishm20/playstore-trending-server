# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from rest_framework import serializers

from core.models import Package, PackageAttachment, SystemVariable


class SystemVariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemVariable
        fields = "__all__"


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = "__all__"


class PackageAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageAttachment
        fields = "__all__"
