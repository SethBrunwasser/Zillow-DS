
import sqlite3
import sys

class RealEstateDB:

	def __init__(self):
		self.connection = sqlite3.connect('realestate.db')
		self.cursor = self.connection.cursor()

		self.cursor.execute("DROP TABLE IF EXISTS REAL_ESTATE;")
		self.cursor.execute("DROP TABLE IF EXISTS TREE_PATH;")

		self.cursor.execute("""
			CREATE TABLE REAL_ESTATE (
			ID INTEGER PRIMARY KEY AUTOINCREMENT,
			ZPID INTEGER
			);""")

		self.cursor.execute("""
			CREATE TABLE TREE_PATH (
			ANCESTOR_ID INTEGER NOT NULL REFERENCES REAL_ESTATE(ZPID),
			DESCENDANT_ID INTEGER NOT NULL REFERENCES REAL_ESTATE(ZPID),
			PRIMARY KEY (ANCESTOR_ID, DESCENDANT_ID)
			);""")

		self.connection.commit()


	def insertZPID(self, zpid):
		self.cursor.execute("INSERT INTO REAL_ESTATE (ZPID) VALUES (?)", (zpid,))
	
	def insertTreeLink(self, ancestor, descendant):
		self.cursor.execute("INSERT INTO TREE_PATH (ANCESTOR_ID, DESCENDANT_ID) VALUES (?, ?)", (ancestor, descendant))

	def checkIfExistsZPID(self, zpid):
		self.cursor.execute("SELECT ZPID FROM REAL_ESTATE WHERE ZPID=(?)", (zpid,))
		if not self.cursor.fetchone():
			return False
		else:
			return True

	def checkIfExistsTreeLink(self, ancestor, descendant):
		self.cursor.execute("SELECT ANCESTOR_ID, DESCENDANT_ID FROM TREE_PATH WHERE ANCESTOR_ID=(?) AND DESCENDANT_ID=(?)", (ancestor, descendant))
		if not self.cursor.fetchone():
			return False
		else:
			return True

	def query_all_real_estate(self):
		data = self.cursor.execute("SELECT * FROM REAL_ESTATE;")
		for row in data:
			print(row)
		return self.cursor.fetchall()

	def query_all_tree_path(self):
		data = self.cursor.execute("SELECT * FROM TREE_PATH;")
		for row in data:
			print(row)
		return self.cursor.fetchall()



#	def __del__(self):
#		self.connection.close()
