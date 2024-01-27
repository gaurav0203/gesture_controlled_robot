# main.py -- put your code here!
def web_page():
    if left_forward.value() == 1:
        left_motor_state="Forwarding"
    elif left_reverse.value() == 1:
        left_motor_state="Reversing"
    else:
        left_motor_state = "Stopped"

    if right_forward.value() == 1:
        right_motor_state="Forwarding"
    elif right_reverse.value() == 1:
        right_motor_state="Reversing"
    else:
        right_motor_state = "Stopped"
    
    html = """
    <html>
        <head> 
            <title>ESP Web Server</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="icon" href="data:,"> 
            <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
            h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
            border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
            .button2{background-color: #4286f4;}</style>
        </head>
        <body> 
            <h1>ESP Web Server</h1> 
            <p>Left Motor State: <strong>""" + left_motor_state + """</strong>Right Motor State: <strong>""" + right_motor_state + """</strong></p>
            <p><a href="/?cmd=lf"><button class="button">LF</button></a><a href="/?cmd=rf"><button class="button">RF</button></a></p>
            <p><a href="/?cmd=lr"><button class="button button2">LR</button></a><a href="/?cmd=rr"><button class="button button2">RR</button></a></p>
            <p><a href="/?cmd=bf"><button class="button">BF</button></a></p>
            <p><a href="/?cmd=br"><button class="button button2">BR</button></a></p>
            <p><a href="/?cmd=sp"><button class="button">Stop</button></a></p>
        </body>
    </html>"""
    return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    print(f'\nGot a connection from {addr}\n')
    request = conn.recv(1024)
    request = str(request)
    print(f'\nContent = {request}\n')


    if request.find('/?cmd=lf') == 6:
        print('Left Forward')
        left_forward.value(1)
        left_reverse.value(0)
        right_forward.value(0)
        right_reverse.value(0)
    elif request.find('/?cmd=lr') == 6:
        print('Left Reverse')
        left_forward.value(0)
        left_reverse.value(1)
        right_forward.value(0)
        right_reverse.value(0)
    elif request.find('/?cmd=rf') == 6:
        print('Right Forward')
        left_forward.value(0)
        left_reverse.value(0)
        right_forward.value(1)
        right_reverse.value(0)
    elif request.find('/?cmd=rr') == 6:
        print('Right Reverse')
        left_forward.value(0)
        left_reverse.value(0)
        right_forward.value(0)
        right_reverse.value(1)
    elif request.find('/?cmd=bf') == 6:
        print('Both Forward')
        left_forward.value(1)
        left_reverse.value(0)
        right_forward.value(1)
        right_reverse.value(0)
    elif request.find('/?cmd=br') == 6:
        print('Both Reverse')
        left_forward.value(0)
        left_reverse.value(1)
        right_forward.value(0)
        right_reverse.value(1)
    elif request.find('/?cmd=sp') == 6:
        print('Command stop')
        left_forward.value(0)
        left_reverse.value(0)
        right_forward.value(0)
        right_reverse.value(0)
    else:
        print('No command Stop')
        left_forward.value(0)
        left_reverse.value(0)
        right_forward.value(0)
        right_reverse.value(0)


    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
    print("Closed")