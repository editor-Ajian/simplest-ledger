# -*- coding: utf-8-sig -*-

# this program will be the complete version
# the goal is make the architecture as clear as possible


import tools


def total_control():
    while True:
        print('请输入字符，按回车结束，以执行您想要的操作\n'
              '输入 “###”：初始化账本。注意，此操作将会使您已有的账本丢失，请谨慎使用这一操作\n'
              '输入 “1”：记录您的现金收支\n'
              '输入 “2”：记录他人对你的欠账或清偿账款\n'
              '输入 “3”：清点账本，即清点所有原始记录，汇总出收支情况和债权情况\n'
              '输入 “4”：查询功能，可按月查询收支情况，或者按债务人姓名查询欠账情况\n'
              '输入 “q"：退出程序')
        choice_1 = input('请输入：')

        if choice_1 == '###':
            tools.initialize_ledger()
        elif choice_1 == '1':
            executor, monthly_income = tools.get_data_from_history(0)
            log_set = tools.input_event(0, executor)
            tools.deal_with_new_log(0, log_set, executor, monthly_income)
        elif choice_1 == '2':
            executor, monthly_income, debt_data = tools.get_data_from_history(1)
            log_set = tools.input_event(1, executor)
            tools.deal_with_new_log(1, log_set, executor, monthly_income, debt_data)
        elif choice_1 == '3':
            tools.form_a_whole_summary()
        elif choice_1 == '4':
            tools.check()
        elif choice_1 == 'q':
            break
        else:
            print('错误！请输入有效的字符')
            continue


if __name__ == '__main__':
    total_control()