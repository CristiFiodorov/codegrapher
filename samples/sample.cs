using System;

class Sample {

    static int Factorial(int n) {
        int result = 1;
        int i = 1;
        while (i <= n) {
            result *= i;
            i++;
        }
        return result;
    }

    static int Fibonacci(int n) {
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

    static int Classify(int value) {
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

    static int FindMax(int[] values) {
        int maxVal = values[0];
        foreach (int v in values) {
            if (v > maxVal) {
                maxVal = v;
            }
        }
        return maxVal;
    }

    static int CountPositive(int[] values) {
        int count = 0;
        int i = 0;
        do {
            if (values[i] > 0) {
                count++;
            }
            i++;
        } while (i < values.Length);
        return count;
    }

    static void Main() {
        int r = Factorial(5);
        int f = Fibonacci(10);
        int[] nums = {3, 1, 4, 1, 5, 9, 2, 6};
        int biggest = FindMax(nums);
        int pos = CountPositive(nums);
        int label = Classify(7);
    }
}
