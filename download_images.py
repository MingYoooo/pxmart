import os
import time
import requests
import django

# 1. 載入 Django 環境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

# 2. 引入正確的 Model 名稱：Product (對應你的 members/models.py)
from members.models import Product 

def run_downloader():
    # 設定圖片儲存路徑
    save_dir = os.path.join('media', 'products')
    os.makedirs(save_dir, exist_ok=True)

    # 偽裝瀏覽器，避免被全聯阻擋
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    # 抓取所有商品資料
    items = Product.objects.all()
    total = items.count()
    print(f"總共找到 {total} 筆商品，開始檢查圖片...")

    for index, item in enumerate(items, 1):
        try:
            # 取得圖片網址 (對應 models.py 裡的 image_url)
            img_url = getattr(item, 'image_url', None) 
            
            if not img_url or 'http' not in img_url:
                continue

            # 用 ID 當檔名，存放在 media/products/
            file_path = os.path.join(save_dir, f"{item.id}.png")

            # 如果圖片已經存在就跳過
            if os.path.exists(file_path):
                continue

            print(f"[{index}/{total}] 正在下載: {item.name} ...")
            res = requests.get(img_url, headers=headers, timeout=10)
            
            if res.status_code == 200:
                with open(file_path, 'wb') as f:
                    f.write(res.content)
                # 禮貌性停頓，避免被封鎖
                time.sleep(0.3) 
            
        except Exception as e:
            print(f"商品 {item.name} 下載出錯: {e}")

    print("\n✅ 執行完畢！圖片已存入 media/products 資料夾。")

if __name__ == '__main__':
    run_downloader()