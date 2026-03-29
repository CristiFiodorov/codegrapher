class Processor {
public:
    int state;

    Processor(int initial) {
        if (initial < 0) {
            throw -1;
        }
        state = initial;
    }

    int process(int items[], int n) {
        int result = 0;
        for (int i = 0; i < n; i++) {
            try {
                if (items[i] < 0) {
                    throw items[i];
                }
                result += items[i];
            } catch (int e) {
                if (e == -1) {
                    continue;
                }
                result = 0;
                break;
            }
        }
        return result;
    }

    int nested_try(int a, int b) {
        int result;
        try {
            try {
                if (b == 0) {
                    throw -1;
                }
                result = a / b;
            } catch (int inner) {
                if (a > 0) {
                    result = a;
                } else {
                    throw -2;
                }
            }
            result += 1;
        } catch (int outer) {
            result = -999;
        }
        return result;
    }
};

int classify_and_sum(int data[], int n) {
    int pos_sum = 0;
    int neg_count = 0;

    for (int i = 0; i < n; i++) {
        switch (data[i] > 0 ? 1 : (data[i] < 0 ? -1 : 0)) {
            case 1:
                pos_sum += data[i];
                if (pos_sum > 1000) {
                    return pos_sum;
                }
                break;
            case -1:
                neg_count++;
                if (neg_count > 5) {
                    goto bail;
                }
                break;
            case 0:
                continue;
        }
    }

    if (neg_count == 0) {
        return pos_sum;
    }
    return pos_sum - neg_count;

bail:
    return -1;
}

int deep_nesting(int matrix[][10], int rows, int cols) {
    int total = 0;
    for (int i = 0; i < rows; i++) {
        if (i % 2 == 0) {
            for (int j = 0; j < cols; j++) {
                if (matrix[i][j] > 0) {
                    while (matrix[i][j] > 10) {
                        matrix[i][j] /= 2;
                        if (matrix[i][j] == 7) {
                            break;
                        }
                    }
                    total += matrix[i][j];
                } else if (matrix[i][j] == 0) {
                    continue;
                } else {
                    total--;
                }
            }
        } else {
            for (int j = cols - 1; j >= 0; j--) {
                total += matrix[i][j];
            }
        }
    }
    return total;
}

void multi_loop_break(int items[], int n) {
    int i = 0;
    while (i < n) {
        for (int j = 0; j < n; j++) {
            if (items[j] == items[i]) {
                if (i != j) {
                    goto found_dup;
                }
                continue;
            }
        }
        i++;
    }
    return;

found_dup:
    items[i] = -1;
    return;
}

int state_machine_v2(int inputs[], int n) {
    int state = 0;
    int output = 0;

    for (int i = 0; i < n; i++) {
        switch (state) {
            case 0:
                if (inputs[i] == 1) {
                    state = 1;
                } else if (inputs[i] == 2) {
                    state = 2;
                } else {
                    continue;
                }
                output++;
                break;
            case 1:
                switch (inputs[i]) {
                    case 0:
                        state = 0;
                        break;
                    case 3:
                        state = 2;
                        output += 10;
                        break;
                    default:
                        output++;
                        break;
                }
                break;
            case 2:
                if (inputs[i] < 0) {
                    return output;
                }
                state = 0;
                break;
        }
    }
    return output;
}

int main() {
    Processor p(1);
    int items[] = {1, -1, 2, -3, 4};
    p.process(items, 5);
    p.nested_try(10, 0);

    classify_and_sum(items, 5);

    int mat[3][10] = {{1,2,3},{4,5,6},{7,8,9}};
    deep_nesting(mat, 3, 3);

    multi_loop_break(items, 5);

    int inputs[] = {1, 3, 0, 2, -1};
    state_machine_v2(inputs, 5);
    return 0;
}
