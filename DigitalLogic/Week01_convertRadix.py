def switchOverTen(x):
    dictTen = {
        0:'0',
        1:'1',
        2:'2',
        3:'3',
        4:'4',
        5:'5',
        6:'6',
        7:'7',
        8:'8',
        9:'9',
        10:'A',
        11:'B',
        12:'C',
        13:'D',
        14:'E',
        15:'F'
    }
    return dictTen.get(x)

def convertDecimal(base,number):
    reminder = base - int(base)
    stack = []
    answer = ""

    while base > 0:
        stack.append(switchOverTen(int(base%number)))
        base = int(base / number)
    while stack:
        answer+=stack.pop()

    if reminder != 0:
        answer += '.'
        for i in range(6):
            quo = int(reminder * number)
            answer += switchOverTen(quo)
            reminder = reminder * number - quo

    return answer

if __name__ == '__main__':
    input = 65535.2
    radix = 2
    output = convertDecimal(input,radix)
    print(repr(input)+"는 "+repr(radix)+ "진수로 변환시 "+repr(output)+"이 됩니다.")