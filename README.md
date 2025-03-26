<div align="center">
<img src="readme_src/logo.svg" width="160px" />
# infinity client WebUI v1.0.0
</div>

#### 项目介绍
infinity client WebUI 是一个基于vue3的webUI，用于管理
<a href="https://github.com/infiniflow/infinity" target="_blank">infinity vector db</a>
数据库。

#### 软件特点
1.  支持多用户管理
2.  支持多数据库管理

#### 路线图
1. [v1.0.1] 支持 match_sparse 查询 
2. [v1.0.1] 支持 match_dense 查询
3. [v1.0.1] 支持 match_text 查询
4. [v1.0.1] 支持 highlight 查询
5. [v1.0.1]个人数据库连接管理，查看连接数和手动关闭连接
6. [v1.0.2] 支持 索引管理


#### 软件架构
```
底层框架：vue3 + typescript + vite + fastapi + uvicorn + Sqlite3
UI框架：element-plus
python版本：3.11
uv版本：uv 0.6.5
数据库：infinity vector v0.6.0-dev3
nodejs：v22.14.0
npm: 10.9.2
```

#### 安装教程

1.  安装UV
```
pip install uv
```
2.  进入项目目录
```
cd infinity-client
```
3.  安装依赖
```
uv sync
cd web
npm i
npm run build
```
4.  启动项目
```
python main.py
```
5.  打开浏览器访问
```
http://localhost:8000
```

#### 使用说明

1.  本系统是一个多用户系统，每个用户可以创建多个数据库配置，可以同时管理多个数据库，仅支持单机管理，不支持集群管理。
2.  登录注册
<img src="readme_src/login.png" width="500px">
3.  主页
<img src="readme_src/home.jpg" width="500px">
4.  数据库配置
<img src="readme_src/db_config.png" width="500px">
5.  数据库管理
<img src="readme_src/manage.png" width="500px">
6.  新增表
<img src="readme_src/new_table.png" width="500px">
7.  表管理与数据管理
<img src="readme_src/table_manage.png" width="500px">

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request
5.  test
6.  git config user.name "xxx"
7.  git config user.email "xxx@xxx.com"

#### 贡献者
[![contributors](https://contrib.rocks/image?repo=openmty/infinity-client-webui)](https://github.com/openmty/infinity-client-webui/graphs/contributors)
