/*마름모로 별 사이에 비어있는 공간을 만들기*/
/*#include <stdio.h>

int main(void) {
    for (int i = 0; i < 9; i++) {
        int n;

        if (i <= 4)
            n = 5 - i;
        else
            n = i - 3;

        for (int j = 0; j < 10; j++) {
            if (j < n || j >= 10 - n)
                printf("*");
            else
                printf(" ");
        }
        printf("\n");
    }

    return 0;
}*/

/*셀 삼각형 만들기 세번 반복
#include <stdio.h>

int main() {
    for (int i = 0; i < 3; i++)
    {
        for (int j = 0; j < 10; j++)
        {
            for (int k = 0; k <= j; k++)
            {
                printf("*");
            }
            printf("\n");
        }
    }
    return 0;
}*/

/* #include <stdio.h>

int main()
{
    int i, j;
    for (i=0; i<10; i++)
    {
        for(j=0; j<i; j++)
        {
            printf("*");
        }
        printf("\n");
    }
    return 0;
}
*/

/*coding-starfunc.c-함수를 이용한 삼각형 출력

#include <stdio.h>

int printStar()
{
    int i, j;
    for (i = 0; i < 10; i++)
    {
        for (j = 0; j <= i; j++)
        {
            printf("*");
        }
        printf("\n");
    }
    return 0;
}

int main()
{
    printStar();
    return 0;
}*/





/*int count 선언하고 printStar에 5 넣으면 전체 별 묶음이 5세트 출력된다
#include <stdio.h>

int printStar(int count)
{
    int i, j;
    for (int k = 0; k < count; k++)
    {
        for (i = 0; i < 10; i++)
        {
            for (j = 0; j <= i; j++)
            {
                printf("*");
            }
            printf("\n");
        }
    }
    return 0;
}

int main()
{
    int count;
    printStar(5);
    return 0;
}*/

/*coding-starfunc.c - 함수를 사용한 삼각형 출력*/
//하다가 제가 중간에 못했어요.. ㅠㅠ

/*#include <stdio.h>

int printStar(int start, int lines)
{
    int i, j;

    for (i=start; i<lines; i++)
    {
        for ()
    }
}*/