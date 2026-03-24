n = int(input())

# Upper half
for i in range(1, n+1):
    print(" "*(n-i) + "* " * i)

# Lower half
for i in range(n, 0, -1):
    print(" "*(n-i) + "* " * i)