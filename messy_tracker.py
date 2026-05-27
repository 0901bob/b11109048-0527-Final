import legacy_lib
import os

TEST_FILE = "test_input_data.txt"

def run_demo():
	# 載入現有資料（legacy 使用 lib_data.txt）
	legacy_lib.load_proc()

	if not os.path.exists(TEST_FILE):
		print("找不到測試輸入檔: ", TEST_FILE)
		return

	with open(TEST_FILE, "r", encoding="utf-8") as f:
		lines = [l.strip() for l in f if l.strip()]

	for op in lines:
		print(f"> {op}")
		if op == "exit":
			# 寫回 legacy 檔案
			fobj = open(legacy_lib.F_NAME, "w", encoding="utf-8")
			for b in legacy_lib.d2:
				fobj.write(f"{b['t']}@@{b['i']}##{b['s']}\n")
			fobj.close()
			print("系統關閉")
			break

		elif op.startswith("add "):
			raw = op[4:].split("/")
			if len(raw) == 3:
				if not legacy_lib.c_res(raw[1]):
					legacy_lib.d2.append({"t": raw[0], "i": raw[1], "s": raw[2]})
					print("Success")
				else:
					print("ISBN Exist")
			else:
				print("Format Error")

		elif op == "show":
			for b in legacy_lib.d2:
				print(f"書名: {b['t']}, ISBN: {b['i']}, 狀態: {b['s']}")

		elif op.startswith("borrow "):
			target_isbn = op[7:]
			updated = False
			for b in legacy_lib.d2:
				if b['i'] == target_isbn:
					b['s'] = "borrowed"
					updated = True
			if updated:
				print("Updated")
			else:
				print("ISBN Not Found")
		else:
			print("Unknown Command")

if __name__ == "__main__":
	run_demo()

