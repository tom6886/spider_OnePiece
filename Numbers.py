import Soup

def getNumbers():
    soup = Soup.get('http://www.ishuhui.com/archives/category/zaixianmanhua/op')
    maxNum = soup.select('.show-lump h2')[0].get_text()
    print('.'*10 + "请注意，1~388话为合集，共计40卷" +'.'*10)
    print('.'*10 + "可供下载范围1~40卷，389话~最新话" +'.'*10)
    print('.'*10 + "当前最新话为%s"%maxNum +'.'*10)
    begin = int(input(u'请输入开始的回数：\n'))
    end = int(input(u'请输入结束的回数：\n'))
    numbers = []
    if(begin>end):
        print('.'*10 + '开始回数不可以大于结束回数' +'.'*10)
        return
    if(begin<41 and end<41):
        for i in range(begin,end+1):
            numbers.append(i)
    elif(begin<41):
        for i in range(begin,41):
            numbers.append(i)
        if(end>388):
            for i in range(389,end+1):
                numbers.append(i)
    elif(begin>388):
        for i in range(begin,end+1):
            numbers.append(i)
    return numbers
    
