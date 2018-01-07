import sys
from classifier import classify
from PIL import Image
from PIL import ImageDraw
from generator import new_captcha

picn = 200
picm = 100

charn = 100
charm = 100

charn2 = 30
charm2 = 30
def split_captcha(im):
    n = picn 
    m = picm
    im = im.resize((n, m))
    S = n * m
    l = 1
    a = [[0 for i in range(m)] for i in range(n)]
    cr = [[0 for i in range(m)] for i in range(n)]
    cg = [[0 for i in range(m)] for i in range(n)]
    cb = [[0 for i in range(m)] for i in range(n)]
    h = [[[0 for i in range(32)] for i in range(32)] for i in range(32)]
    tt = [[[0 for i in range(32)] for i in range(32)] for i in range(32)]
    o = [[[[False for i in range(n)] for i in range(32)] for i in range(32)] for i in range(32)]
    s = [0 for i in range(S)]
    now = [0 for i in range(n + 4)]
    s1 = [[0 for i in range(charm)] for i in range(charn)]
    s2 = [[0 for i in range(charm)] for i in range(charn)]
    s3 = [[0 for i in range(charm)] for i in range(charn)]
    s4 = [[0 for i in range(charm)] for i in range(charn)]
    rs = 0
    gs = 0
    bs = 0
    cut = [0 for i in range(100)]
    def fill(x, cn, back):
        s5 = [[0 for i in range(charm)] for i in range(charn)]
        s6 = [[0 for i in range(charm)] for i in range(charn)]
        for i in range(charn):
            for j in range(charm):
                if (i >= cn or j >= m):
                    s5[i][j] = 0
                if (i < cn and j < m):
                    if (abs(rs - cr[i + x][j]) <= 1 and abs(gs - cg[i + x][j]) <= 1 and abs(bs - cb[i + x][j]) <= 1):
                        s5[i][j] = 1
        up = 0
        dw = charn - 1
        lf = 0
        rt = charm - 1
        while (up <= dw):
            flag = 0
            for i in range(charm):
                if (s5[up][i] == 1):
                    flag = 1
            if (flag == 0):
                up = up + 1
            else:
                break;
        while (up <= dw):
            flag = 0
            for i in range(charm):
                if (s5[dw][i] == 1):
                    flag = 1
            if (flag == 0):
                dw = dw - 1
            else:
                break;
        while (lf <= rt):
            flag = 0
            for i in range(charn):
                if (s5[i][lf] == 1):
                    flag = 1
            if (flag == 0):
                lf = lf + 1
            else:
                break;
        while (lf <= rt):
            flag = 0
            for i in range(charn):
                if (s5[i][rt] == 1):
                    flag = 1
            if (flag == 0):
                rt = rt - 1
            else:
                break;
        n1 = dw - up + 1
        m1 = rt - lf + 1
        for i in range(n1):
            for j in range(m1):
                s6[i][j] = s5[i + up][j + lf]
        return s6, n1, m1   
    def gets(i, j, r, g, b, alpha = 256):
        cr[i][j] = int(r / 8)
        cg[i][j] = int(g / 8)
        cb[i][j] = int(b / 8)
        h[int(r / 8)][int(g / 8)][int(b / 8)] = h[int(r / 8)][int(g / 8)][int(b / 8)] + 1
        if (o[int(r / 8)][int(g / 8)][int(b / 8)][i] == False):
            o[int(r / 8)][int(g / 8)][int(b / 8)][i] = True
            tt[int(r / 8)][int(g / 8)][int(b / 8)] = tt[int(r / 8)][int(g / 8)][int(b / 8)] + 1
        gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
        return gray
    for i in range(n):
        for j in range(m):
            a[i][j] = gets(i, j, *im.getpixel((i,j)))
            s[i * m + j] = a[i][j]
    s.sort()
    i = 0
    mx = 0
    backcolor = s[1]
    while (i < S):
        j = i + 1
        while (j < S and s[j] == s[i]):
            j = j + 1
        if (j - i > mx):
            mx = j - i
            backcolor = s[i]
        i = j
    mx = 0

    for i in range(32):
        for j in range(32):
            for k in range(32):
                if (h[i][j][k] > mx and (i != 31 or j != 31 or k != 31) ):
                    mx = h[i][j][k]
                    back = i * 1024 + j * 32 + k
    mx = 0
    for i in range(32):
        for j in range(32):
            for k in range(32):
                if (h[i][j][k] > mx and i * 1024 + j * 32 + k != back and (i != 31 or j != 31 or k != 31) and tt[i][j][k] <= int(n * 3 / 5)):
                    mx = h[i][j][k]
                    rs = i
                    gs = j
                    bs = k
    la = 0
    cutline = 0
    cut[0] = 0
    for i in range(n):
        now[i] = 0
        for j in range(m):
            if (abs(rs - cr[i][j]) <= 1 and abs(gs - cg[i][j]) <= 1 and abs(bs - cb[i][j]) <= 1):
                now[i] = 1
    for i in range(n):
        if (now[i] == 0 and now[i - 1] == 1 and (now[i + 1] == 0 and now[i + 2] == 0 and now[i + 4] == 0) and i - cut[cutline] >= int(n / 10)):
            cutline = cutline + 1
            cut[cutline] = i
        la = now
    if (cut[4] == 0):
        cut[4] = 199
    s1, cn1, cm1 = fill(0, cut[1] + 1, backcolor)
    s2, cn2, cm2 = fill(cut[1] + 1, cut[2] - cut[1], backcolor)
    s3, cn3, cm3 = fill(cut[2] + 1, cut[3] - cut[2], backcolor)
    s4, cn4, cm4= fill(cut[3] + 1, cut[4] - cut[3], backcolor)    
    resize_image = Image.new('RGB',(cn1,cm1),(255,255,255))
    drawer=ImageDraw.Draw(resize_image)
    for i in range(cn1):
        for j in range(cm1):
            drawer.point((i,j),(s1[i][j],s1[i][j],s1[i][j]))
    resize_image = resize_image.resize((30,30))
    s1 = [[0 for i in range(charm2)] for i in range(charn2)]
    for i in range(30):
        for j in range(30):
            s1[i][j]=resize_image.getpixel((i,j))[0]
    
    resize_image = Image.new('RGB',(cn2,cm2),(255,255,255))
    drawer=ImageDraw.Draw(resize_image)
    for i in range(cn2):
        for j in range(cm2):
            drawer.point((i,j),(s2[i][j],s2[i][j],s2[i][j]))
    resize_image = resize_image.resize((30,30))
    s2 = [[0 for i in range(charm2)] for i in range(charn2)]
    for i in range(30):
        for j in range(30):
            s2[i][j]=resize_image.getpixel((i,j))[0]
    
    resize_image = Image.new('RGB',(cn3,cm3),(255,255,255))
    drawer=ImageDraw.Draw(resize_image)
    for i in range(cn3):
        for j in range(cm3):
            drawer.point((i,j),(s3[i][j],s3[i][j],s3[i][j]))
    resize_image = resize_image.resize((30,30))
    s3 = [[0 for i in range(charm2)] for i in range(charn2)]
    for i in range(30):
        for j in range(30):
            s3[i][j]=resize_image.getpixel((i,j))[0]
            
    resize_image = Image.new('RGB',(cn4,cm4),(255,255,255))
    drawer=ImageDraw.Draw(resize_image)
    for i in range(cn4):
        for j in range(cm4):
            drawer.point((i,j),(s4[i][j],s4[i][j],s4[i][j]))
    resize_image = resize_image.resize((30,30))
    s4 = [[0 for i in range(charm2)] for i in range(charn2)]
    for i in range(30):
        for j in range(30):
            s4[i][j]=resize_image.getpixel((i,j))[0]
   
    return s1, s2, s3, s4, cutline

def save(mat, ch, outfile):
    outline = [ch]
    for i in range(charn2):
        for j in range(charm2):
                outline.append(mat[i][j])
    print(str(outline).strip().strip().replace(',', '').replace('\'', ''), file = outfile)

def expand(mat):
    outline = []
    for i in range(charn2):
        for j in range(charm2):
                outline.append(mat[i][j])
    return outline

def generator_batch(infile):
    batchSize = 100
    batchFile = open(infile, 'w')
    for i in range(batchSize):
        print(infile, i)
        text, image = new_captcha()
        a, b, c, d, cl = split_captcha(image)
        if (cl == 4):
            save(a, text[0], batchFile)
            save(b, text[1], batchFile)
            save(c, text[2], batchFile)
            save(d, text[3], batchFile)
        else:
               print(-1, file = batchFile)
    batchFile.close()

if __name__ == '__main__':
    print(sys.argv)
    image = Image.open(sys.argv[1])
    a, b, c, d, cl = split_captcha(image)
    if (cl == 4):
        print(classify([expand(a), expand(b), expand(c), expand(d)]))
    else:
        print("Can't Classify.")
    

    
