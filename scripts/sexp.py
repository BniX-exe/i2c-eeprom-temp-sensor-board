"""Small lossless-token S-expression reader for KiCad files."""
import re, json
def parse(text):
    stack=[]; root=None
    for t in re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+',text):
        if t=='(':
            n=[]
            if stack: stack[-1].append(n)
            stack.append(n)
        elif t==')': root=stack.pop()
        else: stack[-1].append(t)
    return root
def children(n,key): return [x for x in n if isinstance(x,list) and x and x[0]==key]
def child(n,key): return next((x for x in children(n,key)),None)
def value(t): return json.loads(t) if t.startswith('"') else t
def q(t): return json.dumps(str(t),ensure_ascii=False)
def dump(n,depth=0):
    if not isinstance(n,list): return n
    if not any(isinstance(x,list) for x in n): return '('+' '.join(n)+')'
    out='('; first=True
    for x in n:
        if isinstance(x,list): out+='\n'+'\t'*(depth+1)+dump(x,depth+1)
        else: out+=('' if first else ' ')+x
        first=False
    return out+'\n'+'\t'*depth+')'
