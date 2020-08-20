from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock
from person import Person

PORT = 5600
HOST = 'localhost'
print(HOST)
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)
persons = []


def broadcast(msg, name):
    for person in persons:
        client = person.client
        client.send(f"{name} : {msg.decode('utf8')}".encode('utf8'))


def client_communication(person):
    client = person.client
    while True:
        try:
            msg = client.recv(512)

            # first msg will be name and setting that name and
            # broadcasting that <name> connected
            if not person.name:
                # ------ for new connection --------
                broadcast(f"joined the chat".encode('utf8'), msg.decode('utf8'))
                print(f"{msg.decode('utf8')} : joined the chat")
                person.set_name(msg.decode("utf8"))
            else:
                if msg.decode("utf8") == "{quit}":
                    print(f"{person.name} : [DISCONNECTED]{msg.decode('utf8')}")
                    client.close()    # close the connection
                    persons.remove(person)   # remove that person from persons
                    # broadcasting everyone else that person left
                    broadcast(f'Exited chat...'.encode("utf8"), person.name)
                    break
                else:
                    # normal broadcasting ------------
                    broadcast(msg, person.name)
                    print(f"{person.name} : {msg.decode('utf8')}")
        except Exception as e:
            print(e)


def wait_for_connection():
    run = True
    while run:
        client, addr = SERVER.accept()
        person = Person(addr, client)
        persons.append(person)    # for broadcasting
        print(f"[IGNORE] {persons}")
        print(f'[CONNECTED] TO {addr}')
        Thread(target=client_communication, args=(person,)).start()


if __name__ == "__main__":
    SERVER.listen()
    print("Waiting for connections .... ")
    ACCEPT_THREAD = Thread(target=wait_for_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
