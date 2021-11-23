# 导入pymysql模块
import pymysql
# 连接database
conn = pymysql.connect(host='localhost', user='root',password='123456',database='article',charset='utf8')
# 得到一个可以执行SQL语句的光标对象
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
# 定义要执行的SQL语句
sql = "INSERT INTO g_yq_source_twitter(twitter_id,twitter_name,twitter_account) VALUES (%s,%s,%s);"
twitter_name='琉球(沖縄)を世界へ＠相互'
twitter_account='TANOSHIBAR'
twitter_id='TANOSHIBAR'
# 执行SQL语句
cursor.execute(sql, [twitter_id,twitter_name,twitter_account])
conn.commit()

# 关闭光标对象
cursor.close()
# 关闭数据库连接
conn.close()