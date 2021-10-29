import sqlite3

conn = sqlite3.connect('db.db', check_same_thread=False)  # ~代表路徑
c = conn.cursor()


# 開通會員權限
def add_userInfo(uid, platform, api_key, api_secret, create_at):
    try:
        c.execute(
            "INSERT INTO main.users(uid,  platform, api_key, api_secret, create_at, create_at) VALUES (?,?,?,?,?,?)",
            (uid, platform, api_key, api_secret, create_at, create_at))
        conn.commit()
        return True
    except Exception as e:
        raise ValueError(e)

# 修改會員資料
def edit_userInfo(uid, api_key="", api_secret=""):
    try:
        c.execute('UPDATE "main"."users" SET "api_key" = ?,"api_secret" = ? WHERE "uid" = ?', (api_key, api_secret, uid))
        conn.commit()
        return True
    except Exception as e:
        raise ValueError(e)

# 刪除會員資料
def del_userInfo(uid):
    try:
        c.execute('DELETE FROM "main"."users" WHERE "uid" = ?', (uid,))

        conn.commit()
        return True
    except Exception as e:
        raise ValueError(e)



# 取得帳戶資訊
def get_userInfo(uid):
    c.execute(f'SELECT * FROM users WHERE uid = ?', (uid,))
    rows = c.fetchall()

    if len(rows) > 0:
        rows = rows[0]
        info = {
            'uid': rows[0],
            'platform':rows[1],
            'api_key': rows[2],
            'api_secret': rows[3],
            'create_at': rows[4]
        }
        return info
    else:
        return False
