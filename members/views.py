from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserProfile, Product
from django.contrib import messages

# 1. 註冊頁面
def index(request):
    return render(request, 'register.html')

# 2. 註冊邏輯
def register(request):
    if request.method == 'POST':
        email_input = request.POST.get('email', '').strip().lower()
        nickname_input = request.POST.get('nickname')
        gender_input = request.POST.get('gender')
        birthday_input = request.POST.get('birthday')
        password_input = request.POST.get('password')

        try:
            if UserProfile.objects.filter(email=email_input).exists():
                messages.error(request, "此電子郵件已被註冊過囉！請直接登入或更換 Email。")
                return redirect('/')

            UserProfile.objects.create(
                email=email_input,
                nickname=nickname_input,
                gender=gender_input,
                birthday=birthday_input,
                password=password_input
            )
            messages.success(request, "註冊成功！歡迎加入，請登入。")
            return redirect('/login/') 
        except Exception as e:
            return HttpResponse(f"發生錯誤：{str(e)}")
    return HttpResponse("請使用 POST 方法")

# 3. 登入邏輯
def login_view(request):
    if request.method == 'POST':
        email_input = request.POST.get('email', '').strip().lower()
        password_input = request.POST.get('password')
        try:
            user = UserProfile.objects.get(email=email_input)
            if user.password == password_input:
                request.session['user_email'] = user.email
                
                # 新手引導判斷：如果喜好清單是空的
                if not user.favorites:
                    return redirect('/setup/')
                return redirect('/data/')
            else:
                messages.error(request, "密碼錯誤。")
        except UserProfile.DoesNotExist:
            messages.error(request, "帳號不存在。")
    return render(request, 'login.html')

# 新增功能：新手引導設定頁面
def setup_preferences(request):
    user_email = request.session.get('user_email')
    if not user_email: return redirect('/login/')
    
    try:
        user = UserProfile.objects.get(email=user_email)
        # 取得所有不重複的分類
        categories = Product.objects.values_list('category', flat=True).distinct().order_by('category')
        
        if request.method == 'POST':
            selected_cats = request.POST.getlist('fav_categories')
            if selected_cats:
                user.favorites = ",".join(selected_cats)
                user.save()
                messages.success(request, f"太棒了，{user.nickname}！設定已完成。")
                return redirect('/data/')
            else:
                messages.warning(request, "請至少選擇一個類別，我們才能通知您喔！")
                
        return render(request, 'setup_preferences.html', {
            'nickname': user.nickname,
            'categories': categories
        })
    except UserProfile.DoesNotExist:
        return redirect('/login/')

# 4. 優惠資訊頁面 (包含類別顯示)
def data_view(request):
    user_email = request.session.get('user_email')
    if not user_email: return redirect('/login/')
    
    try:
        user = UserProfile.objects.get(email=user_email)
        products = Product.objects.all().order_by('-date')
        categories = Product.objects.values_list('category', flat=True).distinct().order_by('category')
        
        # 安全處理 favorites 可能為空或 None 的情況
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

# 儲存喜愛類別邏輯 (處理你遇到的 403 錯誤)
def save_favorites(request):
    user_email = request.session.get('user_email')
    if not user_email: return redirect('/login/')

    if request.method == 'POST':
        try:
            selected_cats = request.POST.getlist('fav_categories')
            user = UserProfile.objects.get(email=user_email)
            # 即使 selected_cats 是空的，也會儲存為空字串，代表取消所有選取
            user.favorites = ",".join(selected_cats)
            user.save()
            messages.success(request, "喜好類別已更新！")
        except Exception as e:
            messages.error(request, f"儲存失敗：{str(e)}")
    
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