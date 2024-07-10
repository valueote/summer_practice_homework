def func_1d(x):
    return x ** 2 + 1
def grad_1d(x):
  return x * 2

def gradient_descent_1d(grad, cur_x=0.1, learning_rate=0.01, precision=0.0001, max_iters=10000):
  for i in range(max_iters):
    grad_cur = grad(cur_x)
    if abs(grad_cur) < precision:
      break # 当梯度趋近为 0 时，视为收敛
    cur_x = cur_x - grad_cur * learning_rate
    print("第", i, "次迭代，x 值为： ", cur_x)
    print("局部最小值 x =", cur_x)
  return cur_x
if __name__ == '__main__':
  gradient_descent_1d(grad_1d, cur_x=10, learning_rate=0.2, precision=0.000001, max_iters=10000)