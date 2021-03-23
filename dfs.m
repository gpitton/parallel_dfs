// Depth-first search implementation in magma.
// Usage: magma -b "s0:={1}" "n:=6" dfs.m
// will explore the elements of the power set of {1..6}
// that contain s0.


// A depth-first search on the power set of S,
function dfs(s0, S, marked)
    Include(~marked, s0);
    for i in S do
        si := Include(s0, i);
        if not si in marked then
            Srest := Exclude(S, i);
            mk := $$(si, Srest, marked);
            marked join:= mk;
        end if;
    end for;
    return marked;
end function;


s0 := eval(s0);
n := StringToInteger(n);
print ToString(dfs(s0, {1..n}, {}));
quit;

