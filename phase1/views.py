from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import status
from django.conf import settings

import os
from django.http import HttpResponse, Http404

from datetime import datetime

from .models import FileModel, HistoryModel
from .serializers import FileSerializer

def get_history_list():
    history = HistoryModel.objects.values_list('history_name', flat=True)
    return history.distinct()
def get_file_list():
    files = FileModel.objects.values_list('file_name',flat=True)
    return files.distinct()
    
def get_algorithm_list():
    return['Analytic 1: Classification', 'Analytic 2: Regression' , 'Analytic 3: Outlier Detector']
def get_algorithm(name):
    if name == 'Analytic 1: Classification':
        from .algos import run_algo1
        return run_algo1
    elif name == 'Analytic 2: Regression':
        from .algos import run_algo2
        return run_algo2
    elif name == 'Analytic 3: Outlier Detector':
        from .algos import run_algo3
        return run_algo3
    else:
        # Http404 is imported from django.http
        raise Http404('<h1>Target algorithm not found</h1>')
def run_analytic(file_path, algo):
    print(settings.MEDIA_ROOT)
    file_abs_path = os.path.join(settings.MEDIA_ROOT, str(file_path))
    return algo(file_abs_path)

class YourViewName(APIView):

    parser_classes = [JSONParser, FormParser, MultiPartParser]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'index.html'
    
    # See Django REST Request class here:
    # https://www.django-rest-framework.org/api-guide/requests/
    def get(self, request):
        f = FileModel.objects.all()
        #return Response({'f': f}, status=status.HTTP_200_OK)
        return Response({'f': f, 'files': get_file_list(), 'algorithms': get_algorithm_list()}, status=status.HTTP_200_OK)

    def post(self, request):
        # Upload form
        print('TEST: ' + str(request.data))
        #import pdb;pdb.set_trace()
        if 'upload' in request.data:
            file_serializer = FileSerializer(data=request.data)
            if FileModel.objects.filter(file_name = request.data['file_name']).exists():
                query_file_name = request.data['file_name']
                file_obj = FileModel.objects.get(file_name = query_file_name)
                file_path = file_obj.file_content
                os.remove('media/' + str(file_path))
                file_obj.delete()
                
            if file_serializer.is_valid():
                data = (file_serializer.validated_data)['file_content']
                name = data.name
                if(name.find('.csv') == -1):
                    f = FileModel.objects.all()
                    return Response({'f':f, 'status': 'Please Upload .csv file','algorithms': get_algorithm_list()}, status=status.HTTP_201_CREATED)
                else:
                    file_serializer.save()
                    f = FileModel.objects.all()
                    return Response({'f':f, 'status': 'Upload successful!', 'files': get_file_list(), 'algorithms': get_algorithm_list()}, status=status.HTTP_201_CREATED)

            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        elif 'analytic' in request.data:
            # Run analytics on dataset as specified by file_name and
            # analytic_id received in the post request
            query_file_name = request.data['file_name']
            query_algorithm = request.data['algorithm']
            # Find file path to local folder
            file_obj = FileModel.objects.get(file_name=query_file_name)
            file_path = file_obj.file_content
            # Find algorithm
            algo_obj = get_algorithm(query_algorithm)
            #print(algo_obj)
            analyticresult = run_analytic(file_path, algo_obj)
            f = FileModel.objects.all()
            
            temp = HistoryModel.objects.create(history_name = str(query_file_name)+'' + str(query_algorithm)+ '' + str(datetime.now()), history_content = analyticresult)
            temp.save()
            return Response({'f':f, 'files':get_file_list(), 'algorithms':get_algorithm_list(), 'result_plot':analyticresult,'history': get_history_list()}, status=status.HTTP_200_OK)
        elif 'history' in request.data:
            print("viewing History")
            query_history_name = request.data['history_name']
            print(query_history_name)
            history_obj = HistoryModel.objects.get(
            history_name=query_history_name)
            content = history_obj.history_content

            # query_file_name = request.data['history_name']
            # history_obj = HistoryModel.objects.get(file_name=query_file_name)
            # content = history_obj.history_content
            return Response({'files': get_file_list(), 'algorithms': get_algorithm_list(), 'result_plot': content, 'history': get_history_list()}, status=status.HTTP_200_OK)
        elif 'delete_history' in request.data:
            print("delete")
            query_history_name = request.data['history_name']
            history_obj = HistoryModel.objects.get(history_name=query_history_name)
            history_obj.delete()
            return redirect('phase1:phase1')
        
            
def delete(request, pk):
    try:
        file = FileModel.objects.get(pk=pk)
        file.file_content.delete()
        file.delete()
        return redirect('phase1:phase1')
    except:
        print('failed to delete a file')
        return redirect('phase1:phase1')
    #return Response({'f': f, 'files': get_file_list(), 'algorithms': get_algorithm_list()}, status=status.HTTP_200_OK)
 
        

    
