public class Sample {

    public static int factorial(int n) {
        int result = 1;
        int i = 1;
        while (i <= n) {
            result *= i;
            i++;
        }
        return result;
    }

    public static int fibonacci(int n) {
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

    public static int classify(int value) {
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

    public static int findMax(int[] values) {
        int maxVal = values[0];
        for (int v : values) {
            if (v > maxVal) {
                maxVal = v;
            }
        }
        return maxVal;
    }

    public static int countPositive(int[] values) {
        int count = 0;
        int i = 0;
        do {
            if (values[i] > 0) {
                count++;
            }
            i++;
        } while (i < values.length);
        return count;
    }

    public static void main(String[] args) {
        int r = factorial(5);
        int f = fibonacci(10);
        int[] nums = {3, 1, 4, 1, 5, 9, 2, 6};
        int biggest = findMax(nums);
        int pos = countPositive(nums);
        int label = classify(7);
    }
}
