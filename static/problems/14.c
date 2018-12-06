#include <bits/stdc++.h>
using namespace std;
int main()
{
    int T;
    cin>>T; // Test cases
    assert(1 <= T && T <= 200000);
    int total_length = 0;
    while(T--){
        string a;
        cin>>a; // Sentence
        int N=a.size(); // Size of the sentence
        assert(N > 0 && N <= 500000);
        total_length+=N;
        for(int i=0;i<N;i++)
            assert(a[i] >= 'a' && a[i] <= 'z');
        if(N<4){ // If size is smaller than 4 then it can not contain "chef"
            cout<<"normal"<<endl;
            continue;
        }
        int cnt=0; // initial "chef" count = 0
        for(int i=3;i<N;i++){
            vector<bool> chef(26,0);
            chef[a[i]-'a']=1;
            chef[a[i-1]-'a']=1;
            chef[a[i-2]-'a']=1;
            chef[a[i-3]-'a']=1;
            if(chef['c'-'a'] && chef['h'-'a'] && chef['e'-'a'] && chef['f'-'a']) cnt++; // if found increase
        }
        if(cnt>0) cout<<"lovely "<<cnt<<endl;
        else cout<<"normal\n";
    }
    assert(total_length <= 2000000);
    return 0;
}