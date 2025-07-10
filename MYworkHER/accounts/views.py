from django.shortcuts import render, redirect
from .forms import *
from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from base64 import b64decode

def signup_step1(request):
    if request.method == 'POST':
        form = SignupStep1Form(request.POST)
        if form.is_valid():
            request.session['username'] = form.cleaned_data['username']
            request.session['password'] = form.cleaned_data['password1']
            request.session['email'] = form.cleaned_data['email']
            request.session['phone'] = form.cleaned_data['phone']
            return redirect('accounts:signup_step2')
    else:
        form = SignupStep1Form()

    return render(request, 'accounts/signup/step1.html', {'form': form})

def signup_step2(request):
    if request.method == 'POST':
        form = SignupStep2Form(request.POST, request.FILES)
        if form.is_valid():
            id_image: InMemoryUploadedFile = form.cleaned_data['id_image']
            request.session['id_image_name'] = id_image.name
            request.session['id_image_content'] = id_image.read().decode('latin1')  # binary를 세션에 담기 위해 인코딩
            return redirect('accounts:signup_step3')
    else:
        form = SignupStep2Form()

    return render(request, 'accounts/signup/step2.html', {'form': form})

def signup_step3(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        if user_type in ['CUSTOMER', 'EXPERT']:
            request.session['user_type'] = user_type
            return redirect('accounts:signup_step4')
        else:
            return render(request, 'accounts/signup/step3.html')
        
    return render(request, 'accounts/signup/step3.html')

def signup_step4(request):
    if request.method == 'POST':
        form = SignupStep4Form(request.POST)
        if form.is_valid():
            request.session['nickname'] = form.cleaned_data['nickname']
            request.session['introduction'] = form.cleaned_data['introduction']
            return redirect('accounts:signup_complete')
    else:
        form = SignupStep4Form()

    return render(request, 'accounts/signup/step4.html', {'form': form})

def signup_complete(request):
    # 세션에서 모든 회원가입 정보 꺼내기
    username = request.session.get('username')
    password = request.session.get('password')
    email = request.session.get('email')
    phone = request.session.get('phone')
    user_type = request.session.get('user_type')
    nickname = request.session.get('nickname')
    introduction = request.session.get('introduction')

    id_image_name = request.session.get('id_image_name')
    id_image_content = request.session.get('id_image_content')

    if not all([username, password, email]):
        return redirect('accounts:signup_step1')  # 유효하지 않으면 다시 처음으로

    # 유저 생성
    user = User(
        username = username,
        email = email,
        phone = phone,
        userType = user_type,
        nickname = nickname,
        introduction = introduction,
        isVerified = False
    )
    user.set_password(password)

    # 이미지 복원 및 저장
    if id_image_name and id_image_content:
        image_bytes = id_image_content.encode('latin1')
        user.idImage.save(id_image_name, ContentFile(image_bytes), save = False)

    user.save()
    request.session.flush()

    return render(request, 'accounts/signup/complete.html')
    
def login(request):
    if request.method == 'GET':
        return render(request, 'accounts/login.html', {'form': AuthenticationForm()})
    
    form = AuthenticationForm(request, request.POST)
    if form.is_valid():
        auth_login(request, form.user_cache)
        return redirect('matching:main')
    return render(request, 'accounts/login.html', {'form': form})

def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('matching:main')

@login_required
def mypage(request):
    return render(request, 'accounts/mypage.html')

@login_required
def mypage_update(request):
    if request.method == "POST":
        user = request.user

        # 기본 정보 업데이트
        user.nickname = request.POST.get('nickname', user.nickname)
        user.phone = request.POST.get('phone', user.phone)
        user.email = request.POST.get('email', user.email)
        user.introduction = request.POST.get('introduction', user.introduction)

        # 프로필 이미지 삭제 요청 처리
        if request.POST.get('delete_profile') == "true":
            if user.profileImage:
                user.profileImage.delete()
                user.profileImage = None
        else:
            # 새로운 이미지 업로드 처리
            profile_image = request.FILES.get('upload_image')
            if profile_image:
                if user.profileImage:
                    user.profileImage.delete()
                user.profileImage = profile_image

        user.save()
        return redirect('accounts:mypage')

    return render(request, 'accounts/mypage-update.html')