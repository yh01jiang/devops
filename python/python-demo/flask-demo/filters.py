def do_fixed(data, length=2):
    return f"%.{length}f" % data



# 测试功能而已，实际不需要
if __name__ == '__main__':
    res = do_fixed(10,)
    print(res)
