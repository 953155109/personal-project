import json

html_template = """<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>万科城市花园105㎡户型装修方案</title>
    <style>
      :root {
        --primary: #8b7355;
        --primary-light: #f5f1eb;
        --primary-dark: #6b583f;
        --text-main: #333333;
        --text-light: #666666;
        --border: #e0d9cf;
        --bg-color: #faf8f5;
        --white: #ffffff;
      }

      body {
        font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
        background-color: var(--bg-color);
        color: var(--text-main);
        margin: 0;
        padding: 40px 20px;
      }

      .container {
        max-width: 1200px;
        margin: 0 auto;
        background: var(--white);
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(139, 115, 85, 0.08);
        overflow: hidden;
      }

      .header {
        text-align: center;
        padding: 40px 20px 30px;
        background-color: var(--white);
        position: relative;
      }

      .header h1 {
        font-size: 32px;
        color: var(--primary);
        margin-bottom: 10px;
        letter-spacing: 2px;
      }

      .header p {
        color: var(--text-light);
        font-size: 16px;
      }

      .nav-tabs {
        display: flex;
        background: var(--bg-color);
        border-bottom: 1px solid var(--border);
        border-top: 1px solid var(--border);
      }

      .nav-tab {
        flex: 1;
        padding: 16px 20px;
        text-align: center;
        cursor: pointer;
        font-size: 16px;
        font-weight: 500;
        color: var(--text-light);
        transition: all 0.3s ease;
      }

      .nav-tab.active {
        background: var(--white);
        color: var(--primary);
        border-bottom: 3px solid var(--primary);
      }

      .nav-tab:hover {
        background: var(--primary-light);
        color: var(--primary);
      }

      .content-section {
        padding: 40px;
        display: none;
      }

      .content-section.active {
        display: block;
      }

      .section-title {
        color: var(--primary);
        border-bottom: 2px solid var(--primary-light);
        padding-bottom: 15px;
        margin-top: 0;
        margin-bottom: 25px;
        font-size: 22px;
        display: flex;
        justify-content: space-between;
        align-items: center;
      }

      .summary-cards {
        display: flex;
        gap: 20px;
        margin-bottom: 40px;
        flex-wrap: wrap;
      }

      .card {
        flex: 1;
        min-width: 200px;
        background: var(--white);
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(139, 115, 85, 0.08);
        text-align: center;
        border-top: 4px solid var(--primary);
      }

      .card h3 {
        margin: 0 0 10px 0;
        font-size: 16px;
        color: var(--text-light);
        font-weight: normal;
      }

      .card .amount {
        font-size: 28px;
        font-weight: bold;
        color: var(--primary);
      }

      .category-group {
        margin-bottom: 30px;
        background: var(--white);
        border-radius: 8px;
        border: 1px solid var(--border);
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
      }

      .category-title {
        font-size: 18px;
        font-weight: bold;
        background: var(--primary-light);
        padding: 15px 20px;
        margin: 0;
        color: var(--primary-dark);
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid var(--border);
      }
      
      .title-actions {
        display: flex;
        align-items: center;
      }

      .export-btn {
        background: var(--primary);
        color: var(--white);
        border: none;
        padding: 6px 16px;
        border-radius: 4px;
        font-size: 14px;
        cursor: pointer;
        transition: background 0.3s;
        margin-left: 10px;
      }
      
      .export-btn:hover {
        background: var(--primary-dark);
      }

      .save-btn {
        background: #3fb950;
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 6px;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(63, 185, 80, 0.3);
        margin-top: 15px;
      }

      .save-btn:hover {
        background: #2ea043;
        transform: translateY(-2px);
      }
      
      .save-btn:disabled {
        background: #94d3a2;
        cursor: not-allowed;
        transform: none;
      }

      .table-container {
        overflow-x: auto;
        border-radius: 8px;
        border: 1px solid var(--border);
      }

      table {
        width: 100%;
        border-collapse: collapse;
      }

      table thead tr {
        background: var(--primary-light);
      }

      table th, table td {
        padding: 12px 15px;
        text-align: left;
        border-bottom: 1px dashed var(--border);
        font-size: 15px;
      }

      table th {
        color: var(--primary-dark);
        font-weight: bold;
        font-size: 14px;
        border-bottom: 1px solid var(--border);
      }
      
      table tbody tr:nth-child(even) {
        background: #fafafa;
      }

      table tbody tr:hover {
        background: var(--primary-light);
      }

      .price-col {
        text-align: right;
      }

      .price {
        font-weight: bold;
        color: var(--text-main);
      }
      
      .center-col {
        text-align: center;
      }

      .highlight-list {
        font-size: 15px;
        line-height: 2;
        color: var(--text-light);
        margin-left: 20px;
      }
      
      .highlight-list li {
        margin-bottom: 8px;
      }

      .highlight-list strong {
        color: var(--primary-dark);
      }

      .floor-plan {
        max-width: 100%;
        border-radius: 8px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 30px;
      }

      .axis-note {
        background: var(--primary-light);
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 30px;
        border-left: 4px solid var(--primary);
      }

      .axis-note h3 {
        font-size: 18px;
        color: var(--primary-dark);
        margin-top: 0;
        margin-bottom: 15px;
      }

      .axis-note p {
        font-size: 15px;
        color: var(--text-main);
        line-height: 1.8;
      }

      .editable-cell {
        cursor: text;
        transition: background 0.2s;
        border-bottom: 1px dashed #ccc;
      }
      .editable-cell:hover, .editable-cell:focus {
        background-color: #fff3cd;
        outline: none;
      }

      #loading-overlay {
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(255,255,255,0.8);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
        font-size: 24px;
        color: var(--primary);
        font-weight: bold;
      }

      @media (max-width: 768px) {
        .summary-cards {
          flex-direction: column;
        }
        .content-section {
          padding: 20px;
        }
      }
    </style>
  </head>
  <body>
    <div id="loading-overlay">正在加载最新云端数据...</div>
    <div class="container">
      <div class="header">
        <h1>万科城市花园105㎡户型装修方案</h1>
        <p>原木风设计 | 所有人可实时修改并保存</p>
        <button id="save-all-btn" class="save-btn" onclick="saveData()">💾 保存所有修改至云端</button>
      </div>

      <div class="nav-tabs">
        <div class="nav-tab active" data-tab="overview">概算总览</div>
        <div class="nav-tab" data-tab="hardware">硬装清单明细</div>
        <div class="nav-tab" data-tab="soft">软装与家电明细</div>
        <div class="nav-tab" data-tab="floorplan">户型优化方案</div>
      </div>

      <!-- 总览部分 -->
      <div class="content-section active" id="overview">
        <h2 class="section-title">
            装修总预算预估
            <button class="export-btn" onclick="exportMultipleTables(['hard-table'], Array.from({length: document.querySelectorAll('[id^=soft-table-]').length}).map((_, i) => 'soft-table-' + (i+1)), '全部预算清单')">导出全部清单</button>
        </h2>
        <div class="summary-cards">
          <div class="card">
            <h3>总预算预估 (硬装+软装电器)</h3>
            <div class="amount" id="sum-total">¥ 0.00</div>
          </div>
          <div class="card">
            <h3>硬装部分合计</h3>
            <div class="amount" id="sum-hard">¥ 0.00</div>
          </div>
          <div class="card">
            <h3>软装及家电合计</h3>
            <div class="amount" id="sum-soft">¥ 0.00</div>
          </div>
          <div class="card">
            <h3>硬装占比</h3>
            <div class="amount" id="sum-percent">0.00%</div>
          </div>
        </div>

        <h2 class="section-title">方案核心亮点</h2>
        <ul class="highlight-list">
          <li>严格基于原户型结构优化，不拆承重墙，安全合规。</li>
          <li>原木风统一设计，浅橡木+奶白色为主，柔和通透，适配户型南北采光优势。</li>
          <li>解决原户型痛点：无玄关隐私差、过道浪费、厨房采光弱、次卧噪音干扰。</li>
          <li>全屋定制收纳系统，最大化利用空间，解决老小区收纳不足问题。</li>
          <li>预算清晰可控，硬装+软装完整覆盖，无隐形消费。</li>
        </ul>
      </div>

      <!-- 硬装清单部分 -->
      <div class="content-section" id="hardware">
        <h2 class="section-title">
            <span>硬装预算清单 <span style="font-size: 15px; color: var(--text-main); font-weight: normal; margin-left: 10px;" id="hard-total-title">总计：¥ 0.00</span></span>
            <button class="export-btn" onclick="exportTable('hard-table', '硬装清单')">导出硬装清单</button>
        </h2>
        <div class="table-container">
          <table id="hard-table">
            <thead>
              <tr>
                <th class="center-col">序号</th>
                <th>位置</th>
                <th>项目名称</th>
                <th>规格/品牌</th>
                <th class="center-col">单位</th>
                <th class="center-col">数量(可改)</th>
                <th class="price-col">单价(可改)</th>
                <th class="price-col">总价(元)</th>
                <th>备注(可改)</th>
              </tr>
            </thead>
            <tbody id="hard-tbody">
              <!-- JS Render -->
            </tbody>
          </table>
        </div>
      </div>

      <!-- 软装清单部分 -->
      <div class="content-section" id="soft">
        <h2 class="section-title" style="border: none;">
            <span>软装与家电清单 <span style="font-size: 15px; color: var(--text-main); font-weight: normal; margin-left: 10px;" id="soft-total-title">总计：¥ 0.00</span></span>
            <button class="export-btn" onclick="exportMultipleTables([], Array.from({length: document.querySelectorAll('[id^=soft-table-]').length}).map((_, i) => 'soft-table-' + (i+1)), '软装清单合集')">导出所有软装清单</button>
        </h2>
        <div id="soft-container">
            <!-- JS Render -->
        </div>
      </div>

      <!-- 户型优化部分 -->
      <div class="content-section" id="floorplan">
        <h2 class="section-title">原户型十字中轴线规划</h2>
        <div class="axis-note">
          <h3>十字中轴线设计逻辑</h3>
          <p><strong>竖中轴线（黄色竖线）</strong>：穿过厨房、过道正中心，上下贯穿户型，把户型左右对半拆分。左侧为3个卧室+双卫生间静区（休息区），右侧为客餐厅+双阳台动区（活动区）。装修时沿竖线两侧做原木通顶收纳柜，刚好依托中轴线对称做收纳，消化4.2㎡过道浪费面积。</p>
          <p style="margin-top: 10px;"><strong>横中轴线（黄色横线）</strong>：横穿卫生间A、卧室A、客厅中部，左右贯通全屋。上半区为卧室C、厨卫、北向阳台B，下半区为主卧B、次卧A、客厅+南向阳台A。装修时客餐厅家具沿横线对称摆放，餐桌居中在横线北侧、沙发在横线南侧，保证南北阳台通风对流不被家具遮挡。</p>
        </div>

        <h2 class="section-title">核心户型优化方案</h2>
        <ul class="highlight-list">
          <li><strong>入户玄关优化</strong>：入户右侧做顶天立地原木鞋柜+半高格栅隔断，解决无玄关隐私差问题，同时增加收纳空间。</li>
          <li><strong>过道空间优化</strong>：过道两侧做嵌入式通顶原木收纳柜，深度32cm，不影响通行，把4.2㎡的浪费面积变成实用收纳区。</li>
          <li><strong>厨房采光优化</strong>：把厨房门换成超白长虹玻璃推拉门，让餐厅光线透进厨房，解决暗厨问题，同时不影响厨房油烟隔离。</li>
          <li><strong>次卧噪音优化</strong>：给公卫包下水管贴隔音棉，同时给公卫和次卧C的共用墙做轻钢龙骨+隔音棉+双层石膏板，解决噪音干扰问题。</li>
          <li><strong>全屋收纳优化</strong>：三个卧室做通顶定制衣柜，餐厅做餐边柜，阳台做铝柜，全屋收纳系统最大化利用空间，解决老小区收纳不足问题。</li>
        </ul>
      </div>
    </div>

    <script>
      // 标签切换功能
      const tabs = document.querySelectorAll('.nav-tab');
      const sections = document.querySelectorAll('.content-section');

      tabs.forEach(tab => {
        tab.addEventListener('click', () => {
          const target = tab.dataset.tab;
          tabs.forEach(t => t.classList.remove('active'));
          sections.forEach(s => s.classList.remove('active'));
          tab.classList.add('active');
          document.getElementById(target).classList.add('active');
        });
      });

      // ================== 动态数据加载与渲染 ==================
      const BIN_URL = "https://api.jsonbin.io/v3/b/6a214ec2f5f4af5e29b73145";
      const MASTER_KEY = "$2a$10$jMI2Y8mRfQXL5BnMKITGxuccdUTeFQaFo7NZuiCjF10l8oHycCwQi";
      let appData = { hard_items: [], soft_items: [] };

      function safeVal(val) {
          if(val === null || val === undefined || String(val) === 'nan') return '';
          return String(val).replace('¥', '').trim();
      }

      function parsePrice(val) {
          let s = safeVal(val).replace(/,/g, '');
          let f = parseFloat(s);
          return isNaN(f) ? 0 : f;
      }

      function formatPrice(num) {
          return '¥ ' + num.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
      }

      async function initData() {
          try {
              const response = await fetch(BIN_URL + '/latest', {
                  headers: { "X-Master-Key": MASTER_KEY }
              });
              const json = await response.json();
              if(json.record) {
                  appData = json.record;
                  renderAll();
              }
              document.getElementById('loading-overlay').style.display = 'none';
          } catch(e) {
              alert("加载云端数据失败: " + e.message);
              document.getElementById('loading-overlay').innerText = '加载失败，请刷新重试';
          }
      }

      function renderAll() {
          let hardTotal = 0;
          let softTotal = 0;

          // Render Hard Items
          const hardTbody = document.getElementById('hard-tbody');
          hardTbody.innerHTML = '';
          appData.hard_items.forEach((row, index) => {
              let qty = parsePrice(row["Unnamed: 5"]);
              let price = parsePrice(row["Unnamed: 6"]);
              let total = qty * price;
              hardTotal += total;

              let tr = document.createElement('tr');
              tr.innerHTML = `
                  <td class="center-col">${safeVal(row["万科城市花园105㎡户型装修硬装清单"])}</td>
                  <td>${safeVal(row["Unnamed: 1"])}</td>
                  <td>${safeVal(row["Unnamed: 2"])}</td>
                  <td>${safeVal(row["Unnamed: 3"])}</td>
                  <td class="center-col">${safeVal(row["Unnamed: 4"])}</td>
                  <td class="center-col editable-cell" contenteditable="true" onblur="updateHard(${index}, 'qty', this.innerText)">${safeVal(row["Unnamed: 5"])}</td>
                  <td class="price-col editable-cell" contenteditable="true" onblur="updateHard(${index}, 'price', this.innerText)">${price}</td>
                  <td class="price-col price">${formatPrice(total)}</td>
                  <td class="editable-cell" contenteditable="true" onblur="updateHard(${index}, 'note', this.innerText)">${safeVal(row["Unnamed: 8"])}</td>
              `;
              hardTbody.appendChild(tr);
          });
          
          let trFooter = document.createElement('tr');
          trFooter.style.cssText = "background: var(--primary-light); font-weight: bold;";
          trFooter.innerHTML = `
              <td colspan="7" class="price-col" style="color: var(--primary-dark);">硬装总计：</td>
              <td class="price-col" style="color: var(--primary); font-size: 18px;">${formatPrice(hardTotal)}</td>
              <td></td>
          `;
          hardTbody.appendChild(trFooter);

          // Render Soft Items
          const softContainer = document.getElementById('soft-container');
          softContainer.innerHTML = '';
          
          // Group by location
          let softGroups = {};
          appData.soft_items.forEach(row => {
              let loc = safeVal(row["Unnamed: 1"]);
              if(loc.includes("主卧")) loc = "主卧";
              else if(loc.includes("次卧A")) loc = "次卧A";
              else if(loc.includes("次卧C")) loc = "次卧C";
              else if(loc.includes("卫生间")) loc = "卫生间";
              
              if(!softGroups[loc]) softGroups[loc] = [];
              softGroups[loc].push(row);
          });

          let groupIdx = 0;
          for(let groupName in softGroups) {
              groupIdx++;
              let items = softGroups[groupName];
              let groupTotal = 0;
              let tbodyHtml = '';

              items.forEach(row => {
                  let qty = parsePrice(row["Unnamed: 5"]);
                  let price = parsePrice(row["Unnamed: 6"]);
                  let total = qty * price;
                  groupTotal += total;
                  softTotal += total;
                  
                  // Find index in global array to update correctly
                  let globalIndex = appData.soft_items.indexOf(row);

                  tbodyHtml += `
                    <tr>
                        <td class="center-col">${safeVal(row["万科城市花园105㎡户型装修软装清单"])}</td>
                        <td>${safeVal(row["Unnamed: 1"])}</td>
                        <td>${safeVal(row["Unnamed: 2"])}</td>
                        <td class="editable-cell" contenteditable="true" onblur="updateSoft(${globalIndex}, 'desc', this.innerText)">${safeVal(row["Unnamed: 3"])}</td>
                        <td class="center-col">${safeVal(row["Unnamed: 4"])}</td>
                        <td class="center-col editable-cell" contenteditable="true" onblur="updateSoft(${globalIndex}, 'qty', this.innerText)">${safeVal(row["Unnamed: 5"])}</td>
                        <td class="price-col editable-cell" contenteditable="true" onblur="updateSoft(${globalIndex}, 'price', this.innerText)">${price}</td>
                        <td class="price-col price">${formatPrice(total)}</td>
                        <td class="editable-cell" contenteditable="true" onblur="updateSoft(${globalIndex}, 'note', this.innerText)">${safeVal(row["Unnamed: 8"])}</td>
                    </tr>
                  `;
              });

              let groupDiv = document.createElement('div');
              groupDiv.className = 'category-group';
              groupDiv.innerHTML = `
                  <h3 class="category-title">
                    <span>${groupName}</span>
                    <div class="title-actions">
                      <span style="color: var(--text-main); font-weight: normal; margin-right: 15px;">小计：${formatPrice(groupTotal)}</span>
                      <button class="export-btn" onclick="exportTable('soft-table-${groupIdx}', '${groupName}软装清单')">导出表格</button>
                    </div>
                  </h3>
                  <div class="table-container" style="border: none; border-radius: 0;">
                    <table id="soft-table-${groupIdx}">
                      <thead>
                        <tr>
                          <th class="center-col">序号</th>
                          <th>位置</th>
                          <th>产品名称</th>
                          <th>品牌/规格(可改)</th>
                          <th class="center-col">单位</th>
                          <th class="center-col">数量(可改)</th>
                          <th class="price-col">单价(可改)</th>
                          <th class="price-col">总价(元)</th>
                          <th>备注(可改)</th>
                        </tr>
                      </thead>
                      <tbody>
                        ${tbodyHtml}
                      </tbody>
                    </table>
                  </div>
              `;
              softContainer.appendChild(groupDiv);
          }

          // Update Summaries
          let grandTotal = hardTotal + softTotal;
          document.getElementById('sum-total').innerText = formatPrice(grandTotal);
          document.getElementById('sum-hard').innerText = formatPrice(hardTotal);
          document.getElementById('sum-soft').innerText = formatPrice(softTotal);
          document.getElementById('sum-percent').innerText = ((hardTotal / grandTotal) * 100).toFixed(2) + '%';
          
          document.getElementById('hard-total-title').innerText = '总计：' + formatPrice(hardTotal);
          document.getElementById('soft-total-title').innerText = '总计：' + formatPrice(softTotal);
      }

      function updateHard(index, field, val) {
          if(field === 'qty') appData.hard_items[index]["Unnamed: 5"] = val;
          if(field === 'price') appData.hard_items[index]["Unnamed: 6"] = val;
          if(field === 'note') appData.hard_items[index]["Unnamed: 8"] = val;
          // Re-render to update totals automatically
          renderAll();
      }

      function updateSoft(index, field, val) {
          if(field === 'desc') appData.soft_items[index]["Unnamed: 3"] = val;
          if(field === 'qty') appData.soft_items[index]["Unnamed: 5"] = val;
          if(field === 'price') appData.soft_items[index]["Unnamed: 6"] = val;
          if(field === 'note') appData.soft_items[index]["Unnamed: 8"] = val;
          renderAll();
      }

      async function saveData() {
          const btn = document.getElementById('save-all-btn');
          btn.innerText = "⏳ 正在保存至云端...";
          btn.disabled = true;

          try {
              // Update calculation fields
              appData.hard_items.forEach(r => r["Unnamed: 7"] = parsePrice(r["Unnamed: 5"]) * parsePrice(r["Unnamed: 6"]));
              appData.soft_items.forEach(r => r["Unnamed: 7"] = parsePrice(r["Unnamed: 5"]) * parsePrice(r["Unnamed: 6"]));

              const res = await fetch(BIN_URL, {
                  method: "PUT",
                  headers: {
                      "Content-Type": "application/json",
                      "X-Master-Key": MASTER_KEY
                  },
                  body: JSON.stringify(appData)
              });
              
              if(res.ok) {
                  alert("🎉 恭喜！保存成功！所有人刷新页面都可以看到你的最新修改。");
              } else {
                  alert("保存失败，HTTP状态码: " + res.status);
              }
          } catch(e) {
              alert("保存报错: " + e.message);
          } finally {
              btn.innerText = "💾 保存所有修改至云端";
              btn.disabled = false;
          }
      }

      // ================== 导出 CSV 功能 ==================
      function exportTableToCSV(tableIds, filename) {
        let csv = [];
        tableIds.forEach((id, index) => {
           const table = document.getElementById(id);
           if(!table) return;

           if (tableIds.length > 1) {
               let tableName = "清单";
               if (id === 'hard-table') tableName = "硬装清单";
               else {
                   let titleNode = table.closest('.category-group');
                   if(titleNode) {
                       tableName = titleNode.querySelector('.category-title span').innerText + " 软装清单";
                   }
               }
               csv.push(tableName);
           }
           
           const rows = table.querySelectorAll('tr');
           for (let i = 0; i < rows.length; i++) {
               let row = [], cols = rows[i].querySelectorAll('td, th');
               for (let j = 0; j < cols.length; j++) {
                   let data = cols[j].innerText.replace(/(\\r\\n|\\n|\\r)/gm, '').replace(/(\\s\\s)/gm, ' ');
                   if (data.includes('¥')) {
                       data = data.replace(/¥/g, '').replace(/,/g, '').trim();
                   }
                   data = data.replace(/"/g, '""');
                   row.push('"' + data + '"');
               }
               csv.push(row.join(','));
           }
           if (index < tableIds.length - 1) csv.push(""); 
        });

        downloadCSV(csv.join('\\n'), filename);
      }

      function downloadCSV(csv, filename) {
        let csvFile = new Blob(["\\ufeff", csv], {type: "text/csv;charset=utf-8"});
        let downloadLink = document.createElement("a");
        downloadLink.download = filename + '.csv';
        downloadLink.href = window.URL.createObjectURL(csvFile);
        downloadLink.style.display = "none";
        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
      }

      function exportTable(tableId, filename) {
          exportTableToCSV([tableId], filename);
      }
      
      function exportMultipleTables(hardIds, softIds, filename) {
          exportTableToCSV([...hardIds, ...softIds], filename);
      }

      // 启动
      initData();
    </script>
  </body>
</html>
"""

with open('list.html', 'w', encoding='utf-8') as f:
    f.write(html_template)
