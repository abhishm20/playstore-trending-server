# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Package, SystemVariable
from core.serializers import PackageSerializer, SystemVariableSerializer, PackageAttachmentSerializer
from core.tasks import scrap_listing_task


class PackageList(APIView):
    def get(self, request):
        """
        Return a list of all packages.
        """
        package_name = self.request.query_params.get('package_name')
        if package_name:
            instance = Package.objects.get(package_name=package_name)
            data = PackageSerializer(Package.objects.get(package_name=package_name)).data
            data['attachments'] = []
            for att in instance.attachments.filter():
                data['attachments'].append(PackageAttachmentSerializer(att).data)
        else:
            queryset = Package.objects.filter(~Q(app_name__isnull=True) & ~Q(app_name=''))
            data = PackageSerializer(queryset, many=True).data
        return Response(data)


class ScrapView(APIView):
    def post(self, request):
        SystemVariable.objects.all().update(is_scraping_running=True)
        scrap_listing_task.delay()
        return Response({'message': 'Scrapping is ON.'})

    def get(self, request):
        return Response({'data': SystemVariableSerializer(SystemVariable.objects.all()[0]).data})
