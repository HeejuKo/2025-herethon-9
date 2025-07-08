from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import User
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q

def is_admin(user):
    return user.is_authenticated and user.userType == 'ADMIN'

@user_passes_test(is_admin)
def user_list(request):
    users = User.objects.exclude(
        Q(userType='ADMIN') | Q(username='admin')
    )
    return render(request, 'myadmin/user_list.html', {'users': users})

@user_passes_test(is_admin)
def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'toggle_verified':
            user.isVerified = not user.isVerified
            user.save()
            messages.success(request, '인증 상태가 변경되었습니다.')
        elif action == 'delete_user':
            user.delete()
            messages.success(request, '유저를 삭제했습니다.')
            return redirect('myadmin:user_list')

    return render(request, 'myadmin/user_detail.html', {'user': user})