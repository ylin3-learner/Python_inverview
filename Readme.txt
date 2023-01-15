管理員

新聞編輯；
type_dao: t_type
news_dao: insert -添加新聞 -> news_service
user_dao: 根據用戶名 查詢 用戶id -> user_id - editor_id -> news_service.insert

如果新聞級別大於0, 並且前提管理員審核通過後, 才可以保存到redis內
而管理員可以獲取新聞id -> 查詢新聞內文(news_dao.search_cache())
同時保存到mysql, redis裡 -> redis pool(redis_db) -> redis 無法引用資料(主鍵值), 所以只能保存明確內容
-> 數據{title, author, type, content, is_top, create_time} -redis_news_dao
-> 利用news_service文件, 同時管理redis和mysql存入

將緩存數據刪掉 -> redis_news_dao.delete -> 更改新聞：根據新聞id, 查找新聞 -> news_dao.search_by_id

編輯新聞；如果此新聞被修改過, 無論是否審核通過, 都要變成"待審核"狀態 -> redis緩存紀錄必須刪除
-> 再次審核通過 -> 緩存紀錄

刪除新聞：刪除新聞從mongo, mysql
