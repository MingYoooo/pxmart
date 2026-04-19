from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserProfile, Product
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

# 1. 註冊頁面
def index(request):
    return render(request, 'register.html')

# 2. 註冊邏輯
@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            UserProfile.objects.create(
                email=request.POST.get('email'),
                nickname=request.POST.get('nickname'),
                gender=request.POST.get('gender'),
                birthday=request.POST.get('birthday'),
                password=request.POST.get('password')
            )
            messages.success(request, "註冊成功！請登入。")
            return redirect('/login/') 
        except Exception as e:
            return HttpResponse(f"發生錯誤：{str(e)}")
    return HttpResponse("請使用 POST 方法")

# 3. 登入邏輯
def login_view(request):
    if request.method == 'POST':
        email_input = request.POST.get('email')
        password_input = request.POST.get('password')
        try:
            user = UserProfile.objects.get(email=email_input)
            if user.password == password_input:
                request.session['user_email'] = user.email
                return redirect('/data/')
            else:
                messages.error(request, "密碼錯誤。")
        except UserProfile.DoesNotExist:
            messages.error(request, "帳號不存在。")
    return render(request, 'login.html')

# 4. 優惠資訊頁面 (整合喜好類別與商品排序)
def data_view(request):
    user_email = request.session.get('user_email')
    if not user_email: 
        return redirect('/login/')
    
    try:
        user = UserProfile.objects.get(email=user_email)
        products = Product.objects.all().order_by('-date')
        # 類別按字典順序排列
        categories = Product.objects.values_list('category', flat=True).distinct().order_by('category')
        
        # 讀取使用者喜好並轉為清單，供前端 checked 判斷
        user_favs = user.favorites.split(',') if user.favorites else []
        
        context = {
            'nickname': user.nickname,
            'products': products,
            'categories': categories,
            'user_favs': user_favs,
        }
        return render(request, 'data.html', context)
    except UserProfile.DoesNotExist:
        return redirect('/login/')

# 新增功能：儲存喜愛類別並返回頁面頂端
def save_favorites(request):
    user_email = request.session.get('user_email')
    if not user_email: 
        return redirect('/login/')

    if request.method == 'POST':
        selected_cats = request.POST.getlist('fav_categories')
        fav_str = ",".join(selected_cats)
        
        user = UserProfile.objects.get(email=user_email)
        user.favorites = fav_str
        user.save()
        
        # 發送儲存成功訊息
        messages.success(request, "喜好類別已成功儲存！之後有相關優惠將會通知您。")
    
    # 重新導向至 /data/ 頁面，瀏覽器會回到最上方並顯示 messages
    return redirect('/data/')

# 5. 修改個人資料
def revise_view(request):
    user_email = request.session.get('user_email')
    if not user_email: return redirect('/login/')
    try:
        user = UserProfile.objects.get(email=user_email)
        if request.method == 'POST':
            if user.password != request.POST.get('current_password'):
                messages.error(request, "目前密碼錯誤。")
            else:
                user.nickname = request.POST.get('nickname')
                user.gender = request.POST.get('gender')
                user.birthday = request.POST.get('birthday')
                if request.POST.get('new_password'):
                    user.password = request.POST.get('new_password')
                user.save()
                messages.success(request, "個人資料更新成功！")
                return redirect('/data/')
        return render(request, 'revise.html', {'user': user})
    except UserProfile.DoesNotExist:
        return redirect('/login/')

# 6. 登出
def logout_view(request):
    request.session.flush()
    messages.success(request, "您已成功登出。")
    return redirect('/login/')