from socket import *
from threading import Thread

class user_message:
    def __init__(self,name:str,
                 password:str,
                 state:bool=False,
                 socket_recv:socket=None,
                 addr=None):
        self.name=name
        self.password=password
        self.state=state
        self.socket=socket_recv
        self.addr=addr
        self.friends=[name]

ip=''
port=51801
socket_num_max=500
socket_byte_max=1024
listen_socket=socket(AF_INET,SOCK_STREAM)
print("创建用于监听的listen_socket实例")
listen_socket.bind((ip,port))
print("listen_socket绑定本机所有网络接口IP，端口号%d"%port)
listen_socket.listen(socket_num_max)
print("开始监听：最多接受%d个连接请求"% socket_num_max)
users_table={"liyanwei":user_message("liyanwei","li135642")}

def server_thread(data_socket:socket,addr):
    name=None
    while True:
        try:
            rec = data_socket.recv(socket_byte_max)
        except:
            data_socket.close()
            if not name:
                break
            else:
                name=users_table[name]
                name.state=False
                name.socket=None
                name.addr=None
                print(name.name,"已下线")
                break
        info = rec.decode().split("---...***")
        title=info[0].strip()
        if title=="zc":
            username=info[1].strip()
            password=info[2].strip()
            if username in users_table.keys():
                try:
                    data_socket.send("zc---...***0".encode())
                except:
                    data_socket.close()
                    break
            else:
                try:
                    data_socket.send("zc---...***1".encode())
                except:
                    data_socket.close()
                    break
                name=username
                users_table[name]=user_message(name,password,True,data_socket,addr)
                print(name,"注册成功！")
        elif title=="dl":
            username = info[1].strip()
            password = info[2].strip()
            if username not in users_table.keys():
                try:
                    data_socket.send("dl---...***0".encode())
                except:
                    data_socket.close()
                    break
                print(username,":用户名错误：")
            elif password!=users_table[username].password:
                try:
                    data_socket.send("dl---...***1".encode())
                except:
                    data_socket.close()
                    break
                print(username,"密码错误：")
            else:
                try:
                    data_socket.send("dl---...***2".encode())
                except:
                    data_socket.close()
                    break
                name=username
                users_table[name].state=True
                users_table[name].socket =data_socket
                users_table[name].addr =addr
                print(name,"登录成功：")
        elif title=="updata_friends":
            user=users_table[name]
            friends=user.friends
            n=len(friends)
            try:
                data_socket.send(("updata_friends---...***"+str(n)).encode())
                for i in range(n):
                    ns=friends[i]
                    ss=str(ns)+","+str(users_table[ns].state)
                    data_socket.recv(socket_byte_max)
                    data_socket.send(ss.encode())
            except:
                data_socket.close()
                name = users_table[name]
                name.state = False
                name.socket = None
                name.addr = None
                print(name.name, "已下线")
                break
        elif title=="add_friend":
            friend=info[1].strip()
            if friend!=name and friend in users_table.keys() and friend not in users_table[name].friends:
                users_table[name].friends.append(friend)
                try:
                    data_socket.send("add_friend---...***3".encode())
                except:
                    continue
            elif friend==name:
                try:
                    data_socket.send("add_friend---...***0".encode())
                except:
                    continue
            elif friend not in users_table.keys():
                try:
                    data_socket.send("add_friend---...***1".encode())
                except:
                    continue
            else:
                try:
                    data_socket.send("add_friend---...***2".encode())
                except:
                    continue
        elif title=="del_friend":
            friend=info[1].strip()
            if friend==name:
                try:
                    data_socket.send("del_friend---...***0".encode())
                except:
                    continue
            else:
                users_table[name].friends.remove(friend)
                try:
                    data_socket.send("del_friend---...***1".encode())
                except:
                    continue
        elif title:
            message=info[1].strip()
            if title in users_table.keys() and users_table[title].state:
                friend=users_table[title]
                try:
                    friend.socket.send((name+"---...***"+message).encode())
                except:
                    try:
                        data_socket.send("send---...***0".encode())
                    except:
                        continue
                try:
                    data_socket.send("send---...***1".encode())
                except:
                    continue
            else:
                try:
                    data_socket.send('send---...***0'.encode())
                except:
                    continue
        else:
            data_socket.close()
            if not name:
                break
            else:
                name1 = users_table[name]
                name1.state = False
                name1.socket = None
                name1.socket2=None
                name1.addr = None
                print(name1.name, "已下线")
                break

while True:
    data_socket,addr=listen_socket.accept()
    socket_thread=Thread(target=server_thread,args=(data_socket,addr),daemon=True)
    socket_thread.start()
