#include <iostream>
#include <climits>
using namespace std;

int main() {
	// your code goes here
	int t;
	cin>>t;
	for(int j = 0 ; j < t ; j++)
	{
		int m , n , rx , ry , x = 0, y = 0 , l;
		char c;
		cin>>m>>n;
		cin>>rx>>ry;
		cin>>l;
		for(int i = 0 ; i < l ; i++)
		{
			cin>>c;
			switch(c)
			{
				case 'U':
				y += 1;
				break;
				case 'D':
				y -= 1;
				break;
				case 'L':
				x -= 1;
				break;
				case 'R':
				x += 1;
				break;
			}
		}
		cout<<"Case "<< j + 1 <<": ";
		if(x > m || y > n || x < 0 || y < 0)
			cout<<"DANGER"<<endl;
		else if(x == rx && y == ry)
			cout<<"REACHED"<<endl;
		else
			cout<<"SOMEWHERE"<<endl;
	}
	return 0;
}