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
    """
    :param base: base number which is converted into radix-'number' number
    :param number: radix number
    :return: nothing, just print converted number
    """
    reminder = base - int(base)
    stack = []
    answer = ""
    # if Radix number is between 2~9
    if number in range(2,9):
        while base > 0:
            stack.append(int(base % number))
            base = int(base / number)
        while stack:
            answer+=str(stack.pop())

        if reminder != 0:
            answer+='.'
            for i in range(6):
                quo = int(reminder*number)
                answer+=str(quo)
                reminder = reminder*number - quo

    # if Radix number is 16
    else:
        while base > 1:
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

    print(answer)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    convertDecimal(45.75,7)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
