from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter.messagebox as mb
import pymysql

class document():
    def __init__(self, root):
        self.root = root
        self.root.title("Document Management System")
        self.root.geometry("1020x540")
        self.root.resizable(False, False)


        self.var_name = StringVar()
        self.var_nim = StringVar()
        self.var_prodi = StringVar()

        self.var_search = StringVar()
        
        #Tampilan Utama
        searchbtn = Button(text="Cari", command=self.search_data)
        searchbtn.place(x=849,y=15)
        showallhbtn = Button(text="Semua", command=self.show_data)
        showallhbtn.place(x=890,y=15)
        
        search = Entry(textvariable=self.var_search, bd=3, relief=GROOVE, width=30)
        search.place(x=650,y=14, height=27)
        
        downloadbtn = Button(text="Download", command=self.download)
        downloadbtn.place(x=550, y=15)
        deletebtn = Button(text="Hapus", command=self.delete_data)
        deletebtn.place(x=490,y=15)
        #===================================

        #set tombol Keluar
        #self.imgKeluar = PhotoImage(file='logout.png')
        #self.btnKeluar = Button(image=self.imgKeluar, compound='top', command=self.close)
        #self.btnKeluar.place(x=970, y=12.5, height=30)
        #===================================

        #Tabel 1 
        table1 = Frame(self.root, bd=4, relief=RIDGE, bg="green")
        table1.place(y=50, width=290, height=450)

        name_document= Label(table1, text="DOKUMEN", bg="green", font=("cambria", 20, "bold"))
        name_document.grid(row=0, columnspan=2, pady=5, padx=75)

        #Label
        label_name = Label(table1, text="Nama ", bg="green", font=("cambria", 12))
        label_name.grid(row=1,column=0, pady=10, padx=10, sticky="w")
        label_nim = Label(table1, text="NIM ", bg="green", font=("cambria", 12))
        label_nim.grid(row=2,column=0, pady=10, padx=10, sticky="w")
        label_prodi = Label(table1, text="Prodi", bg="green", font=("cambria", 12))
        label_prodi.grid(row=3,column=0, pady=10, padx=10, sticky="w")

        entry_name = Entry(table1,textvariable=self.var_name, bd=3, relief=GROOVE, width=30)
        entry_name.grid(row=1, column=1, pady=10, padx=10, sticky="w")
        entry_nim = Entry(table1,textvariable=self.var_nim, bd=3, relief=GROOVE, width=30)
        entry_nim.grid(row=2, column=1, pady=10, padx=10, sticky="w")
        entry_prodi = Entry(table1,textvariable=self.var_prodi, bd=3, relief=GROOVE, width=30)
        entry_prodi.grid(row=3, column=1, pady=10, padx=10, sticky="w") 
        #========================================

        #Tabel 2
        table2 = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        table2.place(y=50, x=300, width=719, height=450)
        
        #scroll
        scroll_x= Scrollbar(table2, orient=HORIZONTAL)
        scroll_y= Scrollbar(table2, orient=VERTICAL)  
        self.document_table = ttk.Treeview(table2, column=("Nama", "NIM", "Prodi", "File"), xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)    
        scroll_y.config(command=self.document_table.yview)
        scroll_x.config(command=self.document_table.xview)
        #=================================

        #Tabel 3   
        table3 = Frame(self.root, bd=4, relief=RIDGE, bg="green")
        table3.place(y=410, x=10, width=268, height=55)

        #add, clear, edit, save
        addbtn = ttk.Button(table3, text="Tambah", command=self.add_document).grid(row=0,column=0, padx=5, pady=10)
        editbtn = ttk.Button(table3, text="Edit", command=self.edit_data).grid(row=0,column=1, padx=5, pady=10) 
        clearbtn = ttk.Button(table3, text="Bersihkan", command=self.clear).grid(row=0,column=3, padx=5, pady=10)

        #Add File
        self.addfilebtn = Button(table1, text="Add File", command=self.openfile)
        self.addfilebtn.place(x=110,y=260)
        #====================================

        #Document Table
        self.document_table.heading("Nama", text="Nama")
        self.document_table.heading("NIM", text="NIM")
        self.document_table.heading("Prodi", text="Prodi")
        self.document_table.heading("File", text="File")
        self.document_table["show"]="headings"
        self.document_table.column("Nama", width=100)
        self.document_table.column("NIM", width=100)
        self.document_table.column("Prodi", width=100)
        self.document_table.column("File", width=100)
        self.document_table.pack(fill=BOTH, expand=1)
        self.document_table.bind("<ButtonRelease-1>", self.get_cursor)
        self.show_data()


    #Program
    def openfile(self, event=None):
        self.filepath = filedialog.askopenfilename(initialdir="D:/", filetypes=(("all files", "*.*"),("png files", "*.png"),
                                                                            ("jpg files", "*.jpg"), ("pdf files", "*.pdf"),
                                                                            ("docx files","*docx")))
        self.label = Label(text = "")
        self.label.grid(padx =10, pady=350)
        self.label.configure(text = self.filepath, bg="yellow")
        print('Selected:',self.filepath)
    

    def convertToBinaryData(self, filename):
        # Convert digital data to binary format
        with open(filename, 'rb') as file:
            binaryData = file.read()
        return binaryData


    def insertBLOB(self, nama, nim, prodi, digitalFile):
        print("Inserting BLOB into document table")
        con=pymysql.connect(host="localhost", user="root", password="", database="document")
        cur=con.cursor()
        sql_insert_blob_query = """ INSERT INTO document
        (nama, nim, prodi, file) VALUES (%s,%s,%s,%s)"""
        binaryFile = self.convertToBinaryData(digitalFile)

        # Convert data into tuple format
        insert_blob_tuple = (nama, nim, prodi, binaryFile)
        result = cur.execute(sql_insert_blob_query, insert_blob_tuple)
        con.commit()
        print("File inserted successfully as a BLOB into document table", result)
        cur.close()
        con.close()
        print("MySQL connection is closed")


    def write_file(self, data, filename):
        # Convert binary data to proper format and write it on Hard Disk
        with open(filename, 'wb') as file:
            file.write(data)


    def readBLOB(self, nim, digitalFile):
        print("Reading BLOB data from document table")
        con=pymysql.connect(host="localhost", user="root", password="", database="document")
        cur=con.cursor()
        sql_fetch_blob_query = """SELECT * from document where nim = %s"""
        cur.execute(sql_fetch_blob_query, (nim,))
        record = cur.fetchall()
        for row in record:
            print("nama = ", row[0], )
            print("nim = ", row[1], )
            print("prodi = ", row[2])
            file = row[3]
            print("Storing file mahasiswa on disk \n")
            self.write_file(file, digitalFile)
        cur.close()
        con.close()
        print("MySQL connection is closed")


    def add_document(self):
        self.insertBLOB (self.var_name.get(),self.var_nim.get(),self.var_prodi.get(),self.filepath)
        
        self.show_data()
        self.clear()

    def download(self):
        self.filesave = filedialog.asksaveasfilename(initialdir="D:/", filetypes=(("all files", "*.*"),("png files", "*.png"),
                                                                            ("jpg files", "*.jpg"), ("pdf files", "*.pdf"),
                                                                            ("docx files","*docx")))
        myfile=open(self.filesave, "w+")
        self.readBLOB (self.var_nim.get(), self.filesave)

    def show_data(self):
        con=pymysql.connect(host="localhost", user="root", password="", database="document")
        cur=con.cursor()
        cur.execute("select * from document")
        rows=cur.fetchall()
        if len(rows)!=0:
            self.document_table.delete(*self.document_table.get_children())
            for row in rows:
                self.document_table.insert("", END, values=row)
            con.commit()
        con.close()
    

    def search_data(self):
        con=pymysql.connect(host="localhost", user="root", password="", database="document")
        cur=con.cursor()
        cur.execute("select * from document where nama LIKE '%"+str(self.var_search.get())+"%'" 
                                                    "or nim LIKE '%"+str(self.var_search.get())+"%'"
                                                    "or prodi LIKE '%"+str(self.var_search.get())+"%'")
        rows=cur.fetchall()
        if len(rows)!=0:
            self.document_table.delete(*self.document_table.get_children())
            for row in rows:
                 self.document_table.insert("", END, values=row)
            con.commit()
        con.close()


    def clear(self):
        self.var_name.set(""),
        self.var_nim.set(""),
        self.var_prodi.set(""),

    def get_cursor(self, ev):
        cursor_row=self.document_table.focus()
        content=self.document_table.item(cursor_row)
        row=content["values"]
        self.var_name.set(row[0])
        self.var_nim.set(row[1])
        self.var_prodi.set(row[2])


    def edit_data(self):
        con=pymysql.connect(host="localhost", user="root", password="", database="document")
        cur=con.cursor()
        cur.execute("update document set nama=%s, prodi=%s, file=%s where nim=%s",(self.var_name.get(),
                                                                                  self.var_prodi.get(),
                                                                                  self.openfile,
                                                                                  self.var_nim.get()
                                                                                  ))
        con.commit()
        self.show_data()
        self.clear()
        con.close()


    def delete_data(self):
        con=pymysql.connect(host="localhost", user="root", password="", database="document")
        cur=con.cursor()
        cur.execute("delete from document where nim=%s", self.var_nim.get())
        con.commit()
        con.close()
        self.show_data()
        self.clear()


     #Menu Keluar
    def close(self, event=None):
        if mb.askyesno('Konfirmasi', 'Keluar dari program?', parent=self.root):
            self.root.destroy()
    #====================================    

#Output
if __name__ == '__main__':
    root = Tk()
    root.configure(background="#3cc7f7")
    apk = document(root)
    root.mainloop()
