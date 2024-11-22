from class_bai_2 import Student
# S = Student('001', 'Gà python')
# S2 = Student('002', 'Gà python 2')
sv=[]
print(Student.count)
while True:
    print('''
    Vui lòng chọn chức năng:
          0. Thoát
          1. Xem danh sách sinh vien
          2. Thêm sinh viên
          ....
    ''')
    chon=input('Bạn chọn chức năng nào?')
    if chon.isdigit():
        chon=int(chon)
        if chon==0:
            break
        elif chon==1:
            if len(sv)==0: print('Hiện chưa có sinh viên nào') 
            else:
                for i in sv:
                    i.show()
        elif chon==2:
            id=input('Nhập ID sinh viên: ') 
            Name=input('Nhập Tên sinh viên: ')
            sv.append(Student(id,Name))
        elif chon==3:
            id=input('Nhập ID sinh viên muốn xóa: ') 
            for i in sv:
                if i.id==id:
                    sv.remove(i)
        elif chon==4 :
            id=input('Nhập ID sinh viên muôn sửa: ') 
            for i in sv:
                if i.id==id:
                    sv.set_name(input('Nhập tên muốn thay đổi:'))

    else:
        print('Vui lòng chọn lại')


