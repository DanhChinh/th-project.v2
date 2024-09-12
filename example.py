import mysql.connector
import random

class Bot:
    def __init__(self, name, table_name):
        self.alpha = 0.15
        self.gamma = 0.95
        self.epsilon = 0.15
        self.name = name
        self.table_name = table_name

        # Kết nối đến cơ sở dữ liệu
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="thuhuyen123",
            database="qlearning_database"
        )
        self.cursor = self.conn.cursor()

        # Tải toàn bộ q_table từ cơ sở dữ liệu
        self.q_table = self.load_q_table()

    def load_q_table(self):
        """Tải toàn bộ dữ liệu từ bảng q_table và lưu vào từ điển."""
        self.cursor.execute(f"SELECT * FROM `{self.table_name}`")
        rows = self.cursor.fetchall()

        q_table = {}
        for row in rows:
            state = row[1]  # Giả sử state là cột thứ 2
            action = row[2] # Giả sử action là cột thứ 3
            q_value = row[3] # Giả sử q_value là cột thứ 4

            if state not in q_table:
                q_table[state] = {}
            q_table[state][action] = q_value

        return q_table

    def choose_action(self, state, gameState):
        """Chọn hành động dựa trên chính sách epsilon-greedy."""
        # Kiểm tra xem trạng thái có tồn tại trong q_table không
        if state not in self.q_table:
            # Nếu trạng thái không tồn tại, thêm trạng thái vào q_table
            actions = qtable_add_state(gameState)  # Bạn cần định nghĩa qtable_add_state
            self.q_table[state] = actions

            # Chèn trạng thái mới vào cơ sở dữ liệu
            for action, q_value in actions.items():
                self.insert_q_value(state, action, q_value)

        # Chọn hành động theo chính sách epsilon-greedy
        if random.random() < self.epsilon:
            # Chọn hành động ngẫu nhiên
            return random.choice(list(self.q_table[state].keys()))
        else:
            # Chọn hành động có giá trị Q cao nhất
            return max(self.q_table[state], key=self.q_table[state].get)

    def insert_q_value(self, state, action, q_value):
        """Chèn hoặc cập nhật giá trị Q vào cơ sở dữ liệu."""
        # Thực hiện chèn hoặc cập nhật giá trị Q trong cơ sở dữ liệu
        self.cursor.execute(
            f"""
            INSERT INTO `{self.table_name}` (state, action, q_value)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE q_value = VALUES(q_value)
            """,
            (state, action, q_value)
        )
        self.conn.commit()

    def close(self):
        """Đóng kết nối đến cơ sở dữ liệu."""
        self.cursor.close()
        self.conn.close()
