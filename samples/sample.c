int factorial(int n) {
    int result = 1;
    int i = 1;
    while (i <= n) {
        result *= i;
        i++;
    }
    return result;
}

int fibonacci(int n) {
    if (n <= 1) {
        return n;
    }
    int a = 0;
    int b = 1;
    for (int i = 2; i <= n; i++) {
        int tmp = a + b;
        a = b;
        b = tmp;
    }
    return b;
}

int classify(int value) {
    int label = 0;
    switch (value % 3) {
        case 0:
            label = 1;
            break;
        case 1:
            label = 2;
            break;
        default:
            label = 3;
            break;
    }
    return label;
}

int find_max(int *values, int len) {
    int max_val = values[0];
    for (int i = 1; i < len; i++) {
        if (values[i] > max_val) {
            max_val = values[i];
        }
    }
    return max_val;
}

int count_positive(int *values, int len) {
    int count = 0;
    int i = 0;
    do {
        if (values[i] > 0) {
            count++;
        }
        i++;
    } while (i < len);
    return count;
}

int main() {
    int r = factorial(5);
    int f = fibonacci(10);
    int nums[] = {3, 1, 4, 1, 5, 9, 2, 6};
    int biggest = find_max(nums, 8);
    int pos = count_positive(nums, 8);
    int label = classify(7);
    return 0;
}
