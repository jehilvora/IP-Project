#include <stdio.h>

int main(){
    int t;
    scanf("%d",&t);
    while(t--){
        int n;
        scanf("%d",&n);
        int ans;
        if(n%2==0){
            ans=n-n/2;
        }else ans=n-(n/2+1);
        printf("1 1");
        for(int i=0;i<ans;i++){
            printf("0");
        }
        printf("\n");
    }
}