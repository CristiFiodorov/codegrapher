class SampleHarder {

    int value;

    SampleHarder(int v) {
        if (v < 0) {
            throw new ArgumentException("negative");
        }
        value = v;
    }

    int NestedTryCatch(int a, int b) {
        int result;
        try {
            try {
                if (b == 0) {
                    throw new DivideByZeroException("zero");
                }
                result = a / b;
            } catch (DivideByZeroException) {
                if (a > 0) {
                    result = a;
                } else {
                    throw new InvalidOperationException("both bad");
                }
            }
            result += 1;
        } catch (InvalidOperationException) {
            result = -999;
        } finally {
            Console.WriteLine("outer finally");
        }
        return result;
    }

    int TryInLoop(int[] items) {
        int sum = 0;
        foreach (int item in items) {
            try {
                if (item < 0) {
                    throw new ArgumentException("neg");
                }
                sum += 100 / item;
            } catch (DivideByZeroException) {
                sum += -1;
                if (sum < -10) {
                    break;
                }
            } catch (ArgumentException) {
                continue;
            } finally {
                Console.WriteLine("processed");
            }
        }
        return sum;
    }

    int SwitchWithLoops(int[] data) {
        int state = 0;
        int output = 0;

        for (int i = 0; i < data.Length; i++) {
            switch (state) {
                case 0:
                    if (data[i] > 0) {
                        state = 1;
                    } else if (data[i] < 0) {
                        state = 2;
                    } else {
                        continue;
                    }
                    output++;
                    break;
                case 1:
                    for (int j = 0; j < data[i]; j++) {
                        output += j;
                        if (output > 100) {
                            return output;
                        }
                    }
                    state = 0;
                    break;
                case 2:
                    if (data[i] == -99) {
                        return -1;
                    }
                    output -= data[i];
                    state = 0;
                    break;
            }
        }
        return output;
    }

    void MultiGoto(int a, int b) {
        int result = 0;

        if (a < 0) {
            goto error_a;
        }
        if (b < 0) {
            goto error_b;
        }
        if (a == b) {
            goto equal;
        }

        result = a * b;
        goto done;

    error_a:
        result = -1;
        goto done;

    error_b:
        result = -2;
        goto done;

    equal:
        result = a * a;

    done:
        Console.WriteLine(result);
    }

    int DeepNesting(int[] items) {
        int total = 0;
        int i = 0;
        while (i < items.Length) {
            if (items[i] > 0) {
                for (int j = 0; j < items[i]; j++) {
                    if (j % 2 == 0) {
                        try {
                            if (items[i] / (j + 1) > 10) {
                                throw new OverflowException("too big");
                            }
                            total += items[i] / (j + 1);
                        } catch (OverflowException) {
                            continue;
                        }
                    } else {
                        total += 1;
                    }
                }
            } else if (items[i] == 0) {
                i++;
                continue;
            } else {
                return total;
            }
            i++;
        }
        return total;
    }

    int SwitchFallthrough(int code) {
        int result = 0;
        switch (code) {
            case 1:
            case 2:
            case 3:
                result = code * 10;
                break;
            case 4:
                result = 40;
                goto case 5;
            case 5:
                result += 50;
                break;
            case 6:
                if (code > 5) {
                    result = 60;
                    break;
                }
                goto case 7;
            case 7:
                result = 70;
                break;
            default:
                result = -1;
                break;
        }
        return result;
    }

    void NestedDoWhile(int limit) {
        int i = 0;
        do {
            int j = 0;
            do {
                if (i == j) {
                    j++;
                    continue;
                }
                if (i + j > limit * 2) {
                    break;
                }
                j++;
            } while (j < limit);
            i++;
            if (i == 3) {
                continue;
            }
        } while (i < limit);
    }

    void UsingWithTry(string path) {
        try {
            using (var reader = new StreamReader(path)) {
                string line;
                while ((line = reader.ReadLine()) != null) {
                    if (line.StartsWith("#")) {
                        continue;
                    }
                    if (line == "END") {
                        break;
                    }
                    Console.WriteLine(line);
                }
            }
        } catch (IOException) {
            Console.WriteLine("IO error");
        } finally {
            Console.WriteLine("done");
        }
    }

    void Run() {
        NestedTryCatch(10, 0);
        NestedTryCatch(-5, 0);
        int[] items = {1, 0, -1, 2, 3};
        TryInLoop(items);
        SwitchWithLoops(items);
        MultiGoto(3, -1);
        DeepNesting(items);
        SwitchFallthrough(4);
        NestedDoWhile(4);
        UsingWithTry("test.txt");
    }
}
