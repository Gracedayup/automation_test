# automation_test

### 项目结构

------

- base：基础请求类
- common：公共模块
- config：配置文件
- db：数据库处理
- logs：日志目录
- page_locators：页面元素定位
- page_objects：页面映射对象
- reports：测试报告
- test_case：测试用例
- test_data：测试所需的测试数据目录
- utils：工具类
- verificode：验证码图片目录

### 概况

------



- 本项目支持接口自动化、web ui自动化测试
- 本项目由以下工具组成：
  - pytest：python的一个单元测试框架,https://docs.pytest.org/en/latest/
  - pytest-xdist：pytest的一个插件,可多进程同时执行测试用例,https://github.com/pytest-dev/pytest-xdist
  - allure-pytest：用于生成测试报告,http://allure.qatools.ru/
  - requests：http请求框架,http://docs.python-requests.org/en/master/
  - selenium：web ui自动化测试框架,https://www.seleniumhq.org/
  - PyMySQL：用于操作MySQL数据库,https://github.com/PyMySQL/PyMySQL
  - paramiko：ssh客户端,http://docs.paramiko.org/en/2.4/
  - ddddocr：用于图片处理,https://github.com/sml2h3/ddddocr

### 使用

------



#### 1、安装python依赖模块

- pip install -r requirements.txt

#### 2、安装allure

- 源安装
  * sudo apt-add-repository ppa:qameta/allure
  * sudo apt-get update 
  * sudo apt-get install allure
  * 其他安装方式：https://github.com/allure-framework/allure2
- 手动安装
  * 下载2.7.0版本:https://github.com/allure-framework/allure2/releases
  * 解压allure-2.7.0.zip
  * 加入系统环境变量:export PATH=/home/john/allure-2.7.0/bin:$PATH

#### 3、selenium安装

##### 3.1、安装jdk1.8，并配置环境变量

##### 3.2、安装配置selenium

* 配置selenium server
  * 下载selenium-server-standalone-3.141.0.jar
  * 下载地址:http://selenium-release.storage.googleapis.com/index.html
  * 以管理员身份启动服务:java -jar selenium-server-standalone-3.141.0.jar -log selenium.log
* 下载浏览器驱动
  * 谷歌浏览器：https://chromedriver.storage.googleapis.com/index.html
    * 驱动支持的最低浏览器版本：https://raw.githubusercontent.com/appium/appium-chromedriver/master/config/mapping.json
  * 火狐浏览器：https://github.com/mozilla/geckodriver/
    * 驱动支持的浏览器版本：https://firefox-source-docs.mozilla.org/testing/geckodriver/geckodriver/Support.html
  * IE浏览器(建议使用32位,64位操作极慢)：http://selenium-release.storage.googleapis.com/index.html





