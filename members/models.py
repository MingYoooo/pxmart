from django.db import models

# 1. 使用者資料
class UserProfile(models.Model):
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    birthday = models.DateField()
    password = models.CharField(max_length=128)
    # 儲存喜愛的類別，以逗號隔開的字串儲存
    favorites = models.TextField(default="", blank=True)

    def __str__(self):
        return self.nickname

# 2. 整合後的商品優惠資訊 (與 Supabase 上的 pxmart_data 資料表對應)
class Product(models.Model):
    category = models.CharField(max_length=100, db_column='類別', verbose_name="類別")
    name = models.CharField(max_length=255, db_column='品名', verbose_name="品名")
    price_detail = models.TextField(db_column='價格詳細', verbose_name="價格詳細")
    date = models.CharField(max_length=50, db_column='日期', verbose_name="日期")
    
    # 新增這行：對應資料庫中的圖片網址欄位
    # 這裡的 db_column 必須與你資料庫中的實際欄位名稱一致（例如 '圖片網址'）
    image_url = models.TextField(db_column='圖片網址', verbose_name="圖片網址", default="", blank=True, null=True)

    class Meta:
        managed = False          # 因為是連接現有的資料表，不讓 Django 進行遷移管理
        db_table = 'pxmart_data' # 對應資料庫中的真實資料表名稱

    def __str__(self):
        return self.name