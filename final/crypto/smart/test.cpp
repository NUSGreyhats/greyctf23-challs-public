#include <iostream>
#include <array>

typedef long long ll;

using namespace std;

const ll p = 823, q = 733, r = 947, s = 877;


array<ll,4> f(array<ll,4>& v) {
    ll a = (5 * v[0] + 3 * v[1] + 7 * v[2] + 4 * v[3] + v[0] * v[1] + 10 * (v[2] * v[3])*(v[2] * v[3])) % p;
    ll b = (9 * v[0] + 2 * v[1] + 1 * v[2] + 1 * v[3] + v[1] * v[2] + 11 * (v[0] * v[3])*(v[0] * v[3])) % q;
    ll c = (6 * v[0] + 7 * v[1] + 3 * v[2] + 9 * v[3] + v[2] * v[3] + 12 * (v[0] * v[1])*(v[0] * v[1])) % r;
    ll d = (8 * v[0] + 5 * v[1] + 2 * v[2] + 7 * v[3] + v[3] * v[0] + 13 * (v[1] * v[2])*(v[1] * v[2])) % s;

    return {a,b,c,d};
}


int main() {
    ll a,b,c,d;
    cin >> a >> b >> c >> d;
    array<ll, 4> target = {a,b,c,d};
    array<ll, 4> v = {a,b,c,d};
    array<ll, 4> v2 = {a,b,c,d};

    for (ll i = 0, e = 1e8; i < e; i++) {
        v = f(v);
        v2 = f(v2);
        v2 = f(v2);
        if (v == v2) {
            cout << i << endl;
            break;
        }
    }
}