from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from members import views 

urlpatterns = [
    # 1. 管理員後台
    path('admin/', admin.site.urls),

    # 2. 註冊頁面 (首頁)
    path('', views.index, name='index'),

    # 3. 處理註冊動作
    path('register/', views.register, name='register'),

    # 4. 登入頁面
    path('login/', views.login_view, name='login'),

    # 5. 修改個人資料頁面
    path('revise/', views.revise_view, name='revise'),

    # 6. 優惠資訊頁面
    path('data/', views.data_view, name='data_page'),

    # 7. 處理儲存喜愛類別
    path('save_favorites/', views.save_favorites, name='save_favorites'),

    # 8. 登出動作
    path('logout/', views.logout_view, name='logout'),

    path('setup/', views.setup_preferences, name='setup_preferences'),
]

# 讓 Django 在開發環境下能讀取 media 資料夾內的檔案
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)