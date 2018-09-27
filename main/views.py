from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from .forms import ImageUploadForm
from django.urls import reverse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.template import RequestContext
from detector.detector import model_init, TRANSFORM_IMG_TEST

import os
import cv2
import glob
import scipy.misc
from PIL import Image
import matplotlib.pyplot as plt

def basic(request):
    # model = model_init()
    if request.method == 'POST':
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
    else:
        form = ImageUploadForm()
        return render(request, 'main/basic.html')

def handle_uploaded_image(image):
    # save image in to static/media - Nginx/Gunicorn
    image = image.read()
    path = default_storage.save('', ContentFile(image))
    full_path = os.path.join(settings.MEDIA_ROOT, path)
    image_name = '/media/' + path
    return image_name, full_path


def detect_image(full_path):
    model = model_init()
    img = TRANSFORM_IMG_TEST(cv2.imread(full_path)[...,::-1]).unsqueeze(0)
    res = model(img)
    res_FOR_VISUAL = res[0][0].data.numpy()
    scipy.misc.imsave('static/outfile.jpg', res_FOR_VISUAL)
