## 教务处成绩查询 web 应用
- python3.5
- 安装依赖后`python score_web_app.py` 运行
- 默认服务0.0.0.0:5000端口

### 请求方法：
#### post：
- 地址：`/get_scores`
- 表单需要内容: `student_id`, `password`
- 返回：成绩列表

### 安装依赖
- pip install -r requirements.txt