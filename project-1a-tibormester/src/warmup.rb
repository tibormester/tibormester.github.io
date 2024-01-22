def fib(n)
    arr = Array.new()
   
    for i in 0..n-1 do
        if arr.length >= 2 
            arr.push(arr[i-2] + arr[i-1])
        end 
        if arr.length == 1
            arr.push(1)
        end 
        if arr.length == 0
            arr.push(0)
        end
    end
    return arr
end

def isPalindrome(n)
    string = n.to_s
    length = string.length
    for i in 0..length/2
        if string[i] != string[length-(i+1)]
            return false
        end
    end
    return true
end

def nthmax(n, a)
    a.sort.reverse[n]
end

def freq(s)
    hash = {}
    for char in s.chars do
        if hash.keys.include?(char)
            hash.store(char, hash.fetch(char).+(1))
        else
            hash.store(char, 1)
        end
    end
    max = hash.values.max
    for char in hash.keys do
        if hash.fetch(char) == max
            return char
        end
    end
    return ""
end

def zipHash(arr1, arr2)
    if arr1.length != arr2.length
        return nil
    end
    hash = {}
    for i in 0..arr1.length-1 do
        hash.store(arr1[i], arr2[i])
    end
    return hash
end

def hashToArray(hash)
    arr = Array.new()
    for key in hash.keys do
        arr.push([key, hash.fetch(key)])
    end
    return arr
end

def maxProcChain(init, procs)
    vals = maxProcRecursion(init, procs, Array.new, Array.new)
    vals.max
end

def maxProcRecursion(init, procsRemaining, procsApplied, vals)
    #uneccessary cloning, removes the outer most proc composition to evaluate first
    procs = procsRemaining.clone
    proc = procs.pop
    #if there are no more procs, does base case of a(x) vs x
    if procs.length < 1
        valA = proc.call(init)
        valB = init
        #applies all the previous procs in the chain
        while procsApplied.length > 0 do
            proc = procsApplied.pop
            valA = proc.call(valA)
            valB = proc.call(valB)
        end
        #appends the calculated final vals to the array of all possible values
        vals.push(valA)
        vals.push(valB)
    else
        #branches the proc chain to either apply the current proc or not
        maxProcRecursion(init, procs, procsApplied, vals)
        maxProcRecursion(init, procs, procsApplied.push(proc), vals)
    end
    return vals
end
