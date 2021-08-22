## 手动执行翻译步骤

### 1. extract file
`pybabel extract -F core/i18n/babel.cfg -k lazy_gettext -o core/i18n/messages.pot app`
### 2. 初始化翻译目录（如果不存在翻译目录需要处理一下）
`pybabel init -i core/i18n/messages.pot -d core/i18n/ -l zh_CN`
### 3. 同步翻译
`pybabel update -i core/i18n/messages.pot -d core/i18n/`
### 4. 编译翻译文件
- 修改翻译前置文件，比如中文就是：`core/i18n/zh_CN/LC_MESSAGES/messages.po`，完成缺少的翻译内容

- 编译：`pybabel compile -d core/i18n/`