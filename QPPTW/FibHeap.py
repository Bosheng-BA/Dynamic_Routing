import math

class FibNode:
    def __init__(self, label):
        self.label = label  # 存储标签元组
        self.key = label[0]  # 使用标签的第一个元素作为键值
        self.degree = 0
        self.p = None
        self.child = None
        self.left = None
        self.right = None
        self.mark = False

    def get_child(self, cn):
        cn.p = self
        self.degree = self.degree + 1
        if self.child == 0:
            self.child = cn
            cn.left = cn
            cn.right = cn
        else:
            c = self.child
            cn.right = c
            cn.left = c.left
            cn.left.right = cn

    def print_node(self):
        if self.child != 0:
            c = self.child
            cl = c.left
            while 1:
                print("%d has child: %d" % (self.key, c.key))
                c.print_node()
                if cl == c:
                    break
                c = c.right

    def search_child(self, key):
        w = self
        v = self
        res = 0
        while 1:
            if w.key == key:
                return w
            if w.child != 0:
                res = w.child.search_child(key)
            if res != 0:
                return res
            w = w.right
            if w == v:
                return 0


def make_heap():
    return Fib(0, 0)


class Fib():
    def __init__(self, n, minx):
        self.n = n
        self.min = minx

    def insert(self, x):
        if self.min == 0:
            self.min = x
            x.left = x
            x.right = x
        else:
            x.right = self.min
            x.left = self.min.left
            x.left.right = x
            if x.key < self.min.key:
                self.min = x
        self.n = self.n + 1

    def minimum(self):
        return self.min

    def extract_min(self):
        z = self.min
        if z != 0:
            if z.child != 0:
                c = z.child
                while c.p != 0:
                    cpr = c.left
                    c.p = 0
                    c.left = 0
                    c.right = 0
                    c.right = self.min
                    c.left = self.min.left
                    c.left.right = c
                    self.min.left = c
                    c = cpr
            z.right.left = z.left
            z.left.right = z.right
            z.child = 0
            if z == z.right:
                self.min = 0
            else:
                self.min = z.right
                self.condolidate()
            self.n = self.n - 1
        return z

    def consolidate(self):
        A = []
        for i in range(0, int((math.log(self.n, 2) + 1))):
            A.append(0)
        w = self.min
        t = w.left
        while 1:
            temp = w.right
            x = w
            print("is %d " % w.key)
            d = x.degree
            while A[d] != 0:
                y = A[d]
                if x.key > y.key:
                    v = x
                    x = y
                    y = v
                self.Link(y, x)
                A[d] = 0
                d = d + 1
            A[d] = x
            if w == t:
                break
            w = temp

        self.min = 0
        for i in range(0, int(math.log(self.n, 2) + 1)):
            if A[i] != 0:
                if self.min == 0:
                    self.min = A[i]
                    self.left = A[i]
                    self.right = A[i]
                else:
                    A[i].right = self.min
                    A[i].left = self.min.left
                    A[i].left.right = A[i]
                    self.min.left = A[i]
                    if A[i].key < self.min.key:
                        self.min = A[i]

    def link(self, y, x):
        y.right.left = y.left
        y.left.right = y.right
        y.p = x
        x.degree = x.degree + 1
        y.mark = False
        if x.child == 0:
            x.child = y
            y.left = y
            y.right = y
        else:
            c = x.child
            y.right = c
            y.left = c.left
            y.left.right = y
            c.left = y

    def decrease_key(self, x, k):
        pass
        x = self.find_node(x)
        if k > x.key:
            print("error: new key is greater than current key!")
        x.key = k
        y = x.p
        if y != 0 and x.key < y.key:
            self.cut(x, y)
            self.cascut(y)
        if x.key < self.min.key:
            self.min = x

    def cut(self, x, y):
        pass
        if y.degree == 1:
            y.child = 0
            x.p = 0
        else:
            if x == y.child:
                w = x.right
                w.left = x.left
                x.left.right = x.right
                y.child = w
            else:
                w = x.right
                w.left = x.left
                x.left.right = x.right
        y.degree = y.degree - 1
        self.insert(x)
        x.p = 0
        x.mark = False

    def delete(self, x):
        pass
        self.decrease_key(x, -1)
        self.extract_min()

    def find_node(self, key):
        pass
        w = self.min
        res = 0
        if w.key > key:
            return 0
        else:
            cr = w
            while 1:
                if cr.key == key:
                    return cr
                else:
                    if cr.child != 0:
                        res = cr.child.search_child(key)
                    if res != 0:
                        return res
                    cr = cr.right
                    if cr == w:
                        return 0

    def print_heap(self, key):
        pass
        root = self.min
        c = root
        print("min node and root node is: %d " % c.key)
        c.print_node()
        c = c.right
        while c != root:
            print("root node is :%d" % c.key)
            c.print_node()
            c = c.right
