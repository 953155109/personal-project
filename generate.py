import json
from collections import defaultdict

data = json.load(open('temp_excel_data.json', encoding='utf-8'))

hard_items = data['硬装清单'][1:-1]
soft_items = data['软装清单'][1:-1]

# Adjust budgets based on user request
for row in soft_items:
    name = str(row.get('Unnamed: 2', ''))
    desc = str(row.get('Unnamed: 3', ''))
    
    # 扫地机器人预算调整为 4000 (原为 清洁用品套装 2000)
    if '扫地机器人' in name or '扫地机器人' in desc:
        row['Unnamed: 6'] = 4000
        row['Unnamed: 7'] = 4000
    
    # 洗碗机预算为 4000 (原为 洗碗机 2500)
    if '洗碗机' in name or '洗碗机' in desc:
        row['Unnamed: 6'] = 4000
        row['Unnamed: 7'] = 4000

# 添加洗烘套装 6000
washer_dryer = {
    '万科城市花园105㎡户型装修软装清单': '-',
    'Unnamed: 1': '阳台',
    'Unnamed: 2': '洗烘套装',
    'Unnamed: 3': '预估',
    'Unnamed: 4': '套',
    'Unnamed: 5': 1,
    'Unnamed: 6': 6000,
    'Unnamed: 7': 6000,
    'Unnamed: 8': '补充项'
}
soft_items.append(washer_dryer)

# 添加晾衣架 300
drying_rack = {
    '万科城市花园105㎡户型装修软装清单': '-',
    'Unnamed: 1': '阳台',
    'Unnamed: 2': '晾衣架',
    'Unnamed: 3': '预估',
    'Unnamed: 4': '个',
    'Unnamed: 5': 1,
    'Unnamed: 6': 300,
    'Unnamed: 7': 300,
    'Unnamed: 8': '新增'
}
soft_items.append(drying_rack)

# 添加抽油烟机 3000
range_hood = {
    '万科城市花园105㎡户型装修软装清单': '-',
    'Unnamed: 1': '厨房',
    'Unnamed: 2': '抽油烟机',
    'Unnamed: 3': '预估',
    'Unnamed: 4': '台',
    'Unnamed: 5': 1,
    'Unnamed: 6': 3000,
    'Unnamed: 7': 3000,
    'Unnamed: 8': '新增'
}
soft_items.append(range_hood)

# 添加煤气灶 1500
gas_stove = {
    '万科城市花园105㎡户型装修软装清单': '-',
    'Unnamed: 1': '厨房',
    'Unnamed: 2': '煤气灶',
    'Unnamed: 3': '预估',
    'Unnamed: 4': '台',
    'Unnamed: 5': 1,
    'Unnamed: 6': 1500,
    'Unnamed: 7': 1500,
    'Unnamed: 8': '新增'
}
soft_items.append(gas_stove)


def clean_price(v):
    if isinstance(v, str):
        v = v.replace('¥', '').replace(',', '')
    return float(v)

def safe_val(row, key):
    val = row.get(key, '')
    if val is None or str(val) == 'nan':
        return ''
    return str(val).replace('¥', '')

hard_html = ''
hard_total = 0
for row in hard_items:
    price = clean_price(row['Unnamed: 7'])
    hard_total += price
    hard_html += f'<tr><td class="center-col">{safe_val(row, "万科城市花园105㎡户型装修硬装清单")}</td><td>{safe_val(row, "Unnamed: 1")}</td><td>{safe_val(row, "Unnamed: 2")}</td><td>{safe_val(row, "Unnamed: 3")}</td><td class="center-col">{safe_val(row, "Unnamed: 4")}</td><td class="center-col">{safe_val(row, "Unnamed: 5")}</td><td class="price-col">¥ {float(clean_price(safe_val(row, "Unnamed: 6"))):,.2f}</td><td class="price-col price">¥ {price:,.2f}</td><td>{safe_val(row, "Unnamed: 8")}</td></tr>\n'

def normalize_location(loc):
    if "主卧" in loc: return "主卧"
    if "次卧A" in loc: return "次卧A"
    if "次卧C" in loc: return "次卧C"
    if "卫生间" in loc: return "卫生间"
    return loc

soft_groups = defaultdict(list)
for row in soft_items:
    loc = safe_val(row, "Unnamed: 1")
    norm_loc = normalize_location(loc)
    soft_groups[norm_loc].append(row)

soft_html = ''
soft_total = 0
group_idx = 0
for group_name, items in soft_groups.items():
    group_idx += 1
    group_total = sum(clean_price(r['Unnamed: 7']) for r in items)
    soft_total += group_total
    
    soft_html += f'''
        <div class="category-group">
          <h3 class="category-title">
            <span>{group_name}</span>
            <div class="title-actions">
              <span style="color: var(--text-main); font-weight: normal; margin-right: 15px;">小计：¥ {group_total:,.2f}</span>
              <button class="export-btn" onclick="exportTable('soft-table-{group_idx}', '{group_name}软装清单')">导出表格</button>
            </div>
          </h3>
          <div class="table-container" style="border: none; border-radius: 0;">
            <table id="soft-table-{group_idx}">
              <thead>
                <tr>
                  <th class="center-col">序号</th>
                  <th>位置</th>
                  <th>产品名称</th>
                  <th>品牌/规格</th>
                  <th class="center-col">单位</th>
                  <th class="center-col">数量</th>
                  <th class="price-col">单价(元)</th>
                  <th class="price-col">总价(元)</th>
                  <th>备注</th>
                </tr>
              </thead>
              <tbody>
'''
    for row in items:
        price = clean_price(row['Unnamed: 7'])
        soft_html += f'<tr><td class="center-col">{safe_val(row, "万科城市花园105㎡户型装修软装清单")}</td><td>{safe_val(row, "Unnamed: 1")}</td><td>{safe_val(row, "Unnamed: 2")}</td><td>{safe_val(row, "Unnamed: 3")}</td><td class="center-col">{safe_val(row, "Unnamed: 4")}</td><td class="center-col">{safe_val(row, "Unnamed: 5")}</td><td class="price-col">¥ {float(clean_price(safe_val(row, "Unnamed: 6"))):,.2f}</td><td class="price-col price">¥ {price:,.2f}</td><td>{safe_val(row, "Unnamed: 8")}</td></tr>\n'
    
    soft_html += '''
              </tbody>
            </table>
          </div>
        </div>
'''

total_budget = hard_total + soft_total

html_template = f"""<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>万科城市花园105㎡户型装修方案</title>
    <style>
      :root {{
        --primary: #8b7355;
        --primary-light: #f5f1eb;
        --primary-dark: #6b583f;
        --text-main: #333333;
        --text-light: #666666;
        --border: #e0d9cf;
        --bg-color: #faf8f5;
        --white: #ffffff;
      }}

      body {{
        font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
        background-color: var(--bg-color);
        color: var(--text-main);
        margin: 0;
        padding: 40px 20px;
      }}

      .container {{
        max-width: 1200px;
        margin: 0 auto;
        background: var(--white);
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(139, 115, 85, 0.08);
        overflow: hidden;
      }}

      .header {{
        text-align: center;
        padding: 40px 20px 30px;
        background-color: var(--white);
      }}

      .header h1 {{
        font-size: 32px;
        color: var(--primary);
        margin-bottom: 10px;
        letter-spacing: 2px;
      }}

      .header p {{
        color: var(--text-light);
        font-size: 16px;
      }}

      .nav-tabs {{
        display: flex;
        background: var(--bg-color);
        border-bottom: 1px solid var(--border);
        border-top: 1px solid var(--border);
      }}

      .nav-tab {{
        flex: 1;
        padding: 16px 20px;
        text-align: center;
        cursor: pointer;
        font-size: 16px;
        font-weight: 500;
        color: var(--text-light);
        transition: all 0.3s ease;
      }}

      .nav-tab.active {{
        background: var(--white);
        color: var(--primary);
        border-bottom: 3px solid var(--primary);
      }}

      .nav-tab:hover {{
        background: var(--primary-light);
        color: var(--primary);
      }}

      .content-section {{
        padding: 40px;
        display: none;
      }}

      .content-section.active {{
        display: block;
      }}

      .section-title {{
        color: var(--primary);
        border-bottom: 2px solid var(--primary-light);
        padding-bottom: 15px;
        margin-top: 0;
        margin-bottom: 25px;
        font-size: 22px;
        display: flex;
        justify-content: space-between;
        align-items: center;
      }}

      .summary-cards {{
        display: flex;
        gap: 20px;
        margin-bottom: 40px;
        flex-wrap: wrap;
      }}

      .card {{
        flex: 1;
        min-width: 200px;
        background: var(--white);
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(139, 115, 85, 0.08);
        text-align: center;
        border-top: 4px solid var(--primary);
      }}

      .card h3 {{
        margin: 0 0 10px 0;
        font-size: 16px;
        color: var(--text-light);
        font-weight: normal;
      }}

      .card .amount {{
        font-size: 28px;
        font-weight: bold;
        color: var(--primary);
      }}

      .category-group {{
        margin-bottom: 30px;
        background: var(--white);
        border-radius: 8px;
        border: 1px solid var(--border);
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
      }}

      .category-title {{
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
      }}
      
      .title-actions {{
        display: flex;
        align-items: center;
      }}

      .export-btn {{
        background: var(--primary);
        color: var(--white);
        border: none;
        padding: 6px 16px;
        border-radius: 4px;
        font-size: 14px;
        cursor: pointer;
        transition: background 0.3s;
        margin-left: 10px;
      }}
      
      .export-btn:hover {{
        background: var(--primary-dark);
      }}

      .table-container {{
        overflow-x: auto;
        border-radius: 8px;
        border: 1px solid var(--border);
      }}

      table {{
        width: 100%;
        border-collapse: collapse;
      }}

      table thead tr {{
        background: var(--primary-light);
      }}

      table th, table td {{
        padding: 12px 15px;
        text-align: left;
        border-bottom: 1px dashed var(--border);
        font-size: 15px;
      }}

      table th {{
        color: var(--primary-dark);
        font-weight: bold;
        font-size: 14px;
        border-bottom: 1px solid var(--border);
      }}
      
      table tbody tr:nth-child(even) {{
        background: #fafafa;
      }}

      table tbody tr:hover {{
        background: var(--primary-light);
      }}

      .price-col {{
        text-align: right;
      }}

      .price {{
        font-weight: bold;
        color: var(--text-main);
      }}
      
      .center-col {{
        text-align: center;
      }}

      .highlight-list {{
        font-size: 15px;
        line-height: 2;
        color: var(--text-light);
        margin-left: 20px;
      }}
      
      .highlight-list li {{
        margin-bottom: 8px;
      }}

      .highlight-list strong {{
        color: var(--primary-dark);
      }}

      .floor-plan {{
        max-width: 100%;
        border-radius: 8px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 30px;
      }}

      .axis-note {{
        background: var(--primary-light);
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 30px;
        border-left: 4px solid var(--primary);
      }}

      .axis-note h3 {{
        font-size: 18px;
        color: var(--primary-dark);
        margin-top: 0;
        margin-bottom: 15px;
      }}

      .axis-note p {{
        font-size: 15px;
        color: var(--text-main);
        line-height: 1.8;
      }}

      @media (max-width: 768px) {{
        .summary-cards {{
          flex-direction: column;
        }}
        .content-section {{
          padding: 20px;
        }}
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <div class="header">
        <h1>万科城市花园105㎡户型装修方案</h1>
        <p>原木风设计 | 基于户型图、报价单及家电软装预估清单综合整理</p>
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
            <button class="export-btn" onclick="exportMultipleTables(['hard-table'], Array.from({{length: {group_idx}}}).map((_, i) => 'soft-table-' + (i+1)), '全部预算清单')">导出全部清单</button>
        </h2>
        <div class="summary-cards">
          <div class="card">
            <h3>总预算预估 (硬装+软装电器)</h3>
            <div class="amount">¥ {total_budget:,.2f}</div>
          </div>
          <div class="card">
            <h3>硬装部分合计</h3>
            <div class="amount">¥ {hard_total:,.2f}</div>
          </div>
          <div class="card">
            <h3>软装及家电合计</h3>
            <div class="amount">¥ {soft_total:,.2f}</div>
          </div>
          <div class="card">
            <h3>硬装占比</h3>
            <div class="amount">{hard_total/total_budget*100:.2f}%</div>
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
            <span>硬装预算清单 <span style="font-size: 15px; color: var(--text-main); font-weight: normal; margin-left: 10px;">总计：¥ {hard_total:,.2f}</span></span>
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
                <th class="center-col">数量</th>
                <th class="price-col">单价(元)</th>
                <th class="price-col">总价(元)</th>
                <th>备注</th>
              </tr>
            </thead>
            <tbody>
              {hard_html}
              <tr style="background: var(--primary-light); font-weight: bold;">
                  <td colspan="7" class="price-col" style="color: var(--primary-dark);">硬装总计：</td>
                  <td class="price-col" style="color: var(--primary); font-size: 18px;">¥ {hard_total:,.2f}</td>
                  <td></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 软装清单部分 -->
      <div class="content-section" id="soft">
        <h2 class="section-title" style="border: none;">
            <span>软装与家电清单 <span style="font-size: 15px; color: var(--text-main); font-weight: normal; margin-left: 10px;">总计：¥ {soft_total:,.2f}</span></span>
            <button class="export-btn" onclick="exportMultipleTables([], Array.from({{length: {group_idx}}}).map((_, i) => 'soft-table-' + (i+1)), '软装清单合集')">导出所有软装清单</button>
        </h2>
        {soft_html}
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

      tabs.forEach(tab => {{
        tab.addEventListener('click', () => {{
          const target = tab.dataset.tab;
          // 移除所有active类
          tabs.forEach(t => t.classList.remove('active'));
          sections.forEach(s => s.classList.remove('active'));
          // 添加active类
          tab.classList.add('active');
          document.getElementById(target).classList.add('active');
        }});
      }});

      // 导出CSV功能
      function exportTableToCSV(tableIds, filename) {{
        let csv = [];
        
        tableIds.forEach((id, index) => {{
           const table = document.getElementById(id);
           if(!table) return;

           // 加入表头区分(如果有多个表)
           if (tableIds.length > 1) {{
               let tableName = "清单";
               if (id === 'hard-table') tableName = "硬装清单";
               else {{
                   let titleNode = table.closest('.category-group');
                   if(titleNode) {{
                       tableName = titleNode.querySelector('.category-title span').innerText + " 软装清单";
                   }}
               }}
               csv.push(tableName);
           }}
           
           const rows = table.querySelectorAll('tr');
           for (let i = 0; i < rows.length; i++) {{
               let row = [], cols = rows[i].querySelectorAll('td, th');
               for (let j = 0; j < cols.length; j++) {{
                   let data = cols[j].innerText.replace(/(\\r\\n|\\n|\\r)/gm, '').replace(/(\\s\\s)/gm, ' ');
                   if (data.includes('¥')) {{
                       data = data.replace(/¥/g, '').replace(/,/g, '').trim();
                   }}
                   data = data.replace(/"/g, '""');
                   row.push('"' + data + '"');
               }}
               csv.push(row.join(','));
           }}
           // 在多表之间加空行
           if (index < tableIds.length - 1) csv.push(""); 
        }});

        downloadCSV(csv.join('\\n'), filename);
      }}

      function downloadCSV(csv, filename) {{
        let csvFile;
        let downloadLink;
        csvFile = new Blob(["\\ufeff", csv], {{type: "text/csv;charset=utf-8"}});
        downloadLink = document.createElement("a");
        downloadLink.download = filename + '.csv';
        downloadLink.href = window.URL.createObjectURL(csvFile);
        downloadLink.style.display = "none";
        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
      }}

      function exportTable(tableId, filename) {{
          exportTableToCSV([tableId], filename);
      }}
      
      function exportMultipleTables(hardIds, softIds, filename) {{
          exportTableToCSV([...hardIds, ...softIds], filename);
      }}
    </script>
  </body>
</html>
"""

with open('list.html', 'w', encoding='utf-8') as f:
    f.write(html_template)
