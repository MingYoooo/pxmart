const { createClient } = require('@supabase/supabase-js');
const nodemailer = require('nodemailer');

const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_KEY);

const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: { user: process.env.EMAIL_USER, pass: process.env.EMAIL_PASS },
});

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function sendDailyDeals() {
  console.log('--- 任務開始：' + new Date().toLocaleString() + ' ---');

  // A. 取得所有使用者
  const { data: users, error: userError } = await supabase
    .from('members_userprofile')
    .select('email, nickname, favorites, date_joined');

  if (userError) {
    console.error('❌ 讀取用戶資料失敗:', userError);
    return;
  }

  // 取得今天的日期並歸零時間
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  for (let i = 0; i < users.length; i++) {
    const user = users[i];
    
    // 如果沒有 email、沒有喜好，或沒有註冊時間，就跳過
    if (!user.email || !user.favorites || !user.date_joined) continue;

    try {
      // --- 生命週期郵件日期判斷邏輯 ---
      const joinDate = new Date(user.date_joined);
      joinDate.setHours(0, 0, 0, 0);

      const diffTime = Math.abs(today - joinDate);
      const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

      // 判斷是否「不符合」寄信條件
      if (diffDays === 0) {
        console.log(`⏸️ 跳過 ${user.email} (今天剛註冊，明天才會發送首封)`);
        continue;
      } else if (diffDays > 1 && (diffDays - 1) % 3 !== 0) { // <--- 這裡改成了 % 3
        console.log(`⏸️ 跳過 ${user.email} (註冊第 ${diffDays} 天 - 未達每三天寄送日)`);
        continue;
      }

      // 印出準備發送的提示
      if (diffDays === 1) {
        console.log(`🎯 準備發送給 ${user.email} (註冊第 ${diffDays} 天 - 首次通知)`);
      } else {
        console.log(`🎯 準備發送給 ${user.email} (註冊第 ${diffDays} 天 - 每三天定期通知)`); // <--- 這裡改了文字
      }
      // --- 日期判斷邏輯結束 ---

      // B. 處理喜好類別
      const favoriteList = user.favorites.split(/[、,]/).map(item => item.trim()).filter(item => item !== "");
      
      let allUserProducts = [];

      // C. 抓取所有符合條件的商品
      for (const fav of favoriteList) {
        const { data: products, error: prodError } = await supabase
          .from('pxmart_data')
          .select('品名, 價格詳細, 類別')
          .ilike('類別', `%${fav}%`) 
          .order('日期', { ascending: false }); 

        if (!prodError && products) {
          allUserProducts = allUserProducts.concat(products);
        }
      }

      // D. 移除重複商品
      const uniqueProducts = Array.from(new Set(allUserProducts.map(a => a.品名)))
        .map(品名 => allUserProducts.find(a => a.品名 === 品名));

      if (uniqueProducts.length === 0) {
        console.log(`ℹ️ 用戶 ${user.nickname} 目前無優惠商品。`);
        continue;
      }

      // E. 組合 HTML
      const productRows = uniqueProducts.map(p => `
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
          <div style="padding: 20px;">
            <p><b>${user.nickname}</b> 您好：</p>
            <p>您的關注類別：<span style="color: #e11d48;">${user.favorites}</span></p>
            <p style="color: #666; font-size: 14px;">今日共有 ${uniqueProducts.length} 件優惠商品：</p>
            <ul style="padding: 0;">${productRows}</ul>
          </div>
        </div>
      `;

      // F. 發送 Email
      await transporter.sendMail({
        from: `"全聯特惠機器人" <${process.env.EMAIL_USER}>`,
        to: user.email,
        subject: `【今日完整更新】${user.nickname}，您關注的類別優惠總整理！`,
        html: htmlBody,
      });

      console.log(`✅ 郵件已發送至: ${user.email} (共 ${uniqueProducts.length} 筆商品)`);
      await sleep(1500); 

    } catch (err) {
      console.error(`❌ 處理用戶 ${user.email} 時錯誤:`, err.message);
    }
  }
  console.log('--- 任務完成 ---');
}

sendDailyDeals();