import sys, os, configparser
from subprocess import Popen, TimeoutExpired

def check(ans_file, out_file):
    for (l1, l2) in zip(ans_file, out_file):
        if l1.rstrip() != l2.rstrip():
            return False
    return True

parser = configparser.ConfigParser()
parser.read('config.txt', encoding = 'UTF-8')
parser = parser['path']

testdir_base = parser['testdir_base']
testdir_folder = parser['testdir_folder']
testdir = os.path.join(testdir_base, testdir_folder)
exedir = parser['exedir']

in_ext = '.'+parser['in_ext']
out_ext = '.'+parser['out_ext']
ans_ext = '.ans'
timelimit = int(sys.argv[1])

print('\n---***---채점 시작---***---')

for test in os.listdir(testdir):
    in_absdir = os.path.join(testdir, test)
    if in_ext in in_absdir:
        ans_absdir = in_absdir.replace(in_ext, ans_ext)
        in_file = open(in_absdir, 'r')
        ans_file = open(ans_absdir, 'w')
        #print(name1, name2)
        proc = Popen([exedir], stdin = in_file, stdout = ans_file, stderr = ans_file, \
                     universal_newlines = True)
        try:
            proc.communicate(timeout = timelimit)
        except TimeoutExpired:
            print('Time Limit Exceeded on Test ' + test)
            proc.kill()
            continue
        
        if proc.returncode != 0:
            print('Runtime Error on Test ' + test)
        else:
            ans_file.close()
            ans_file = open(ans_absdir, 'r')
            out_absdir = in_absdir.replace(in_ext, out_ext)
            out_file = open(out_absdir, 'r')
            if check(ans_file, out_file):
                print('Correct Answer on Test ' + test)
            else:
                print('Wrong Answer on Test ' + test)
        
            
        
        
