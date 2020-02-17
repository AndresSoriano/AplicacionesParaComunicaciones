#!/usr/bin/env python3
import socket
import random
import os

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
buffer_size = 2048
##Metodos##
def crea_tablero(fil, col, val):
    '''Crea matriz con filas y columnas y valor que le pasemos'''
    tablero = []
    for i in range(fil):
        tablero.append([])
        for j in range(col):
            tablero[i].append(val)
    return tablero


def muestra_tablero(tablero):
    '''Muestra en filas y columnas la matriz que la pasemos'''
    print("")
    i = 1
    for fila in tablero:
        print(i, end=" ")
        for elem in fila:
            print(elem, end=" ")
        print("*")
        i = i + 1

    if i < 11:
        print("  1 2 3 4 5 6 7 8 9")
    else:
        print("   1 2 3 4 5 6 7 8 910111213141516")


def coloca_minas(tablero, minas, fil, col, y, x):
    '''Coloca en el tablero que le pasemos el numero de minas que le pasemos'''
    minas_ocultas = []
    numero = 0
    '''while numero < minas:
        y = random.randint(0, fil - 1)
        x = random.randint(0, col - 1)'''
    if tablero[y][x] != 9:
        tablero[y][x] = 9
        TCPClientSocket.sendall(b"r")
        minas_ocultas.append((y, x))
    return tablero, minas_ocultas


def coloca_pistas(tablero, fil, col):
    for y in range(fil):
        for x in range(col):
            if tablero[y][x] == 9:
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        if 0 <= y + i <= fil - 1 and 0 <= x + j <= col - 1:
                            if tablero[y + i][x + j] != 9:
                                tablero[y + i][x + j] += 1
    return tablero


def rellenado(oculto, visible, y, x, fil, col, val):
    '''Recorre todas las casilla vecinas, y comprueba si son ceros,
    si lo son los descubre y las recorre las vecinas en busca de pistas, que tambien descubre'''
    ceros = [(y, x)]
    while len(ceros) > 0:
        y, x = ceros.pop()
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if 0 <= y + i <= fil - 1 and 0 <= x + j <= col - 1:
                    if visible[y + i][x + j] == val and oculto[y + i][x + j] == 0:
                        visible[y + i][x + j] = 0
                        if (y + i, x + j) not in ceros:
                            ceros.append((y + i, x + j))
                    else:
                        visible[y + i][x + j] = oculto[y + i][x + j]
    return visible


def tablero_completo(tablero, fil, col, val):
    '''Comprueba si el tablero no tiene ninguna casilla con el valor visible inicial'''
    for y in range(fil):
        for x in range(col):
            if tablero[y][x] == val:
                return False
    return True

def presentacion():
    '''Pantalla Presentacion'''
    os.system("cls")
    print("********************")
    print("*    BUSCAMINAS    *")
    print("*     SORIANO      *")
    print("*                  *")
    print("*    1 = FACIL     *")
    print("*   2 = AVANZADO   *")
    print("********************")
    print()
    #input(" 'Enter' para empezar ...")
    nivel = int(input("Introduce el nivel ... "))
    print()
    return nivel

'''def menu(visible):
    #Devuelve el movimiento u opcion elegida por el usuario
    print()
    #opcion = input("¿w/s/a/d -m - b/v? ")
    y = int(input("Fila: "))
    x = int(input("Columna: "))
    real = visible[y][x]
    opcion = "m"
    return visible'''

def reemplaza_ceros(tablero, col, fil):
    for i in range(fil):
        for j in range(col):
            if tablero[i][j] == 0:
                tablero[i][j] = " "
    return tablero
##Metodos##

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, PORT))
    print("Enviando mensaje...")
    lev = presentacion()
    lev = str(lev)
    bytesToSend = str.encode(lev)
    TCPClientSocket.sendall(bytesToSend)
    lev = int(lev)

    if lev == 1:
        columnas = 9
        filas = 9
        minas = 10
    if lev == 2:
        columnas = 16
        filas = 16
        minas = 40

    visible = crea_tablero(filas, columnas, "-")

    oculto = crea_tablero(filas, columnas, 0)
    num = 0
    while num < minas:
        y = TCPClientSocket.recv(buffer_size)
        y = int(y)

        x = TCPClientSocket.recv(buffer_size)
        x = int(x)
        oculto, minas_ocultas = coloca_minas(oculto, minas, filas, columnas, y, x)
        num += 1


    oculto = coloca_pistas(oculto, filas, columnas)


    os.system("cls")

    muestra_tablero(visible)

    # bucle principal#

    minas_marcadas = []
    jugando = True
    while jugando:
        # mov = menu()
        # visible = menu(visible)
        y = int(input("Fila: "))
        x = int(input("Columna: "))
        y -= 1
        x -= 1
        real = visible[y][x]
        y = str(y)
        bytesToSend = str.encode(y)
        TCPClientSocket.sendall(bytesToSend)
        y = int(y)
        x = str(x)
        bytesToSend = str.encode(x)
        TCPClientSocket.sendall(bytesToSend)
        x = int(x)

        mov = "m"
        vali = TCPClientSocket.recv(buffer_size)
        vali = str(vali)
        #print(vali)
        '''if mov == "w":
            if y == 0:
                y = 0
            else:
                visible[y][x] = real
                y -= 1
                real = visible[y][x]
                visible[y][x] = "x"

        elif mov == "s":
            if y == filas - 1:
                y = filas - 1
            else:
                visible[y][x] = real
                y += 1
                real = visible[y][x]
                visible[y][x] = "x"

        elif mov == "a":
            if x == 0:
                x = 0
            else:
                visible[y][x] = real
                x -= 1
                real = visible[y][x]
                visible[y][x] = "x"

        elif mov == "d":
            if x == columnas - 1:
                x = columnas - 1
            else:
                visible[y][x] = real
                x += 1
                real = visible[y][x]
                visible[y][x] = "x"

        elif mov == "b":
            if real == "-":
                visible[y][x] = "#"
                real = visible[y][x]
                if (y, x) not in minas_marcadas:
                    minas_marcadas.append((y, x))

        elif mov == "v":
            if real == "#":
                visible[y][x] = "-"
                real = visible[y][x]
                if (y, x) in minas_marcadas:
                    minas_marcadas.remove((y, x))'''

        if mov == "m":
            if vali == "b'd'":
                oculto[y][x] == 9
                visible[y][x] = "@"
                jugando = False

            elif vali == "b'l'":
                oculto[y][x] != 0
                visible[y][x] = oculto[y][x]
                real = visible[y][x]
                print("dentro")

            elif vali == "b's'":
                oculto[y][x] == 0
                visible[y][x] = 0
                visible = rellenado(oculto, visible, y, x, filas, columnas, "-")
                visible = reemplaza_ceros(visible, filas, columnas)
                real = visible[y][x]

        x = y = 0

        #os.system("cls")

        muestra_tablero(visible)

        ganas = False

        if tablero_completo(visible, filas, columnas, "-") and \
        sorted(minas_ocultas) == sorted(minas_marcadas) and \
        real != "-":
            ganas = True
            jugando = False

    if not ganas:
        print("******Has Perdido******")

    else:
        print("******Has Ganado******")



    print("Esperando una respuesta...")
    data = TCPClientSocket.recv(buffer_size)
    print("Recibido,", repr(data), " de", TCPClientSocket.getpeername())