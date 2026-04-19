const { createClient } = require('@supabase/supabase-js');
const nodemailer = require('nodemailer');

// 1. 初始化 Supabase
const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_KEY
);

// 2. 設定 Gmail 發信
const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: process.env.EMAIL_USER,
    pass: process.env.EMAIL_PASS,
  },
});

// 輔助函數：延遲執行（避免觸發 Gmail 垃圾郵件機制）
const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function sendDailyDeals() {
  console.log('--- 任務開始：' + new Date().toLocaleString() + ' ---');

  // A. 取得所有使用者
  const { data: users, error: userError } = await supabase
    .from('members_userprofile')
    .select('email, nickname, favorites');

  if (userError) {
    console.error('❌ 讀取用戶資料失敗:', userError);
    return;
  }

  console.log(`預計處理 ${users.length} 個帳號...`);

  for (let i = 0; i < users.length; i++) {
    const user = users[i];
    
    // 檢查是否有 email 與 喜好
    if (!user.email || !user.favorites) {
      console.log(`⚠️ 跳過用戶 ${user.nickname || '未命名'}: 無 Email 或無喜好資料`);
      continue;
    }

    try {
      // B. 處理喜好類別
      const favoriteList = user.favorites.split(/[、,]/).map(item => item.trim());

      // C. 查詢該用戶感興趣的優惠商品
      const { data: products, error: prodError } = await supabase
        .from('pxmart_data')
        .select('品名, 價格詳細, 類別')
        .in('類別', favoriteList)
        .order('日期', { ascending: false }) // 優先顯示最新的優惠
        .limit(15);

      if (prodError) throw prodError;

      if (!products || products.length === 0) {
        console.log(`ℹ️ 用戶 ${user.nickname} (${user.email}) 的類別目前無優惠商品，跳過發信。`);
        continue;
      }

      // D. 組合 HTML 郵件內容
      const productRows = products.map(p => `
        <li style="margin-bottom: 12px; list-style: none; border-bottom: 1px dashed #eee; padding-bottom: 8px;">
          <span style="background: #e11d48; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">
            ${p.類別}
          </span>
          <div style="margin-top: 5px;">
            <b style="color: #333; font-size: 16px;">${p.品名}</b>
            <div style="color: #b91c1c; font-size: 15px; font-weight: bold; margin-top: 3px;">
              💰 ${p.價格詳細}
            </div>
          </div>
        </li>
      `).join('');

      const htmlBody = `
        <div style="font-family: 'Microsoft JhengHei', Arial, sans-serif; max-width: 600px; margin: auto; border: 1px solid #ddd; border-radius: 8px; overflow: hidden;">
          <div style="background: #e11d48; color: white; padding: 20px; text-align: center;">
            <h1 style="margin: 0; font-size: 20px;">全聯今日特惠報</h1>
          </div>
          <div style="padding: 20px; background: #fff;">
            <p style="font-size: 16px;"><b>${user.nickname}</b> 您好：</p>
            <p style="color: #666;">根據您關注的類別：<span style="color: #e11d48;">${user.favorites}</span>，我們為您篩選了以下優惠：</p>
            <ul style="padding: 0;">
              ${productRows}
            </ul>
            <div style="text-align: center; margin-top: 30px;">
              <p style="font-size: 12px; color: #999;">
                此郵件由畢業專題自動化系統發送，請勿直接回覆。<br>
                更新時間：${new Date().toLocaleDateString()}
              </p>
            </div>
          </div>
        </div>
      `;

      // E. 執行發送
      await transporter.sendMail({
        from: `"全聯特惠機器人" <${process.env.EMAIL_USER}>`,
        to: user.email,
        subject: `【今日優惠】${user.nickname}，您關注的商品折扣報來囉！`,
        html: htmlBody,
      });

      console.log(`✅ [${i + 1}/${users.length}] 郵件已發送至: ${user.email}`);

      // 如果不是最後一封，等待 1.5 秒再發下一封（保護帳號不被停權）
      if (i < users.length - 1) {
        await sleep(1500); 
      }

    } catch (err) {
      console.error(`❌ [${i + 1}/${users.length}] 處理用戶 ${user.email} 時發生錯誤:`, err.message);
      // 發生錯誤不中斷，繼續處理下一個使用者
    }
  }

  console.log('--- 任務完成：' + new Date().toLocaleString() + ' ---');
}

// 執行主程式
sendDailyDeals().catch(err => {
  console.error('致命錯誤:', err);
  process.exit(1);
});