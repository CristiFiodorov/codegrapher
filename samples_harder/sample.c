int parse_tokens(int tokens[], int n) {
    int result = 0;
    int i = 0;

    if (n <= 0) {
        goto done;
    }

    for (i = 0; i < n; i++) {
        switch (tokens[i]) {
            case 0:
                goto skip_token;
            case 1:
            case 2:
            case 3:
                result += tokens[i];
                break;
            case 99:
                goto done;
            default:
                if (tokens[i] < 0) {
                    result--;
                    continue;
                }
                result += 1;
                break;
        }

        if (result > 100) {
            goto overflow;
        }

    skip_token:
        ;
    }

    goto done;

overflow:
    result = -1;

done:
    return result;
}

int matrix_search(int mat[][10], int rows, int cols, int target) {
    int i, j;
    for (i = 0; i < rows; i++) {
        if (i % 2 == 0) {
            for (j = 0; j < cols; j++) {
                if (mat[i][j] == target) {
                    return i * 100 + j;
                }
                if (mat[i][j] > target) {
                    break;
                }
            }
        } else {
            for (j = cols - 1; j >= 0; j--) {
                if (mat[i][j] == target) {
                    return i * 100 + j;
                }
                if (mat[i][j] < target) {
                    break;
                }
            }
        }
    }
    return -1;
}

void nested_do_while(int limit) {
    int i = 0;
    do {
        int j = 0;
        do {
            if (i == j) {
                j++;
                continue;
            }
            if (i + j > limit) {
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

int switch_in_loop(int data[], int n) {
    int state = 0;
    int sum = 0;
    int i;

    for (i = 0; i < n; i++) {
        switch (state) {
            case 0:
                if (data[i] > 0) {
                    state = 1;
                } else if (data[i] < 0) {
                    state = 2;
                }
                break;
            case 1:
                sum += data[i];
                if (data[i] == 0) {
                    state = 0;
                }
                break;
            case 2:
                sum -= data[i];
                if (sum < -100) {
                    return sum;
                }
                if (data[i] > 0) {
                    state = 1;
                }
                break;
        }
    }
    return sum;
}

int multi_goto(int a, int b) {
    int r = 0;

    if (a < 0) {
        goto error_a;
    }
    if (b < 0) {
        goto error_b;
    }
    if (a == b) {
        goto equal;
    }

    r = a * b;
    goto done;

error_a:
    r = -1;
    goto done;

error_b:
    r = -2;
    goto done;

equal:
    r = a * a;

done:
    return r;
}

int main() {
    int tokens[] = {1, 0, 2, 3, -1, 99, 4};
    parse_tokens(tokens, 7);

    int mat[3][10] = {{1,2,3},{4,5,6},{7,8,9}};
    matrix_search(mat, 3, 3, 5);

    nested_do_while(4);

    int data[] = {1, 2, 0, -1, 3, -2};
    switch_in_loop(data, 6);

    multi_goto(3, 5);
    return 0;
}
