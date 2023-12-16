#!/usr/bin/env python3
# x, y, z, w - helping variables
# s, t, r - copies

variables_pool = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}

def borrow_vars(n: int):
    return list(variables_pool)[:n]

def claim_vars(n: int):
    vars = list(variables_pool)[:n]
    for var in vars:
        variables_pool.remove(var)
    return vars

def claim_var(x: str):
    if x in variables_pool:
        variables_pool.remove(x)

def return_vars(*vars: str):
    for var in vars:
        variables_pool.add(var)

def unwrap(body: list[str]):
    return ''.join([x for x in body])

def set(a: str, n: int):
    claim_var(a)
    return "".join([a for i in range(n)]) + '\n'

def print_variable(a: str):
    return f"={a}\n"

def zero(a: str):
    return f"({a})"

def if_then(condition: str, body: list[str]):
    return f"({condition}({condition}){unwrap(body)})"

def if_else(cond: str, if_body: list[str], else_body: list[str]):
    x = claim_vars(1)[0]
    body = f"{x}({cond}({cond})({x}){unwrap(if_body)})({x}({x}){unwrap(else_body)})"
    return_vars(x)
    return body

def while_simple(var: str, body: list[str]):
    return f"({var}{unwrap(body)})"

def copy(a: str, b: str):
    x = borrow_vars(1)[0]
    return f"({a}{b}{x})({x}{a})"

def move(a: str, b: str):
    return f"({a}{b})"

def increment_variable(a: str):
    return f"{a}"

def swap(a: str, b: str):
    x = borrow_vars(1)[0]
    return f"({a}{x})({b}{a})({x}{b})"

# a += b
def add(a: str, b: str):
    x = borrow_vars(1)[0]
    return f"({b}{a}{x})({x}{b})"

# a = max(0, a - b)
def sub(a: str, b: str):
    y, z, w = claim_vars(3)
    body = unwrap([
        copy(b, y),
        copy(a, w),
        while_simple(a, [
            while_simple(y, [
                move(y, z),
                zero(w),
                copy(a, w)
            ]),
            move(z, y)
        ]),
        zero(y),
        zero(z),
        move(w, a)
    ])
    return_vars(y, z, w)
    return body

# a *= b
def mul(a: str, b: str):
    x, y = claim_vars(2)
    body = unwrap([
        copy(b, y),
        move(a, x),
        while_simple(b, [
            add(a, x)
        ]),
        move(y, b),
        zero(x)
    ])
    return_vars(x, y)
    return body

# a /= b
def div(a: str, b: str):
    r, u, w, s = claim_vars(4)
    body = unwrap([
        copy(a, r),
        while_simple(a, [
            a,
            zero(r),
            copy(a, r),
            sub(a, b),
            u,
        ]),
        copy(b, s),
        sub(b, r),
        if_else(b, [
            w,
            sub(u, w),
            zero(w),
        ],
        [
            zero(r)
        ]),
        zero(r),
        move(s, b),
        move(u, a)
    ])
    return_vars(r, u, w, s)
    return body

# a = a % b
def mod(a: str, b: str):
    r, s = claim_vars(2)
    body = unwrap([
        copy(a, r),
        while_simple(a, [
            a,
            zero(r),
            copy(a, r),
            sub(a, b),
        ]),
        copy(b, s),
        sub(b, r),
        if_else(b, [
        ],
        [
            zero(r)
        ]),
        move(s, b),
        move(r, a)
    ])
    return_vars(r, s)
    return body

def add_int(a: str, n: int):
    return "".join([a for _ in range(n)])

def mul_int(a: str, n: int):
    x = borrow_vars(1)[0]
    base = "".join([x for _ in range(n)])
    return f"({a}{base})({x}{a})"

# a = n^b
def exp(a: str, b: str, n: int):
    return unwrap([
        zero(a),
        add_int(a, 1),
        while_simple(b, [
            mul_int(a, n)
        ])
    ])

# a and b gen n-th fib number
def fib(a: str, b: str, n: int):
    z, x = claim_vars(2)
    body = unwrap([
        add_int(z, n),
        zero(a),
        zero(b),
        add_int(a, 1),
        while_simple(z, [
            copy(a, x),
            add(b, a),
            zero(b),
            move(x, b)
        ])
    ])
    return_vars(z, x)
    return body

def fib_var(a: str, b: str, z: str):
    x = claim_vars(1)[0]
    body = unwrap([
        zero(a),
        zero(b),
        add_int(a, 1),
        while_simple(z, [
            copy(a, x),
            add(a, b),
            zero(b),
            move(x, b)
        ])
    ])
    return_vars(x)
    return body

def if_a_g_b(a: str, b: str, body: list[str]):
    x, y = claim_vars(2)
    l_body = unwrap([
        copy(a, x),
        copy(b, y),
        sub(x, y),
        zero(y),
        if_then(x, body),
    ])
    return_vars(x, y)
    return l_body

# zeroes b, returns gcd in a
def gcd(a: str, b: str):
    return while_simple(b, [
        b,
        sub(a, b),
        if_a_g_b(b, a, [
            swap(a, b)
        ])
    ])


# a = sqrt(a), n iterations
def babilonian_method(a: str, n: int):
    x, z, s, m = claim_vars(4)
    body = unwrap([
        add_int(m, n),
        copy(a, s),
        add_int(x, 2),
        while_simple(m, [
            copy(a, z),
            div(z, s),
            add(s, z),
            div(s, x),
            zero(z),
        ]),
        zero(x),
        zero(a),
        move(s, a),
    ])

    return_vars(x, z, s, m)
    return body

def is_prime(a: str):
    x, three, z, f = claim_vars(4)
    body = unwrap([
        copy(a, x),
        babilonian_method(x, 10),
        add_int(x, 2),
        add_int(three, 3),
        add_int(f, 1),
        while_simple(x, [
            copy(a, z),
            mod(z, x),
            if_else(z, [

            ], [
                zero(f)
            ]),
            if_a_g_b(three, x, [
                zero(x)
            ])
        ]),
        zero(a),
        move(f, a),
        zero(three),
        zero(z)
    ])
    return_vars(x, three, z, f)
    return body

a, b, c = claim_vars(3)

program = [
    set(a, 27),
    print_variable(a),
    set(b, 9),
    print_variable(b),
    set(c, 144),
    print_variable(c),
    gcd(a, b),
    babilonian_method(c, 6),
    gcd(c, a),
    is_prime(c),
    '\n',
    print_variable(c)
]

print(unwrap(program))
