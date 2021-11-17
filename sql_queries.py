from config import *
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


def pull_stat(u_id=None):
    cur.execute(f'select * from users where id = ({u_id})')
    result = cur.fetchone()
    return result


def get_users_number():
    cur.execute('select id from users')
    result = cur.fetchall()
    cur.execute('select id from users where is_admin = true')
    result_admin = cur.fetchall()
    return len(result), len(result_admin)


def add_user_to_db(u_id=None):
    cur.execute(f'select id from users where id = ({u_id})')
    result = cur.fetchall()
    if not bool(result):
        cur.execute(f'INSERT INTO users (id) VALUES ({u_id})')
        conn.commit()
    return bool(result)


def change_user_to_admin(u_id=None):
    cur.execute(f'select is_admin from users where id = ({u_id})')
    result = cur.fetchone()
    if result[0] == False:
        cur.execute(f"UPDATE users SET is_admin = true WHERE id = ({u_id})")
        conn.commit()


def create_item(item_name, price, image, description, flavors, times_clicked):
    cur.execute(
        f"INSERT INTO item (item_name, price, image, description, flavors, times_clicked) VALUES ('{item_name}', '{price}', '{image}', '{description}', '{flavors}', '{times_clicked}')")
    conn.commit()


def pull_items():
    cur.execute(f'select item_name from item')
    result = cur.fetchall()
    return result


def pull_item_info(item_name):
    cur.execute(f"select * from item WHERE item_name = ('{item_name}')")
    result = cur.fetchone()
    return result


def del_item(item_name):
    cur.execute(f'''DELETE FROM item WHERE item_name = ('{item_name}')''')
    conn.commit()


def get_clicks():
    cur.execute(f'select times_clicked, item_name from item ORDER BY times_clicked DESC')
    result = cur.fetchall()
    return result


def get_item_by_clicks(clicks):
    cur.execute(f"select item_name from item WHERE times_clicked = ('{clicks}')")
    result = cur.fetchall()
    return result[0][0]


def get_item_clicks(item_name):
    cur.execute(f"select times_clicked from item WHERE item_name = ('{item_name}')")
    result = cur.fetchall()
    return result[0]


def update_clicks(item_name):
    clicks = get_item_clicks(item_name)
    clicks = clicks[0] + 1
    cur.execute(f"UPDATE item SET times_clicked = {clicks} WHERE item_name = ('{item_name}')")
    conn.commit()


def change_users_lang(lang, uid):
    cur.execute(f"UPDATE users SET language = ('{lang}') WHERE id = ('{uid}')")
    conn.commit()


def change_admin_pass(new_pass, u_id):
    cur.execute(f"UPDATE users SET admin_pass = ('{new_pass}')")
    cur.execute(f"UPDATE users SET is_admin = false")
    cur.execute(f"UPDATE users SET is_admin = true WHERE id = ({u_id})")
    conn.commit()
