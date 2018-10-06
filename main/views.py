from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from .forms import ImageUploadForm, ExcelUploadForm
from .models import Document
from django.urls import reverse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.template import RequestContext
from detector.detector import model_init, TRANSFORM_IMG_TEST

import os
import cv2
import glob
import random
from datetime import datetime
import scipy.misc
from PIL import Image
import matplotlib.pyplot as plt
from anova.views import read_excel

from django.conf import settings
from django.core.files.storage import FileSystemStorage

def directory_path():
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    today = datetime.today()
    cur_date = datetime(today.year, today.month, today.day).strftime('%y_%m_%d')
    return 'uploads/{0}/{1}/'.format(cur_date,random.randint(1000,9999))

def basic(request):
    # model = model_init()
    if request.method == 'POST':

        if request.POST['type_of_analysis'] == 'opisthorchiasis':
            form = ImageUploadForm(request.POST, request.FILES)
            if form.is_valid():
                image_name, full_path = handle_uploaded_image(request.FILES['image'])
                prediction = detect_image(full_path)
                form = ImageUploadForm()
                image_name2 = 'outfile.jpg'
                context = {'photo_url': image_name, 'photo_url2':image_name2}
                return render(request, 'main/basic.html', context)
            else:
                form = ImageUploadForm()
                return render(request, 'main/basic.html')

        elif request.POST['type_of_analysis'] == 'anova':
            # Simple save
            try:
                myfile = request.FILES['image']
            except:
                form = ImageUploadForm()
                return render(request, 'main/basic.html')
            path = directory_path()
            fs = FileSystemStorage(path)
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)

            form = ImageUploadForm()
            dfr = read_excel(os.path.join(settings.BASE_DIR, path + 'sample.xlsx'))
            # return HttpResponse(dfr)
            return render(request, 'main/basic.html', {'result':dfr})
        else:
            form = ImageUploadForm()
            return render(request, 'main/basic.html')
            # Save via models and forms
            # form = ExcelUploadForm(request.POST, request.FILES)
            # if form.is_valid():
            #     newdoc = Document(docfile = request.FILES['image'])
            #     # tmp = dir(newdoc)
            #     # for i in tmp:
            #     #     print(eval('newdoc.{}'.format(i)))
            #     #     print('--'*10)
            #     newdoc.save()
            #     data = request.FILES['image']
            #     print(data)
            #     # full_path = handle_uploaded_excel(request.FILES['image'])
            #     return HttpResponse('q')
            # else:
            #     form = ImageUploadForm()
            #     return render(request, 'main/basic.html')
    form = ImageUploadForm()
    return render(request, 'main/basic.html')

# def handle_uploaded_excel(image):
#     # save image in to static/media - Nginx/Gunicorn
#     path = default_storage.save('', ContentFile(image))
#     full_path = os.path.join(settings.MEDIA_ROOT, path)
#     image_name = 'uploads/' + path
#     return full_path


def handle_uploaded_image(image):
    # save image in to static/media - Nginx/Gunicorn
    image = image.read()
    path = default_storage.save('', ContentFile(image))
    full_path = os.path.join(settings.MEDIA_ROOT, path)
    image_name = 'media/' + path
    return image_name, full_path


def detect_image(full_path):
    model = model_init()
    img = TRANSFORM_IMG_TEST(cv2.imread(full_path)[...,::-1]).unsqueeze(0)
    res = model(img)
    res_FOR_VISUAL = res[0][0].data.numpy()
    # scipy.misc.imsave('static/outfile.jpg', res_FOR_VISUAL) # for web-server
    scipy.misc.imsave('main/static/outfile.jpg', res_FOR_VISUAL) # for local-server
