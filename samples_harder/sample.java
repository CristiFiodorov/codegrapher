class SampleHarder {

    int value;

    SampleHarder(int v) {
        if (v < 0) {
            throw new IllegalArgumentException("negative");
        }
        value = v;
    }

    int nestedTryCatch(int a, int b) {
        int result;
        try {
            try {
                if (b == 0) {
                    throw new ArithmeticException("zero");
                }
                result = a / b;
            } catch (ArithmeticException inner) {
                if (a > 0) {
                    result = a;
                } else {
                    throw new RuntimeException("both bad");
                }
            }
            result += 1;
        } catch (RuntimeException outer) {
            result = -999;
        } finally {
            System.out.println("outer finally");
        }
        return result;
    }

    int tryInLoop(int[] items) {
        int sum = 0;
        for (int item : items) {
            try {
                if (item < 0) {
                    throw new IllegalArgumentException("negative");
                }
                sum += 100 / item;
            } catch (ArithmeticException e) {
                sum += -1;
                if (sum < -10) {
                    break;
                }
            } catch (IllegalArgumentException e) {
                continue;
            } finally {
                System.out.println("processed");
            }
        }
        return sum;
    }

    int switchWithLoops(int[] data) {
        int state = 0;
        int output = 0;

        for (int i = 0; i < data.length; i++) {
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

    int labeledBreaks(int[][] matrix) {
        int found = -1;
        outer:
        for (int i = 0; i < matrix.length; i++) {
            for (int j = 0; j < matrix[i].length; j++) {
                if (matrix[i][j] < 0) {
                    continue;
                }
                if (matrix[i][j] == 0) {
                    found = i;
                    break;
                }
                if (matrix[i][j] == 99) {
                    found = i * 100 + j;
                    break outer;
                }
            }
            if (found >= 0) {
                break;
            }
        }
        return found;
    }

    String deepNesting(int[] items) {
        StringBuilder sb = new StringBuilder();
        int i = 0;
        while (i < items.length) {
            if (items[i] > 0) {
                for (int j = 0; j < items[i]; j++) {
                    if (j % 2 == 0) {
                        try {
                            if (items[i] / (j + 1) > 10) {
                                throw new ArithmeticException("too big");
                            }
                            sb.append(items[i] / (j + 1));
                        } catch (ArithmeticException e) {
                            sb.append("E");
                            continue;
                        }
                    } else {
                        sb.append("-");
                    }
                }
            } else if (items[i] == 0) {
                i++;
                continue;
            } else {
                return sb.toString();
            }
            i++;
        }
        return sb.toString();
    }

    int switchFallthrough(int code) {
        int result = 0;
        switch (code) {
            case 1:
            case 2:
            case 3:
                result = code * 10;
                break;
            case 4:
                result = 40;
            case 5:
                result += 50;
                break;
            case 6:
                if (code > 5) {
                    result = 60;
                    break;
                }
            case 7:
                result = 70;
                break;
            default:
                result = -1;
                break;
        }
        return result;
    }

    void doWhileNested(int limit) {
        int i = 0;
        do {
            int j = 0;
            while (j < limit) {
                if (i == j) {
                    j++;
                    continue;
                }
                if (i + j > limit * 2) {
                    break;
                }
                j++;
            }
            i++;
            if (i == 3) {
                continue;
            }
        } while (i < limit);
    }

    void run() {
        nestedTryCatch(10, 0);
        nestedTryCatch(-5, 0);
        int[] items = {1, 0, -1, 2, 3};
        tryInLoop(items);
        switchWithLoops(items);
        int[][] matrix = {{1, 2, 99}, {-1, 0, 3}};
        labeledBreaks(matrix);
        deepNesting(items);
        switchFallthrough(4);
        doWhileNested(4);
    }
}
