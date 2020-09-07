from math import log
import argparse


def months_to_years_and_months(months):
    years = 0
    while months >= 12:
        years += 1
        months -= 12
    m_s = f'{months} month' if months > 0 else ''
    if months > 1:
        m_s += 's'
    y_s = f'{years} year' if years > 0 else ''
    if years > 1:
        y_s += 's'
    if y_s != '' and m_s != '':
        return y_s + ' and ' + m_s
    return y_s + m_s


def n(principal, payment, interest):
    # You need 8 years and 2 months to repay this credit!
    i = (interest / 12) / 100
    n = log(payment / (payment - i * principal), 1 + i)
    if int(n) < n:
        n = int(n) + 1
    return n, months_to_years_and_months(n)


def a(principal, periods, interest):
    # Your annuity payment = 21248!
    i = (interest / 12) / 100
    a = principal * i * pow(1 + i, periods) / (pow(1 + i, periods) - 1)
    if int(a) < a:
        a = int(a) + 1
    return int(a)


def p(payment, periods, interest):
    # Your credit principal = 800000!
    i = (interest / 12) / 100
    p = payment / ((i * pow(1 + i, periods)) / (pow(1 + i, periods) - 1))
    # if int(p) < p:
    #     p = int(p) + 1
    return int(p)


def diff(principal, periods, interest):
    i = (interest / 12) / 100
    results = []
    for j in range(periods):
        a = principal / periods + i * (principal - (principal * j / periods))
        if int(a) < a:
            a = int(a) + 1
        results.append(int(a))
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Credit calculator parameters')
    parser.add_argument('--type', type=str, help='Type of operation (diff or annuity)')
    parser.add_argument('--principal', type=int, help='Credit principal')
    parser.add_argument('--periods', type=int, help='Total periods (usually months)')
    parser.add_argument('--interest', type=float, help='Credit interest')
    parser.add_argument('--payment', type=int, help='Payment per period')
    args = vars(parser.parse_args())

    credit_type = args["type"]
    principal = float(args["principal"]) if args["principal"] else None
    payment = float(args["payment"]) if args["payment"] else None
    periods = int(args["periods"]) if args["periods"] else None
    interest = float(args["interest"]) if args["interest"] else None

    nones_counter = 0
    for arg in args:
        if args[arg] is None:
            nones_counter += 1

    if nones_counter != 1 or interest is None:
        print('Incorrect parameters')
    elif credit_type == 'diff':
        payments = diff(principal, periods, interest)
        for i, pey in enumerate(payments):
            print(f'Month {i + 1}: paid out {pey}')
        print(f'\nOverpayment = {sum(payments) - principal:.0f}')
    else:
        if not periods:
            periods, periods_string = n(principal, payment, interest)
            print('You need ' + periods_string + ' to repay this credit!')
        elif not payment:
            payment = a(principal, periods, interest)
            print(f'Your annuity payment = {payment}!')
        elif not principal:
            principal = p(payment, periods, interest)
            print(f'Your credit principal = {principal}!')

        print(f'Overpayment = {payment * periods - principal:.0f}')
