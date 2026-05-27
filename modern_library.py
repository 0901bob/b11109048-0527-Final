# filepath: c:\Users\pclab\Desktop\NTUST-0527-Final-master\modern_library.py
import json
import os
from typing import Dict, List, Optional

DATA_FILE = 'books.json'

class LibraryManager:
    def __init__(self, data_file: str = DATA_FILE) -> None:
        self.data_file = data_file
        self.books: List[Dict[str, str]] = []
        self.modified = False
        self.load_books()

    def load_books(self) -> None:
        if not os.path.exists(self.data_file):
            self.books = []
            return

        try:
            with open(self.data_file, 'r', encoding='utf-8-sig') as file:
                data = json.load(file)

            if not isinstance(data, list):
                raise ValueError('Invalid JSON structure: expected a list')

            self.books = [self._normalize_record(item) for item in data if isinstance(item, dict)]
        except (json.JSONDecodeError, ValueError) as exc:
            print(f'Warning: 無法解析 {self.data_file}，將以空資料庫啟動。({exc})')
            self.books = []
        except OSError as exc:
            print(f'Warning: 讀取 {self.data_file} 時發生錯誤，將以空資料庫啟動。({exc})')
            self.books = []

    def save_books(self) -> None:
        try:
            with open(self.data_file, 'w', encoding='utf-8') as file:
                json.dump(self.books, file, ensure_ascii=False, indent=4)
            self.modified = False
        except OSError as exc:
            print(f'Error: 無法寫入 {self.data_file}。({exc})')

    def _normalize_record(self, record: Dict[str, str]) -> Dict[str, str]:
        return {
            'title': str(record.get('title', '')).strip(),
            'isbn': str(record.get('isbn', '')).strip(),
            'status': str(record.get('status', '')).strip() or 'available',
        }

    def find_book_by_isbn(self, isbn: str) -> Optional[Dict[str, str]]:
        normalized_isbn = isbn.strip()
        return next((book for book in self.books if book.get('isbn') == normalized_isbn), None)

    def add_book(self, title: str, isbn: str, status: str) -> bool:
        if self.find_book_by_isbn(isbn):
            return False

        self.books.append({
            'title': title.strip(),
            'isbn': isbn.strip(),
            'status': status.strip() or 'available',
        })
        self.modified = True
        return True

    def borrow_book(self, isbn: str) -> bool:
        book = self.find_book_by_isbn(isbn)
        if not book:
            return False
        book['status'] = 'borrowed'
        self.modified = True
        return True

    def show_books(self) -> None:
        if not self.books:
            print('目前沒有任何書籍資料。')
            return

        for idx, book in enumerate(self.books, start=1):
            print(f"書名: {book['title']}, ISBN: {book['isbn']}, 狀態: {book['status']}")

    def handle_command(self, command: str) -> bool:
        command = command.strip()
        if command == 'show':
            self.show_books()
            return True
        if command == 'exit':
            return False
        if command.startswith('add '):
            payload = command[4:].strip()
            parts = payload.split('/')
            if len(parts) != 3:
                print('Format Error')
                return True
            title, isbn, status = [part.strip() for part in parts]
            if not title or not isbn or not status:
                print('Format Error')
                return True
            if self.add_book(title, isbn, status):
                print('Success')
            else:
                print('ISBN Exist')
            return True
        if command.startswith('borrow '):
            isbn = command[7:].strip()
            if not isbn:
                print('Format Error')
                return True
            if self.borrow_book(isbn):
                print('Updated')
            else:
                print('ISBN Not Found')
            return True

        print('Unknown Command')
        return True

    def close(self) -> None:
        if self.modified:
            self.save_books()


def main() -> None:
    manager = LibraryManager()
    print('=== 圖書管理系統 v1.0 (Modern) ===')

    while True:
        try:
            op = input('> ').strip()
        except EOFError:
            break

        if not manager.handle_command(op):
            break

    manager.close()
    print('系統關閉')


if __name__ == '__main__':
    main()
