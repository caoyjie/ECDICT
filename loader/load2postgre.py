import pandas as pd
import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values

# CSV文件路径
path = "stardict.csv"

# 读取CSV文件
df = pd.read_csv(path)
print("CSV文件前10行数据：")
print(df.head(10))

# PostgreSQL连接配置
db_config = {
    'host': 'localhost',
    'port': 5432,
    'user': 'postgres',
    'password': '123456',
    'database': 'english'
}

# 连接到PostgreSQL
try:
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    print("成功连接到PostgreSQL数据库")
    
    # 检查表是否存在
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = 'stardict'
        );
    """)
    table_exists = cursor.fetchone()[0]
    
    if not table_exists:
        print("表不存在，开始创建表...")
        
        # 获取DataFrame的列信息来创建表结构
        columns = []
        for col_name, dtype in zip(df.columns, df.dtypes):
            # 映射pandas数据类型到PostgreSQL数据类型
            if dtype == 'int64':
                pg_type = 'BIGINT'
            elif dtype == 'float64':
                pg_type = 'DOUBLE PRECISION'
            elif dtype == 'bool':
                pg_type = 'BOOLEAN'
            else:
                pg_type = 'TEXT'
            
            columns.append(f'"{col_name}" {pg_type}')
        
        # 创建表的SQL语句
        create_table_sql = f"""
            CREATE TABLE stardict (
                id SERIAL PRIMARY KEY,
                {', '.join(columns)}
            );
        """
        
        # 执行创建表
        cursor.execute(create_table_sql)
        print("表创建成功")
    
    # 准备插入数据
    print("开始插入数据...")
    
    # 获取列名
    columns = [f'"{col}"' for col in df.columns]
    
    # 准备数据值
    values = [tuple(x) for x in df.to_numpy()]
    
    # 构建插入SQL
    insert_sql = f"""
        INSERT INTO stardict ({', '.join(columns)})
        VALUES %s;
    """
    
    # 使用execute_values批量插入数据
    execute_values(cursor, insert_sql, values)
    
    # 提交事务
    conn.commit()
    print(f"成功插入 {len(df)} 条数据")
    
    # 验证数据插入
    cursor.execute("SELECT COUNT(*) FROM stardict;")
    count = cursor.fetchone()[0]
    print(f"表中现有数据条数: {count}")
    
except Exception as e:
    print(f"发生错误: {e}")