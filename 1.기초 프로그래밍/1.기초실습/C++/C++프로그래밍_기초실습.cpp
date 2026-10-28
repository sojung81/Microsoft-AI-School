/*coding-star.cpp-c__기초*/
/*
#include <iostream>

int main()
{
    using std::cout;
    using std::endl;

    int i,j;

    for (i=0; i<10; i++)
    {
        for (j=0; j<=i; j++)
        {
            cout << "*";
        }
        cout << endl;
    }
    return 0;
} */

//멤버변수, 멤버함수 - 클래스 멤버 변수,함수

#include <iostream>

class Star
{
    private: //외부에서 접근 금지
        int lines; //멤버 변수

    public: //외부에서 접근 허용
        void set(int value)
        {
            lines = value;
        }

        int get()
        {
            return lines;
        }
};

int main()
{
    Star star; //Star 객체를 선언
    star.set(500);

    std::cout << star.get();

    return 0;
}