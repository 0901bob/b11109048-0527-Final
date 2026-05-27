import json
import os

TEST_FILE = "test_input_data.txt"


class Library:
	def __init__(self, filename="books.json"):
		self.filename = filename
		self.books = []
		self.load()

	def load(self):
		if os.path.exists(self.filename):
			try:
				with open(self.filename, "r", encoding="utf-8") as f:
					self.books = json.load(f)
			except Exception:
				self.books = []
		else:
			self.books = []

	def save(self):
		with open(self.filename, "w", encoding="utf-8") as f:
			json.dump(self.books, f, ensure_ascii=False, indent=2)

	def exists(self, isbn):
		return any(b.get("isbn") == isbn for b in self.books)

	def add_book(self, title, isbn, status):
		if self.exists(isbn):
			return False
		self.books.append({"title": title, "isbn": isbn, "status": status})
		return True

	def borrow(self, isbn):
		for b in self.books:
			if b.get("isbn") == isbn:
				b["status"] = "borrowed"
				return True
		return False

	def show(self):
		for b in self.books:
			print(f"書名: {b.get('title')}, ISBN: {b.get('isbn')}, 狀態: {b.get('status')}")


def run_demo():
	lib = Library()

	if not os.path.exists(TEST_FILE):
		print("找不到測試輸入檔: ", TEST_FILE)
		return

	with open(TEST_FILE, "r", encoding="utf-8") as f:
		lines = [l.strip() for l in f if l.strip()]

	for op in lines:
		print(f"> {op}")
		if op == "exit":
			lib.save()
			print("系統關閉 (refined)")
			break

		elif op.startswith("add "):
			raw = op[4:].split("/")
			if len(raw) == 3:
				ok = lib.add_book(raw[0], raw[1], raw[2])
				print("Success" if ok else "ISBN Exist")
			else:
				print("Format Error")

		elif op == "show":
			lib.show()

		elif op.startswith("borrow "):
			target_isbn = op[7:]
			ok = lib.borrow(target_isbn)
			print("Updated" if ok else "ISBN Not Found")
		else:
			print("Unknown Command")


if __name__ == "__main__":
	run_demo()

