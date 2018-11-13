from django.shortcuts import render
from .models import *
from rest_framework import status, views
from rest_framework.response import Response
from .serializer import *
from django.db.utils import DatabaseError
from django.http import HttpResponse, StreamingHttpResponse
import pandas as pd
try:
    from io import BytesIO as IO # for modern python
except ImportError:
    from StringIO import StringIO as IO # for legacy python

class UploadFile(views.APIView):

    def post(self, request, **kwargs):
        try:
            file = request.data['file']
            name = request.data['name']
        except KeyError as e:
            return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        data, created = Data.objects.get_or_create(file=file, name=name)
        return Response(DataSerializer(data).data, status=status.HTTP_200_OK)

class FilterPCLPCPLasmogen(views.APIView):

    def get(self, request, **kwargs):
        try:
            data = Data.objects.filter(name='analytics_data')[0]

            # Let's do the analytics
            df = pd.read_excel(data.file, sheet_name='Raw Data')
            df.columns = [col.replace(' ', '_').lower() for col in df.columns]

            df = df.loc[df['accepted_compound_id'].str.endswith('PC') |
                        df['accepted_compound_id'].str.endswith('LPC') |
                        df['accepted_compound_id'].str.endswith('plasmalogen')]

            excel_file = IO()
            xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter')
            df.to_excel(xlwriter, 'Raw Data')
            xlwriter.save()
            xlwriter.close()
            excel_file.seek(0)

            response = HttpResponse(excel_file.read(),
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=output1.xlsx'
            return response
        except DatabaseError as e:
            return Response({"Error" : str(e)}, status=status.HTTP_304_NOT_MODIFIED)

class RoundOffRetentionTime(views.APIView):

    def get(self, request, **kwargs):
        try:
            data = Data.objects.filter(name='analytics_data')[0]

            # Let's do the analytics
            df = pd.read_excel(data.file, sheet_name='Raw Data')
            df.columns = [col.replace('(min)', '').lower() for col in df.columns]
            df.columns = [col.strip() for col in df.columns]
            df.columns = [col.replace(' ', '_').lower() for col in df.columns]
            df = df.assign(retention_time_roundoff=(df.retention_time))

            df.retention_time_roundoff = df.retention_time_roundoff.astype(float).round().astype(int)
            retention_time_roundoff = df['retention_time_roundoff']

            excel_file = IO()
            xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter')
            df.to_excel(xlwriter, 'raw_data_1')
            retention_time_roundoff.to_excel(xlwriter, 'raw_data_2')
            xlwriter.save()
            xlwriter.close()
            excel_file.seek(0)

            response = HttpResponse(excel_file.read(),
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=output2.xlsx'
            return response
        except DatabaseError as e:
            return Response({"Error" : str(e)}, status=status.HTTP_304_NOT_MODIFIED)