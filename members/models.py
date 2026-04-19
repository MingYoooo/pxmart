from django.db import models

# 1. 原有的使用者資料 (增加 favorites 欄位)
class UserProfile(models.Model):
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    birthday = models.DateField()
    password = models.CharField(max_length=128)
    # 新增：儲存喜愛的類別，以逗號隔開的字串儲存
    favorites = models.TextField(default="", blank=True)

    def __str__(self):
        return self.nickname

# 2. 整合後的商品優惠資訊
class Product(models.Model):
    category = models.CharField(max_length=100, db_column='類別', verbose_name="類別")
    name = models.CharField(max_length=255, db_column='品名', verbose_name="品名")
    price_detail = models.TextField(db_column='價格詳細', verbose_name="價格詳細")
    date = models.CharField(max_length=50, db_column='日期', verbose_name="日期")

    class Meta:
        managed = False          
        db_table = 'pxmart_data' 

    def __str__(self):
        return self.name