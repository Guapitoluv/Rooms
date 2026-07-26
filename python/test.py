from pathlib import Path
import sqlite3

conn = sqlite3.connect(Path(__file__).parent / "data/rooms.db")