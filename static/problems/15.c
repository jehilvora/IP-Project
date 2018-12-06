#include <iostream>
using namespace std;

int main() {
	// your code goes here
	int t;
	cin>>t;
	while(t--)
	{
		int n , o = 0 , temp;
		cin>>n;
		for(int i = 0 ; i < n ; i++)
		{
			cin>>temp;
			if(temp % 2 == 1)
				o++;
		}
		if(o % 2 == 1 && n != 1)
			cout<<2<<endl;
		else
			cout<<1<<endl;
	}
	return 0;
}