# Class trong python
class Student:
    count = 0  # Đảm bảo thụt lề đúng

    # Phương thức
    def __init__(self, id, name):  # Hàm khởi tạo đối tượng
        print('Hàm khởi tạo đối tượng')
        self.id = id
        self.name = name
        Student.count += 1

    def set_id(self, id):
        self.id = id

    def get_id(self):
        return self.id

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def edit(self, id):
        print('Sửa student')

    def show(self):
        print(f'ID: {self.get_id()}')
        print(f'Name: {self.name}')

# Sử dụng class
# S = Student('001', 'Gà python')
# S2 = Student('002', 'Gà python 2')
# print(Student.count)
