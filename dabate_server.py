import socket, threading

# 딕셔너리1: ip, socket
socs = {}
# 딕셔너리2: ip, time
times = {}
# 대기 큐: ip
participants = []
# 발언
flag = True

HOST = '0.0.0.0'
PORT = 9999 #msg, command
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()

#1. 발언 신청 함수
def getrequest(ip,option):
    global socs
    global times
    global participants
    print("<발언 신청>")
    # 신청 거절: 대기 큐의 마지막 ip가 해당 클라이언트 ip라면
    if len(participants)>0 and participants[-1] == ip:
        print("신청 거절")
        s = "/refuse"
        socs.get(ip).sendall(s.encode())
        print("refuse 메세지 전송 완료")
    # 신청 수락
    else :
        print("신청 수락")
        # 대기 큐에 ip append
        participants.append(ip)
        # 딕셔너리2의 ip(키)에 time(밸류) 저장
        k = option.split('/')
        times[ip]=k[2]
        s = "/accept"
        for addr in participants:
            s+="/"+str(addr)
        socs.get(ip).sendall(s.encode())
        print("accept 메세지 전송 완료")

#2. 발언 신청 쥐소 함수
def cancelrequest(ip):
    print("<발언 신청 취소>")
    for i in participants :
        if i == ip :
            print("발언 취소 완료")
            s = "0"
            socs.get(ip).sendall(s.encode())
            participants.remove(i)
        else:
            s = "-1"
            socs.get(ip).sendall(s.encode())

#3. 발언자 텍스트 수신 함수
def setdata(ip,option):
    global socs
    global flag
    if participants[0] == ip:
        print("발언권자 메세지")
        contents = option.split('/')[2]
        print(contents)
        for addr in participants: #모든 클라이언트에게 msg 전송
            socs[addr].sendall(option.encode())
    else:
        print("발언권 없는 사람의 메세지")
        s = "-1"
        socs.get(ip).sendall(s.encode())

def recvCommand(ip):
    while 1:
        #print(socs.get(ip))
        data = socs.get(ip).recv(1024)
        #print(ip)
        option = data.decode()
        if option.startswith("/request"):
            print("발언 신청 함수")
            getrequest(ip,option)
        elif option.startswith("/stop"):
            print("발언 중지 함수")
            #현재 speaker면 발언 송출 중지
            if participants[0] == ip:
                print("발언권자 발언 취소")
                #flag = False
                participants.pop(0)
                print("발언 중단 완료. 다음 대기자에 발언권 부여")
                s = "0"
                socs.get(ip).sendall(s.encode())
            else:
                print("발언권자가 아니면 발언 취소 불가")
                s = "-1"
                socs.get(ip).sendall(s.encode())
        elif option.startswith("/cancel"):
            print("발언 신청 취소 함수")
            cancelrequest(ip)
        elif option.startswith("/msg"):
            print("발언권자 msg 뿌리기 함수")
            setdata(ip, option)


print("server start")
while True:
    client_socket, addr = server_socket.accept()
    #딕셔너리1(ip, socket)에 추가
    socs[addr]=client_socket
    #딕셔너리2(ip, time)에 추가
    times[addr]=''
    print('Connected by', addr)
    t = threading.Thread(target=recvCommand, args=(addr,))  # 쓰레드 생성.
    t.start()  # 쓰레드 실행 runnable로 만들기

#server_socket.close()

