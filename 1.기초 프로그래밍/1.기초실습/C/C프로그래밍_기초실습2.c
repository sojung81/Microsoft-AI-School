/*기본구문*/
/*#include <stdio.h>

int main()
{
    int i, j;
    
    for (i=0; i<10; i++)
    {
        for (j=0; j<i; j++)
        {
            printf("*");
        }
            printf("\n");
    }
        return 0;
}*/

/*continue써서 위의 구문을 별 5개만 출력, 현재의 구문은 살려면서 continue 사용
# include <stdio.h>

int main()
{
    int i, j;
    
    for (i=1; i<10; i++)
    {
        if (i > 5)
            continue;
        
        for (j=0; j<i; j++)
        {
            printf("*");
        }
        printf("\n");
    }
    return 0;
}*/


/*continue써서 위의 구문을 별 5개만 출력, 현재의 구문은 살려면서 break 사용
#include <stdio.h>

int main()
{
    int i, j;
    
    for (i=1; i<10; i++)
    {
        if (i > 5)
            break;
        
        for (j=0; j<i; j++)
        {
            printf("*");
        }
        printf("\n");
    }
    return 0;
}*/

//C언어 실습 - 벽에 튕기기
/*#include <stdio.h>
#include <unistd.h>

#define WIDTH 40
#define HEIGHT 12
#define SPEED 100000

int main(void)
{
    int x = 3, y = 2;
    int dx = 1, dy = 1;
    int i, j;

    // 화면 전체 지우기 (대문자 J)
    printf("\033[2J");

    while (1)
    {
        // 커서를 화면 왼쪽 위로 이동
        printf("\033[H");

        // 사각형 벽과 별 출력
        for (i = 0; i < HEIGHT; i++)
        {
            for (j = 0; j < WIDTH; j++)
            {
                // #으로 벽을 출력, *을 출력, 나머지는 공백
                if (i == 0 || i == HEIGHT - 1 || j == 0 || j == WIDTH - 1)
                    printf("#");
                else if (i==y && j==x)
                    printf("*");
                else
                    printf(" ");
            }
            printf("\n");
        }
        printf("Ctrl+C : Exit\n");

        fflush(stdout);

        // 0.1초 대기
        usleep(SPEED);

        // 다음 위치가 좌우 벽이면 가로 방향 반전
        if (x + dx == 0 || x + dx == WIDTH - 1)
            dx = -dx;

        // 다음 위치가 상하 벽이면 세로 방향 반전
        if (y + dy == 0 || y + dy == HEIGHT - 1)
            dy = -dy;

        // 바뀐 방향으로 별의 위치 변경
        x += dx;
        y += dy;
    }

    return 0;
}*/

/*여기서 스페이스 바 눌러서 공을 튕겨서 벽돌을 깨는 프로그램을 어떻게 만들 수 있을까?
벽돌은 벽안에 위쪽에 5겹으로 쌓여있고 공이랑 부딪히면 깨져야해*/
/*#include <stdio.h>
#include <unistd.h>
#include <termios.h>
#include <fcntl.h>
#define WIDTH 40
#define HEIGHT 12
#define SPEED 100000

int main(void)
{
    int x = 3, y = 2;
    int dx = 1, dy = 1;
    int i, j;

    // 화면 전체 지우기 (대문자 J)
    printf("\033[2J");

    while (1)
    {
        // 커서를 화면 왼쪽 위로 이동
        printf("\033[H");

        // 사각형 벽과 별 출력
        for (i = 0; i < HEIGHT; i++)
        {
            for (j = 0; j < WIDTH; j++)
            {
                // #으로 벽을 출력, *을 출력, 나머지는 공백
                if (i == 0 || i == HEIGHT - 1 || j == 0 || j == WIDTH - 1)
                    printf("#");
                else if (i==y && j==x)
                    printf("*");
                else
                    printf(" ");
            }
            printf("\n");
        }
        printf("Ctrl+C : Exit\n");

        fflush(stdout);

        // 0.1초 대기
        usleep(SPEED);

        // 다음 위치가 좌우 벽이면 가로 방향 반전
        if (x + dx == 0 || x + dx == WIDTH - 1)
            dx = -dx;

        // 다음 위치가 상하 벽이면 세로 방향 반전
        if (y + dy == 0 || y + dy == HEIGHT - 1)
            dy = -dy;

        // 바뀐 방향으로 별의 위치 변경
        x += dx;
        y += dy;
    }

    return 0;
}

int kbhit(void)
{
    struct termios oldt, newt;
    int ch;
    int oldf;

    tcgetattr(STDIN_FILENO, &oldt);
    newt = oldt;
    newt.c_lflag &= ~(ICANON | ECHO);
    tcsetattr(STDIN_FILENO, TCSANOW, &newt);
    oldf = fcntl(STDIN_FILENO, F_GETFL, 0);
    fcntl(STDIN_FILENO, F_SETFL, oldf | O_NONBLOCK);

    ch = getchar();

    tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
    fcntl(STDIN_FILENO, F_SETFL, oldf);

    if (ch != EOF)
    {
        ungetc(ch, stdin);
        return 1;
    }

    return 0;
}

int main(void)
{
    while (1)
    {
        if (kbhit())
        {
            char c = getchar();
            if (c == ' ')
            {
                // 스페이스 바가 눌렸을 때 공을 튕기도록 처리
                dy = -dy; // 세로 방향 반전
            }
        }

        // 기존의 공 이동 및 벽 충돌 처리 코드
        // ...
    }

    return 0;
}

int main(void)
{
    int x = 3, y = 2;
    int dx = 1, dy = 1;
    int i, j;

    // 화면 전체 지우기 (대문자 J)
    printf("\033[2J");

    while (1)
    {
        // 커서를 화면 왼쪽 위로 이동
        printf("\033[H");

        // 사각형 벽과 별 출력
        for (i = 0; i < HEIGHT; i++)
        {
            for (j = 0; j < WIDTH; j++)
            {
                // #으로 벽을 출력, *을 출력, 나머지는 공백
                if (i == 0 || i == HEIGHT - 1 || j == 0 || j == WIDTH - 1)
                    printf("#");
                else if (i==y && j==x)
                    printf("*");
                else
                    printf(" ");
            }
            printf("\n");
        }
        printf("Ctrl+C : Exit\n");

        fflush(stdout);

        // 0.1초 대기
        usleep(SPEED);

        // 다음 위치가 좌우 벽이면 가로 방향 반전
        if (x + dx == 0 || x + dx == WIDTH - 1)
            dx = -dx;

        // 다음 위치가 상하 벽이면 세로 방향 반전
        if (y + dy == 0 || y + dy == HEIGHT - 1)
            dy = -dy;

        // 바뀐 방향으로 별의 위치 변경
        x += dx;
        y += dy;
    }

    return 0;
}*/


//C언어 - 배열 (1차원)
/*
#include <stdio.h>

int main()
{
    int i;
    int person[5];

    person[0] = 10;
    person[1] = 20;
    person[2] = 30;
    person[3] = 40;
    person[4] = 50;
    int sum = 0;

    for (i = 0; i < 5; i++)
    {
        sum += person[i];
        printf("person[%d] = %d\n", i, person[i]);
    }

    printf("sum = %d\n", sum);
        
    return 0;
}
*/

/*c언어 코딩하기 - 배열 100개 선언
#include <stdio.h>

int main()
{
    int i,j;
    int person[100];
    int sum=0;

    for (i=0; i<100; i++)
    {
        person[i] = i+1;
        sum += person[i];
        printf("person[%d] = %d\n", i, person[i]);
    }
    
    printf("sum = %d\n", sum);
    return 0;
}
*/

//c언어 코딩 - 2차원 배열
/*#include <stdio.h>

int main()
{
    int i, j;
    int score[10][3]; //30개의 변수를 선언

    score[0][0] = 90; //값을 직접 대입
    score[0][1] = 85; //값을 직접 대입
    score[0][2] = 95; //값을 직접 대입

    for (i=0; i<10; i++)
    {
        score[i][0] = i; //2차원 배열 요소를 i로 지정
        score[i][1] = i; //2차원 배열 요소를 i로 지정
        score[i][2] = i; //2차원 배열 요소를 i로 지정    
    }

    for (i=0; i<10; i++)
    {
        for (j=0; j<3; j++)
        {
            printf("i=%d, j=%d, value=%d \n", i, j, score[i][j]);
        }
    }
    return 0;
}*/

//c언어 코딩하기 - 벽에 튕기기 배열
/*
#include <stdio.h>
#include <unistd.h>

#define WIDTH 40
#define HEIGHT 12
#define SPEED 100000

int main()
{
    int i,j;
    int wall[WIDTH][HEIGHT];

    for (i=0; i<HEIGHT; i++)
    {
        for (j=0; j<WIDTH; j++)
        {
            if (i==0 || i==HEIGHT-1 || j==0 || j==WIDTH-1)
                printf("#");
            else printf(" ");
        }
        printf("\n");
    }

    printf("person[%d][%d] = %d\n%d\n", i, j, wall[i][j]);
    return 0;
}*/

// Online C compiler (editor)
// Write and run C online using this editor.

#include <stdio.h>
#include <unistd.h>

#define WIDTH 40
#define HEIGHT 12
#define SPEED 100000

/*int main(void)
{
    int x=3, y=2;
    int dx=1, dy=1;
    int i, j;
    int board[HEIGHT][WIDTH] = {0};

volatile sig_atomic_t running = 1;

// Ctrl+C를 누르면 실행
void stop(int sig)
{
    running = 0;
}

    while (1)
        {
         printf("\033[H\033[J");

            for (i=0; i<HEIGHT; i++)
            {
                for (j=0; j<WIDTH; j++)
                {
                    if (i==0 || i==HEIGHT-1 || j==0 || j==WIDTH-1)
                    {
                        printf("#");
                    }
                    else if (i==y && j==x)
                    {
                        printf("*");
                    }
                    else
                    {
                        printf(" ");
                    }
                }
                printf("\n");
            }

            
            // 좌우 벽에 부딪히면 방향 전환
            if (x + dx == 0 || x + dx == WIDTH-1)
            {
                dx = -dx;
            }

            // 위아래 벽에 부딪히면 방향 전환
            if (y + dy == 0 || y + dy == HEIGHT-1)
            {
                dy = -dy;
            }

            // 위치 이동
            x += dx;
            y += dy;

            usleep(SPEED);
        }
    return 0;
}*/

//문자열
/*
#include <stdio.h>

void main()
{

    for (i=0; i<5; i++)
        {
            printf("%d번째 문자의 값 %c \n", i, array[i]);
        }

    char* pstr = "아름다운 지구입니다. \n";
    char string[] ] "How do you do! \n";

    printf("문자열 출력1 %s", pstr);
    printf("문자열 출력2 %s", string);
}
*/

//포인터
/*
#include <stdio.h>

void main(void)
{
    int i=5;

    printf("i의 값 : %d\n",i);
    printf("i의 메모리번지 : %d\n", &i); //i의 메모리 주소 출력
}*/

//포인터2-두 변수의 값을 교환
/*
#include <stdio.h>

void Swab(int a, int b)
{
    int tmp;
    tmp = a;
    a = b;
    b = tmp;
    printf("Swab: %d, %d\n", a, b);
}

int main(void)
{
    int a = 3, b = 100;
    Swab(a, b);
    printf("main: %d, %d\n", a, b);
    return 0;
}
*/


/*#include <stdio.h>

void Swab(int* a, int* b)
{
    int tmp;
    tmp = *a;
    *a = *b;
    *b = tmp;
    printf("Swab: %d, %d\n", *a, *b);
}

int main(void)
{
    int a = 3, b = 100;
    Swab(&a, &b);
    printf("main: %d, %d\n", a, b);
    return 0;
}*/

#include <stdio.h>

int a=3, b=100;

void swab()
{
    int tmp;
    tmp = a;
    a=b;
    b=tmp;
    printf("swab:%d, %d\n", a, b);
}

int main(void)
{
    swab();
    printf("main:%d, %d\n",a,b);
    return 0;
}