# Front end of my dictionary

## Features

- Query word and show the details,查询到以后可以选择是否加入生词本
- A sheet which record unknown words，可以提供各种排序，生词本的信息从单词表中查询
- Add a word to this sheet，加入生词本

## Tech

- React

## 生词本
表结构：id, word_id(单词表的外键),create_time,update_time,is_delete

前后端暂时不分离，直接使用前端代码操作本地数据库

单词本在本地postgresql的english库stardict表