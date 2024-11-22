# Class trong python
class Student1:
    # Thuộc tính
    id=''
    name=''
    # Phương thức
    def __init__(self,id,name):# Hàm khởi tạo đối tượng
        print('hàm add student')
        self.id=id
        self.name=name
    # def add(self,id,name):
    #     print('hàm add student')
    #     self.id=id
    #     self.nam=name
    def delete(self,id):
        print('Xóa student')       
    def edit(self,id):
        print('Sửa student')        
    def show(self):
        print(f'ID: {self.id}')
        print(f'Name: {self.name}')
      
# Sử dụng clsas
S=Student('001','Gà python')
# S.add('001','Gà python')
S.show()   
        