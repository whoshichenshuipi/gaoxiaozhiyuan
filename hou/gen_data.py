import random

def gen_sql():
    universities = [
        ("清华大学", "985/211/双一流", "北京"), ("北京大学", "985/211/双一流", "北京"),
        ("复旦大学", "985/211/双一流", "上海"), ("上海交通大学", "985/211/双一流", "上海"),
        ("中山大学", "985/211/双一流", "广东"), ("华南理工大学", "985/211/双一流", "广东"),
        ("浙江大学", "985/211/双一流", "浙江"), ("南京大学", "985/211/双一流", "江苏"),
        ("武汉大学", "985/211/双一流", "湖北"), ("华中科技大学", "985/211/双一流", "湖北"),
        ("西安交通大学", "985/211/双一流", "陕西"), ("哈尔滨工业大学", "985/211/双一流", "黑龙江"),
        ("四川大学", "985/211/双一流", "四川"), ("吉林大学", "985/211/双一流", "吉林"),
        ("南开大学", "985/211/双一流", "天津"), ("天津大学", "985/211/双一流", "天津"),
        ("山东大学", "985/211/双一流", "山东"), ("中南大学", "985/211/双一流", "湖南"),
        ("厦门大学", "985/211/双一流", "福建"), ("东南大学", "985/211/双一流", "江苏"),
        ("北京航空航天大学", "985/211/双一流", "北京"), ("同济大学", "985/211/双一流", "上海"),
        ("北京师范大学", "985/211/双一流", "北京"), ("中国科学技术大学", "985/211/双一流", "安徽"),
        ("中国人民大学", "985/211/双一流", "北京"), ("中国农业大学", "985/211/双一流", "北京"),
        ("北京理工大学", "985/211/双一流", "北京"), ("大连理工大学", "985/211/双一流", "辽宁"),
        ("东北大学", "985/211/双一流", "辽宁"), ("华东师范大学", "985/211/双一流", "上海"),
        ("兰州大学", "985/211/双一流", "甘肃"), ("重庆大学", "985/211/双一流", "重庆"),
        ("湖南大学", "985/211/双一流", "湖南"), ("电子科技大学", "985/211/双一流", "四川"),
        ("西北工业大学", "985/211/双一流", "陕西"), ("中国海洋大学", "985/211/双一流", "山东"),
        ("中央民族大学", "985/211/双一流", "北京"), ("华南师范大学", "211/双一流", "广东"),
        ("暨南大学", "211/双一流", "广东"), ("深圳大学", "一本", "广东"),
        ("广东工业大学", "一本", "广东"), ("南方科技大学", "双一流", "广东"),
        ("广州大学", "一本", "广东"), ("汕头大学", "一本", "广东"),
        ("安徽大学", "211/双一流", "安徽"), ("福州大学", "211/双一流", "福建"),
        ("南昌大学", "211/双一流", "江西"), ("河南大学", "双一流", "河南"),
        ("湖北大学", "一本", "湖北"), ("苏州大学", "211/双一流", "江苏"),
    ]
    
    # Pad to 230 universities
    idx = 1
    while len(universities) < 230:
        names = ["科技大学", "理工大学", "师范大学", "工业大学", "财经大学", "医科大学", "交通大学", "大学", "农林大学", "建筑大学", "轻工业大学", "工程大学", "艺术大学"]
        city_prefix = ["宁海", "临安", "海西", "漠北", "龙江", "青山", "白云", "凤城", "灵山", "星海", "南华", "北辰", "东岭", "西沧", "中云", "广川", "平阳", "高邮", "定山", "洛水"]
        uni_name = random.choice(city_prefix) + random.choice(names)
        if uni_name in [x[0] for x in universities]:
            uni_name += str(idx)
            idx += 1
        universities.append((uni_name, random.choice(["一本", "二本", "双一流"]), random.choice(["浙江", "江苏", "广东", "山东", "河南"])))

    majors_base = [
        ("计算机科学与技术", "工学", "计算机类"), ("人工智能", "工学", "计算机类"),
        ("软件工程", "工学", "计算机类"), ("大数据技术", "工学", "计算机类"),
        ("电子信息工程", "工学", "电子信息类"), ("自动化", "工学", "自动化类"),
        ("机械设计制造及其自动化", "工学", "机械类"), ("法学", "法学", "法学类"),
        ("金融学", "经济学", "金融学类"), ("经济学", "经济学", "经济学类"),
        ("土木工程", "工学", "土木类"), ("临床医学", "医学", "临床医学类"),
        ("电气工程及其自动化", "工学", "电气类"), ("通信工程", "工学", "电子信息类"),
        ("工商管理", "管理学", "工商管理类"), ("会计学", "管理学", "工商管理类"),
        ("汉语言文学", "文学", "中国语言文学类"), ("英语", "文学", "外国语言文学类"),
        ("物理学", "理学", "物理学类"), ("化学", "理学", "化学科学类"),
    ]
    # Pad to 110 majors
    idx = 1
    while len(majors_base) < 110:
        extra_names = ["统计学", "社会学", "翻译", "数学与应用数学", "预防医学", "护理学", "药学", "环境工程", "材料科学与工程", "测绘工程", "心理学", "建筑学"]
        name = random.choice(extra_names)
        if name in [x[0] for x in majors_base]:
            name += str(idx)
            idx += 1
        majors_base.append((name, random.choice(["理学", "工学", "医学", "管理学"]), "其他类别"))

    sql_output = []
    
    # 1. University
    sql_output.append("-- University (230 records)")
    for i, (name, level, region) in enumerate(universities, 1):
        sql_output.append(f"INSERT INTO university (id, name, level, region, intro, official_url, status) VALUES ({i}, '{name}', '{level}', '{region}', '{name}是一所具有悠久历史的高等学府...', 'http://www.{i}.edu.cn', 1);")

    # 2. Major (Each uni has subset of majors)
    sql_output.append("\n-- Major (110 records)")
    all_major_refs = []
    for i, (name, category, discipline) in enumerate(majors_base, 1):
        uni_id = (i % 230) + 1
        all_major_refs.append((i, uni_id))
        sql_output.append(f"INSERT INTO major (id, name, category, discipline, intro, university_id) VALUES ({i}, '{name}', '{category}', '{discipline}', '{name}专业致力于培养高素质人才...', {uni_id});")

    # 3. Admission Score (2500+ records)
    sql_output.append("\n-- Admission Score (2500 records)")
    provinces = ["广东", "北京", "江苏", "浙江", "山东", "河南", "湖北", "四川"]
    count = 0
    for u_id in range(1, 231):
        # assign 10-12 score records per university across different majors and provinces
        for year in [2022, 2023]:
            for p in random.sample(provinces, 3):
                m_id = random.randint(1, 110)
                min_score = random.randint(550, 680)
                min_rank = (700 - min_score) * 100 + random.randint(1, 100)
                count += 1
                sql_output.append(f"INSERT INTO admission_score (id, university_id, major_id, year, province, min_score, min_rank, avg_score, plan_num, status) VALUES ({count}, {u_id}, {m_id}, {year}, '{p}', {min_score}, {min_rank}, {min_score + 5}, {random.randint(10, 50)}, 1);")
                if count >= 2500: break
            if count >= 2500: break
        if count >= 2500: break

    # 4. Users & Students (50 records + 1 Admin)
    sql_output.append("\n-- Users & Student Profiles (50 records + 1 Admin)")
    pwd_hash = "$2b$12$jK94or/VUSvazdcn.LGFluAwHA2.axZpEVHfcV4EomAUJElj.GCO2" # hash for '123456'
    
    # Add Admin
    sql_output.append(f"INSERT INTO sys_user (id, username, password_hash, role, status, create_time) VALUES (1, 'admin', '{pwd_hash}', 'admin', 1, '2023-12-01 09:00:00');")
    
    for i in range(1, 51):
        sql_output.append(f"INSERT INTO sys_user (id, username, password_hash, role, status, create_time) VALUES ({i+100}, 'student{i}', '{pwd_hash}', 'student', 1, '2023-12-01 10:00:00');")
        sql_output.append(f"INSERT INTO student_profile (id, user_id, score, province, subject_selection, region_preference) VALUES ({i}, {i+100}, {random.randint(580, 650)}, '广东', '物理类', '广东');")

    # 5. Volunteer Plans (200 records)
    sql_output.append("\n-- Volunteer Plan (200 records)")
    for i in range(1, 201):
        u_id = random.randint(1, 230)
        m_id = random.randint(1, 110)
        user_id = (i % 50) + 101
        sql_output.append(f"INSERT INTO volunteer_plan (id, user_id, type, university_id, major_id, priority, create_time) VALUES ({i}, {user_id}, '{random.choice(['备选库', '模拟方案'])}', {u_id}, {m_id}, {random.randint(1, 100)}, '2024-01-10 15:00:00');")

    with open(r'b:\python-xm\gaokaozhiyuan\hou\init_data.sql', 'w', encoding='utf-8') as f:
        f.write('\n'.join(sql_output))

if __name__ == '__main__':
    gen_sql()
