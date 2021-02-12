#include <bits/stdc++.h>

using namespace std;

vector<vector<int>> graph;
vector<int> visited;
int start = -1;

bool detected_cycle(int prev, int node){

    visited[node] = 2;

    bool edge_have_cycle = false;

    for(auto edge : graph[node]){

        if(prev != edge) {
            if(visited[edge] == -1){
                edge_have_cycle = edge_have_cycle or detected_cycle(node, edge);
            }

            if(visited[edge] == 2){
                start = edge;
                edge_have_cycle = true;
            }
        }
    }

    visited[node] = 1;

    // if some edge is in the cycle and i'am not the start of the cycle propagate that
    if(edge_have_cycle)
        cout << "-> "<<  node << endl;

    return edge_have_cycle and (start != node);
}

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

    graph.resize(n);
    visited = vector<int>(n, -1);

    int a, b;
    for(int i = 0; i<m; ++i){

        cout << "Insira a ligação" << endl;
        cin >> a >> b;

        graph[a].push_back(b);
        graph[b].push_back(a);
    }

    show_graph();

    cout << "Nós que fazem parte do ciclo" << endl;
    detected_cycle(-1, 0);

    return 0;
}
