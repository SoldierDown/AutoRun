from os import system

def get_input(str=''):
    return input('Press ' + str + ' and it is: ')
def done():
    print('Done: go to next round')
def maybe(str=''):
    print('May be ' + str)
def confirm(str=''):
    print(str + '. Done')
todo = True
while todo:
    input('Start a new round')
    system('CLS')
    pos1 = get_input('pos1')
    if pos1 == '4':
        pos4 = get_input('pos4')
        if pos4 == '5':
            confirm('2 or 3') # originally 3
            continue
        elif pos4 == '6':
            pos5 = get_input('pos5')
            if pos5 == 'z':
                confirm('3 or 2 or 7')
                continue
            elif pos5 == 'x':
                confirm('6 or 7')
                continue
            elif pos5 == 'd':
                done()
                continue
        elif pos4 == 'x':
            confirm('5 or 6 or 7')
        elif pos4 == 'z':
            pos5 = get_input('pos5')
            if pos5 == '5':
                confirm('2 or 3')
                continue
            elif pos5 == 'z' or pos5 == 'x':
                confirm('7 or 8')
                continue
            elif pos5 == '6':
                confirm('2 or 3')
                continue
            elif pos5 == 'd':
                done()
                continue
        elif pos4 == 'd':
            done()
            continue
    elif pos1 == 'z':
        pos4 = get_input('pos4')
        if pos4 == '5':
            pos2 = get_input('pos2')
            if pos2 == '4':
                confirm('5 or 3 or 6')
                continue
            elif pos2 == 'z':
                confirm('8 or 6 or 7')
                continue
            elif pos2 == 'd':
                done()
                continue
        elif pos4 == '6':
            pos5 = get_input('pos5')
            if pos5 == 'z':
                confirm('8 or 6 or 7')
                continue
            elif pos5 == 'x':
                confirm('6 or 7 or 8')
                continue
        elif pos4 == 'z':
            confirm('5 or 6 or 7 or 8')
            continue