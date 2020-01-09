# this file is to store function used in the simple ledger system


import time
import csv
from statistics import mode


def get_time():
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return timestamp


def rewrite_whole_csv(file_name, data_list, mode_used=1):
    # 本函数用在会把 csv 文件整个覆盖、写入之时
    # 因为在非 w 的写入模式中，定位到需要改写的位置比较麻烦，所以基本采取全表重写的方案
    # 默认模式 1 一次仅写入 1 行，即接收的 data_list 是一个集合且元素中没有集合
    # 用于初始化原始记录、初始化经手人收支表
    # 模式 2 一次写入多行，即接受的 data_list 中的元素皆为集合
    # 用于更新经手人收支表、初始化及更新应收帐统计表
    with open(file_name, 'w+', encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if mode_used == 1:
            writer.writerow(data_list)
        elif mode_used == 2:
            writer.writerows(data_list)


def initialize_ledger():
    # 初始化原始记录表
    raw_log_head = ['流水号', '发生年月', '事项', '类型（0 为现金收支，1 为欠账/清帐）',
                    '货主', '金额', '经手人', '记账时间']
    rewrite_whole_csv('原始流水记录.csv', raw_log_head)

    # 初始化经手人收支表
    print('输入经手人姓名，多个姓名间以中文符号逗号 “，” 分隔（例：“张XX，刘XX"）')
    executor = input('请输入:').split('，')
    executor.insert(0, '发生年月')
    rewrite_whole_csv('月度收支表.csv', executor)

    # 初始化债务人姓名表
    print('输入几位常用的债务人姓名，多个姓名间以中文符号逗号 “，” 分割（例：“张XX，刘XX”）')
    debtor_name = input('请输入：').split('，')
    debtor_data = []
    for name in debtor_name:
        debtor_data.append([name, 0])
    rewrite_whole_csv('应收帐统计.csv', debtor_data, mode_used=2)


def get_data_from_history(mode_used):
    # 先读取月度收支表中的数据，组装出一个经手人姓名列表以及一个字典
    # 字典以发生年月为 key，具体收支情况为 value（也是一个 list）
    # list 中元素的位置与原数据相同
    monthly_income = {}
    with open('月度收支表.csv', 'r', encoding='utf-8-sig', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for item in reader:
            if item[0] == '发生年月':
                executor = item[1:]
            else:
                if monthly_income.get(item[0]) is None:
                    monthly_income[item[0]] = item

    if mode_used == 0:
        # 注意顺序
        return executor, monthly_income
    elif mode_used == 1:
        # 如果使用模式 2，则还需读取债务人姓名数据
        # 为后续性能考量（查找及改写方便），将债务人数据组装成字典
        # 字典的 key 为债务人姓名，value 为 [姓名，金额]
        # 不组装成 list 还有一个原因是应收帐形式与月度收支表形式不同，不能共用一套函数
        # 因为写入 csv 需要用 list，所以写入时还需要一个 dict 转 list 的函数
        debt_data = {}
        with open('应收帐统计.csv', 'r', encoding='utf-8-sig', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for item in reader:
                if debt_data.get(item[0]) is None:
                    debt_data[item[0]] = item
        # 注意顺序
        return executor, monthly_income, debt_data


def get_nonce():
    # 只有原始流水记录表需要用到流水号
    with open('原始流水记录.csv', 'r', encoding='utf-8-sig', newline='') as csvfile:
        reader = csv.reader(csvfile)
        number_of_event = 0
        for item in reader:
            number_of_event += 1
    # 因为原始记录表至少有 head 一条，因此 number 必然大于等于 1
    # 从 1 开始计数，也没啥大不了，对吧。只要一直递增就好了
    return number_of_event


def get_happened_time():
    # 为获取用户主动输入的发生年月
    while True:
        print('请输入该项事务发生的年月。例：19 年 12 月请输入 “1912”\n'
              '20 年 2 月请输入 “2002”\n'
              '输入其他类型的字符会导致报错并重来\n')
        happened_time = input('请输入:')
        try:
            int(happened_time)
            if len(happened_time) == 4:
                break
            else:
                pass
        except:
            pass

    return happened_time


def get_debtor(dict_2):
    useful_list = []
    for key in dict_2:
        useful_list.append(dict_2[key][0])

    info = ''
    for n in range(0, len(useful_list)):
        info += '{}. {}\n'.format(str(n + 1), useful_list[n])

    print('请通过输入序号来选择货主\n'
          '如果列表中不存在您想要输入的姓名，请直接输入\n')
    print(info)

    while True:
        th = input('请输入：')
        try:
            num = int(th) - 1
            if num < len(useful_list):
                return useful_list[num]
            else:
                print('输入错误，请输入合适序号或新的姓名\n')
        except:
            return th


def get_cash_amount():
    while True:
        print('请输入该项事务涉及的钱额\n'
              '例：在现金交易中，获得 100 元请输入 “100”，支出 80 元请输入 “-80”\n'
              '如果是赊账/还钱，赊账 500 请输入“500”，还款 1000 请输入“-1000”'
              '输入其他类型的字符会导致报错并重来\n')
        amount_str = input('请输入：')
        try:
            amount_int = int(amount_str)
            break
        except:
            print('输入错误，请重新输入')

    return amount_int


def get_executor(list_2, type='经手人'):
    info = ''
    for n in range(0, len(list_2)):
        info += '{}. {}\n'.format(str(n + 1), list_2[n])

    print('请通过输入序号来选择' + type + '\n')
    print('如果想要输入的' + type + '姓名不在此列表中，请直接输入姓名\n')
    print(info)

    while True:
        th = input('请输入:')
        try:
            num = int(th) - 1
            if num < len(list_2):
                return list_2[num]
            else:
                print('输入错误，请输入合适序号或新的姓名\n')
        except:
            return th


def write_to_raw(file_name, list_3):
    # 此函数用的是追加模式，仅用于向原始流水表增加记录
    with open(file_name, 'a+', encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(list_3)


def input_event(event_type, executor_list, debtor_dict=None):
    # event_type 用来区分输入事件的不同类型
    # 0 表示简单的现金收支交易，给原始流水记录添加数据后只需更新月度收支表
    # 现金收支交易也无需记录货主姓名
    # 1 表示发生交易时没有结清货款的交易，以及清偿往日未付账款的交易
    # 此种交易必须记录货主姓名
    if debtor_dict is None:
        debtor_dict = {}
    log_set = []
    while True:
        event = [get_nonce(), get_happened_time(), input('请输入事项描述，按回车结束：')]
        # 先获取流水号。获得的数据是 int 也没关系，写入时会自动转为 str
        # note：有关系，后文在使用类型作判断时用的数据格式是 str，为了重用，这里也要用 str
        # 然后获取发生年月
        # 然后输入事项
        # 然后加入类型、货主
        if event_type == 0:
            event.append('0')
            event.append('')
        elif event_type == 1:
            event.append('1')
            event.append(get_debtor(debtor_dict))
        # 输入金额
        event.append(get_cash_amount())
        # 输入经手人
        event.append(get_executor(executor_list))
        event.append(get_time())
        # 将输入的事件记录先写入文件，后续操作不用再更新原始记录
        # 原始记录与统计结果的更新不同步，可能会导致两边对不上
        # 但我们已计划写校验函数，只需重用即可
        write_to_raw('原始流水记录.csv', event)

        # 传出这个以列表为元素的列表，方便统一处理
        log_set.append(event)
        print('请问是否还要添加记录？输入大写的 Y 表示继续；输入大写 N 会退出\n')
        while True:
            answer = input('请输入：')
            if answer == 'Y':
                break
            elif answer == 'N':
                return log_set
            else:
                print('输入错误！请输入正确的字符')


def get_location(word, list_4):
    for n in range(0, len(list_4)):
        if list_4[n] == word:
            return n


def deal_with_new_log(type, loglist_list, excutor_list, income_dict, debtor_dict=None):
    # 该函数的目的是输入新的事件记录，并根据此记录来更新统计表
    if debtor_dict is None:
        debtor_dict = {}

    print(loglist_list)
    print(excutor_list)
    print(income_dict)
    print(debtor_dict)

    for event in loglist_list:
        # 检验是否需要增加月度收入表中的条目
        if income_dict.get(event[1]) is None:
            income_dict[event[1]] = [event[1]]
            for n in range(0, len(excutor_list)):
                income_dict[event[1]].append(0)
        # 检验是否新增了经手人
        if event[6] not in excutor_list:
            excutor_list.append(event[6])
            for key in income_dict:
                income_dict[key].append(0)

    if type == 1:
        debtor_name = []
        for ele in debtor_dict:
            debtor_name.append(debtor_dict[ele][0])
        for event in loglist_list:
            if event[3] == '1':
                if event[4] not in debtor_name:
                    debtor_dict[event[4]] = [event[4], 0]

    # 以上的都是准备工作，保证数据对齐
    # 正式开始处理
    for event in loglist_list:
        if event[3] == '0':
            change_local = get_location(event[6], excutor_list) + 1
            income_dict[event[1]][change_local] = int(income_dict[event[1]][change_local]) + int(event[5])
        elif event[3] == '1':
            if int(event[5]) < 0:
                change_local = get_location(event[6], excutor_list) + 1
                income_dict[event[1]][change_local] = int(income_dict[event[1]][change_local]) - int(event[5])
    print(income_dict)

    if type == 1:
        for event in loglist_list:
            if event[3] == '1':
                print(debtor_dict)
                print(int(event[5]))
                debtor_dict[event[4]][1] = int(debtor_dict[event[4]][1]) + int(event[5])
    print(debtor_dict)

    # 已更新收入状况和债务统计
    # 为求俭省（避免进一步传出传入数据），直接在此函数内完成剩下的文件写入工作
    monthly_income_list = [excutor_list]
    monthly_income_list[0].insert(0, '发生年月')
    for key in income_dict:
        monthly_income_list.append(income_dict[key])
    rewrite_whole_csv('月度收支表.csv', monthly_income_list, mode_used=2)

    if type == 1:
        debt_list = []
        for key in debtor_dict:
            debt_list.append(debtor_dict[key])
        rewrite_whole_csv('应收帐统计.csv', debt_list, mode_used=2)


def read_from_raw():
    log_set = []
    with open('原始流水记录.csv', 'r', encoding='utf-8-sig', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for event in reader:
            if event[0] == '流水号':
                pass
            else:
                log_set.append(event)

    return log_set


def printer_result(file_name):
    with open(file_name, 'r', encoding='utf-8-sig', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for record in reader:
            print(record)


def form_a_whole_summary():
    log_set = read_from_raw()
    deal_with_new_log(1, log_set, [], {}, {})
    printer_result('月度收支表.csv')
    printer_result('应收帐统计.csv')


def check():
    while True:
        print('请使用序号选择查询模式\n'
              '1. 根据货主姓名查询原始交易记录\n'
              '2. 根据经手人姓名查询原始交易记录\n'
              '3. 查看经手人的月度收支余额\n'
              '4. 查看货主的欠款状况\n'
              '输入其它字符将退出退出查询模式\n')
        choice = input('请输入：')

        if choice == '1':
            log_set = read_from_raw()
            debtor = []
            for event in log_set:
                if event[4] not in debtor:
                    debtor.append(event[4])
            name = get_executor(debtor, '货主')
            for event in log_set:
                if event[4] == name:
                    print(event)
        elif choice == '2':
            log_set = read_from_raw()
            excutor = []
            for event in log_set:
                if event[6] not in excutor:
                    excutor.append(event[6])
            name = get_executor(excutor)
            for event in log_set:
                if event[6] == name:
                    print(event)
        elif choice == '3':
            printer_result('月度收支表.csv')
        elif choice == '4':
            printer_result('应收帐统计.csv')
        else:
            break


if __name__ == '__main__':
    form_a_whole_summary()
