
import os
import sys
import string
import sqlite3
from os import listdir
from os.path import isabs
from os.path import join as path_join
from auth import AccessDeniedError, allowed_to_read
from config import BASE_DIR, DATA_DIR


from message import Messager


from time import sleep


DB_FNAME = 'lite.db'

# state in Table Ann
Ann_NULL, Ann_ING, Ann_DONE, Ann_CHECKED = list(range(4))


_CREATE_ANN_SQL = u"""
CREATE TABLE IF NOT EXISTS Ann (
  id INTEGER PRIMARY KEY,
  state INTEGER,
  fid INTEGER,
  fileName TEXT, 
  fileDirAbs TEXT,
  uid INTEGER,
  userName TEXT
);
"""

_INSERT_ANN_SQL = u"""
INSERT INTO Ann (state, fid, fileName, fileDirAbs, uid, userName) VALUES (?, ?, ?, ?, ?, ?);
"""

def assert_allowed_to_read(doc_path):
    if not allowed_to_read(doc_path):
        raise AccessDeniedError  # Permission denied by access control


def real_directory(directory, rel_to=DATA_DIR):
    assert isabs(directory), 'directory "%s" is not absolute' % directory
    return path_join(rel_to, directory[1:])


def _is_hidden(file_name):
    return file_name.startswith('hidden_') or file_name.startswith('.')


def _listdir(directory):
    # return listdir(directory)
    try:
        # 文件目录控制
        assert_allowed_to_read(directory)
        return [f for f in listdir(directory) if not _is_hidden(f)
                and allowed_to_read(path_join(directory, f))]
    except OSError as e:
        print('Error listing '+ directory + ': ' + e, file=sys.stderr)


class DBlite():
    """
    Transaction Control At The SQL Level
The changes to locking and concurrency control in SQLite version 3 also
introduce some subtle changes in the way transactions work at the SQL
language level. By default, SQLite version 3 operates in autocommit mode.
In autocommit mode, all changes to the database are committed as soon as
all operations associated with the current database connection complete.

The SQL command "BEGIN TRANSACTION" (the TRANSACTION keyword is optional)
is used to take SQLite out of autocommit mode. Note that the BEGIN command
does not acquire any locks on the database. After a BEGIN command, a SHARED
lock will be acquired when the first SELECT statement is executed. A RESERVED
lock will be acquired when the first INSERT, UPDATE, or DELETE statement is
executed. No EXCLUSIVE lock is acquired until either the memory cache fills
up and must be spilled to disk or until the transaction commits. In this way,
the system delays blocking read access to the file file until the last possible
moment.

The SQL command "COMMIT" does not actually commit the changes to disk. It just
turns autocommit back on. Then, at the conclusion of the command, the regular
autocommit logic takes over and causes the actual commit to disk to occur. The
SQL command "ROLLBACK" also operates by turning autocommit back on, but it also
sets a flag that tells the autocommit logic to rollback rather than commit.

If the SQL COMMIT command turns autocommit on and the autocommit logic then
tries to commit change but fails because some other process is holding a SHARED
lock, then autocommit is turned back off automatically. This allows the user to
retry the COMMIT at a later time after the SHARED lock has had an opportunity
to clear.

If multiple commands are being executed against the same SQLite database connection
at the same time, the autocommit is deferred until the very last command completes.
For example, if a SELECT statement is being executed, the execution of the command
will pause as each row of the result is returned. During this pause other INSERT,
UPDATE, or DELETE commands can be executed against other tables in the database.
But none of these changes will commit until the original SELECT statement finishes.
    """

    def __init__(self):
        # 连接到SQLite数据库
        # 数据库文件是DB_FNAME，如果文件不存在，会自动在当前目录创建
        flag_exist = os.path.isfile(DB_FNAME)
        self.conn = sqlite3.connect(DB_FNAME)

        if flag_exist:
            return None
        try:
            cursor = self.conn.cursor()
            cursor.execute(_CREATE_ANN_SQL)
            self.conn.commit()
        except sqlite3.Error as e:
            # print("Database error: %s" % e, file=sys.stderr)
            Messager.error("Database error: %s" % e)
            self.conn.rollback()
            self.conn.close()
        except Exception as e:
            # print("Exception in _query: %s" % e, file=sys.stderr)
            Messager.error("Exception in _query: %s" % e)
            self.conn.rollback()
            self.conn.close()
        finally:
            cursor.close()
            en_import_DATA = True
            if en_import_DATA:
                for dir in [x[0].replace(DATA_DIR, '')+'/' for x in os.walk(DATA_DIR)]:
                    if len(dir)>1:
                        self.import_files(dir)
            return None

    def __del__(self):
        self.conn.close()

    def import_files(self, directory):
        real_dir = real_directory(directory)
        assert_allowed_to_read(real_dir)
        # Get the document names
        file_names = [fn[0:-4] for fn in _listdir(real_dir) if fn.endswith('txt')]
        try:
            cursor = self.conn.cursor()
            for filename in file_names:
                state, fid, fileName, fileDirAbs, uid, userName = Ann_NULL, 0, filename, directory, 0, None
                cursor.execute(_INSERT_ANN_SQL, (state, fid, fileName, fileDirAbs, uid, userName))
            self.conn.commit()
        except sqlite3.Error as e:
            # print("Database error: %s" % e, file=sys.stderr)
            Messager.error("Database error: %s" % e)
            self.conn.rollback()
        except Exception as e:
            # print("Exception in _query: %s" % e, file=sys.stderr)
            Messager.error("Exception in _query: %s" % e)
            self.conn.rollback()
        finally:
            cursor.close()


    def set_AnnING_file(self, directory, file, user):
        real_dir = real_directory(directory)
        assert_allowed_to_read(real_dir)
        # check and update
        try:
            cursor = self.conn.cursor()
            cursor.execute("""BEGIN TRANSACTION""")
            cursor.execute("""SELECT userName FROM Ann WHERE fileDirAbs = ? and  fileName = ?;""", (directory, file))
            rows = cursor.fetchall()
            # sleep(10)
            # 分配给单个用户标注
            if len(rows) == 1 and None in rows[0]:
                cursor.execute("""UPDATE Ann SET userName = ?, state = ? WHERE fileDirAbs = ? and  fileName = ?;""", (user, Ann_ING, directory, file))
        except sqlite3.Error as e:
            # print("Database error: %s" % e, file=sys.stderr)
            Messager.error("Database error: %s" % e)
            self.conn.rollback()
        except Exception as e:
            # print("Exception in _query: %s" % e, file=sys.stderr)
            Messager.error("Exception in _query: %s" % e)
            self.conn.rollback()
        finally:
            cursor.execute("COMMIT")
            cursor.close()
            self.show_db()

    def set_Ann_user(self, directory, file, user):
        real_dir = real_directory(directory)
        assert_allowed_to_read(real_dir)
        # check and update
        try:
            cursor = self.conn.cursor()
            cursor.execute("""BEGIN TRANSACTION""")
            cursor.execute("""SELECT userName FROM Ann WHERE fileDirAbs = ? and  fileName = ?;""", (directory, file))
            rows = cursor.fetchall()
            if len(rows) == 0:
                cursor.execute("""UPDATE Ann SET userName = ? WHERE fileDirAbs = ? and  fileName = ?;""", (user, directory, file))
        except sqlite3.Error as e:
            # print("Database error: %s" % e, file=sys.stderr)
            Messager.error("Database error: %s" % e)
            self.conn.rollback()
        except Exception as e:
            # print("Exception in _query: %s" % e, file=sys.stderr)
            Messager.error("Exception in _query: %s" % e)
            self.conn.rollback()
        finally:
            cursor.execute("COMMIT")
            cursor.close()


    def set_Ann_state(self, directory, file, state):
        real_dir = real_directory(directory)
        assert_allowed_to_read(real_dir)
        # check and update
        try:
            cursor = self.conn.cursor()
            cursor.execute("""BEGIN TRANSACTION""")
            cursor.execute("""SELECT userName FROM Ann WHERE fileDirAbs = ? and  fileName = ?;""", (directory, file))
            rows = cursor.fetchall()
            if len(rows) == 0:
                cursor.execute("""UPDATE Ann SET state = ? WHERE fileDirAbs = ? and  fileName = ?;""", (state, directory, file))
        except sqlite3.Error as e:
            # print("Database error: %s" % e, file=sys.stderr)
            Messager.error("Database error: %s" % e)
            self.conn.rollback()
        except Exception as e:
            # print("Exception in _query: %s" % e, file=sys.stderr)
            Messager.error("Exception in _query: %s" % e)
            self.conn.rollback()
        finally:
            cursor.execute("COMMIT")
            cursor.close()


    def get_AnnNull_files(self, directory):
        real_dir = real_directory(directory)
        assert_allowed_to_read(real_dir)
        try:
            cursor = self.conn.cursor()
            cursor.execute("""SELECT fileName FROM Ann WHERE state=? and fileDirAbs=?;""", (Ann_NULL, directory))

            rows = cursor.fetchall()
            return [row[0] for row in rows]
        except sqlite3.Error as e:
            # print("Database error: %s" % e, file=sys.stderr)
            Messager.error("Database error: %s" % e)
        except Exception as e:
            # print("Exception in _query: %s" % e, file=sys.stderr)
            Messager.error("Exception in _query: %s" % e)
        finally:
            cursor.close()


    def get_AnnING_files(self, directory, user):
        real_dir = real_directory(directory)
        assert_allowed_to_read(real_dir)
        try:
            cursor = self.conn.cursor()
            cursor.execute("""SELECT fileName FROM Ann WHERE state=? and fileDirAbs=? and userName=?;""", (Ann_ING, directory, user))
            rows = cursor.fetchall()
            return [row[0] for row in rows]
        except sqlite3.Error as e:
            # print("Database error: %s" % e, file=sys.stderr)
            Messager.error("Database error: %s" % e)
        except Exception as e:
            # print("Exception in _query: %s" % e, file=sys.stderr)
            Messager.error("Exception in _query: %s" % e)
        finally:
            cursor.close()

    def get_Ann_DONE_files(self, directory, user):
        real_dir = real_directory(directory)
        assert_allowed_to_read(real_dir)
        try:
            cursor = self.conn.cursor()
            cursor.execute("""SELECT fileName FROM Ann WHERE state=? and fileDirAbs=? and userName=?;""",
                           (Ann_DONE, directory, user))
            rows = cursor.fetchall()
            return [row[0] for row in rows]
        except sqlite3.Error as e:
            # print("Database error: %s" % e, file=sys.stderr)
            Messager.error("Database error: %s" % e)
        except Exception as e:
            # print("Exception in _query: %s" % e, file=sys.stderr)
            Messager.error("Exception in _query: %s" % e)
        finally:
            cursor.close()

    def comlete_Ann_files(self, directory, file, user):
        real_dir = real_directory(directory)
        assert_allowed_to_read(real_dir)
        try:
            cursor = self.conn.cursor()
            cursor.execute("""UPDATE Ann SET state = ? WHERE fileName = ? and userName=?;""",
                           (Ann_DONE, file, user))
            self.conn.commit();
            rows = cursor.fetchall()
            return [row[0] for row in rows]
        except sqlite3.Error as e:
            # print("Database error: %s" % e, file=sys.stderr)
            Messager.error("Database error: %s" % e)
        except Exception as e:
            # print("Exception in _query: %s" % e, file=sys.stderr)
            Messager.error("Exception in _query: %s" % e)
        finally:
            cursor.close()

    def show_db(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""SELECT * FROM Ann;""")
            rows = cursor.fetchall()
            print("data in DB:", file=sys.stderr)
            for r in rows:
                print(r, file=sys.stderr)
        except sqlite3.Error as e:
            # print("Database error: %s" % e, file=sys.stderr)
            Messager.error("Database error: %s" % e)
        except Exception as e:
            # print("Exception in _query: %s" % e, file=sys.stderr)
            Messager.error("Exception in _query: %s" % e)
        finally:
            cursor.close()

