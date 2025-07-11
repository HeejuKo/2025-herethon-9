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

    users = list(User.objects.exclude(
        Q(userType='ADMIN') | Q(username='admin')
    ))

    idx = next((i for i, u in enumerate(users) if u.id == user.id), None)
    prev_user = users[idx - 1] if idx is not None and idx > 0 else None
    next_user = users[idx + 1] if idx is not None and idx < len(users) - 1 else None

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

    return render(request, 'myadmin/user_detail.html', {'user': user, 'prev_user': prev_user, 'next_user': next_user})