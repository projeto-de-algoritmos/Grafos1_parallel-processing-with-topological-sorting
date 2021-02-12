#include <bits/stdc++.h>

using namespace std;

vector<vector<int>> graph;


void show_graph(){
    for(int i = 0; i<graph.size(); ++i){
        cout << i << ": ";

        for(auto node : graph[i])
            cout << node << " ";

        cout << endl;
    }
}

int main(){


    int n, m;

    cout << "Número de nos" << endl;
    cin >> n;

    cout << "Numero de ligações" << endl;
    cin >> m;

    graph = vector<vector<int>>(n);

    int a, b;
    for(int i = 0; i<m; ++i){

        cout << "Insira a ligação" << endl;
        cin >> a >> b;

        graph[a].push_back(b);
        graph[b].push_back(a);
    }

    show_graph();

    return 0;
}
