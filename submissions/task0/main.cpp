#include <iostream>

using namespace std;



class Watched
{
public:
    static int t;
    static int Amount()
    {
        return t;
    }
};
int Watched::t = 0;
class Counted
{
public:
    Counted()
    {
        Watched::t++;
    }
    Counted(const Counted & c)
    {
        Watched::t++;
    }
};



int main()
{
    Counted b,c,d;
    Counted x = b;


    cout << Watched::Amount() << endl;
}
