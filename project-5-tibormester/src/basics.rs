/**
    Returns the sum 1 + 2 + ... + n
    If n is less than 0, return -1
**/
pub fn gauss(n: i32) -> i32 {
    if n >= 0 {
        (n * (n + 1)) / 2
    } else {
        -1 
    }
}

/**
    Returns the number of elements in the list that 
    are in the range [s,e]
**/
pub fn in_range(ls: &[i32], s: i32, e: i32) -> i32 {
    let mut count = 0;
    for &num in ls {
        if num >= s && num <= e {
            count += 1;
        }
    }
    count
}

/**
    Returns true if target is a subset of set, false otherwise

    Ex: [1,3,2] is a subset of [1,2,3,4,5]
**/
pub fn subset<T: PartialEq>(set: &[T], target: &[T]) -> bool {
    for element in target {
        if !set.contains(element) {
            return false;
        }
    }
    true
}

/**
    Returns the mean of elements in ls. If the list is empty, return None
    It might be helpful to use the fold method of the Iterator trait
**/
pub fn mean(ls: &[f64]) -> Option<f64> {
    let sum: f64 = ls.iter().sum();
    let count = ls.len();

    if count > 0 {
        Some(sum / count as f64)
    } else {
        None
    }
}

/**
    Converts a binary number to decimal, where each bit is stored in order in the array
    
    Ex: to_decimal of [1,0,1,0] returns 10
**/
pub fn to_decimal(ls: &[i32]) -> i32 {
    let mut decimal = 0;

    for &bit in ls {
        decimal = (decimal << 1) + bit;
    }

    decimal
}

/**
    Decomposes an integer into its prime factors and returns them in a vector
    You can assume factorize will never be passed anything less than 2

    Ex: factorize of 36 should return [2,2,3,3] since 36 = 2 * 2 * 3 * 3
**/
pub fn factorize(n: u32) -> Vec<u32> {
    let mut factors = Vec::new();
    let mut num = n;

    for factor in 2..=n {
        while num % factor == 0 {
            factors.push(factor);
            num /= factor;
        }
        if num == 1 {
            break;
        }
    }

    factors
}

/** 
    Takes all of the elements of the given slice and creates a new vector.
    The new vector takes all the elements of the original and rotates them, 
    so the first becomes the last, the second becomes first, and so on.
    
    EX: rotate [1,2,3,4] returns [2,3,4,1]
**/
pub fn rotate(lst: &[i32]) -> Vec<i32> {
    let mut rotated = Vec::new();

    if !lst.is_empty() {
        rotated.extend_from_slice(&lst[1..]);
        rotated.push(lst[0]);
    }

    rotated
}

/**
    Returns true if target is a subtring of s, false otherwise
    You should not use the contains function of the string library in your implementation
    
    Ex: "ace" is a substring of "rustacean"
**/
pub fn substr(s: &String, target: &str) -> bool {
    let s_chars = s.chars().collect::<Vec<char>>();
    let target_chars = target.chars().collect::<Vec<char>>();
    let s_len = s_chars.len();
    let target_len = target_chars.len();

    if target_len == 0 {
        return true;
    }
    if target_len > s_len {
        return false;
    }
    for i in 0..=(s_len - target_len) {
        let window = &s_chars[i..i + target_len];
        if window == target_chars {
            return true;
        }
    }

    return false;
}

/**
    Takes a string and returns the first longest substring of consecutive equal characters

    EX: longest_sequence of "ababbba" is Some("bbb")
    EX: longest_sequence of "aaabbb" is Some("aaa")
    EX: longest_sequence of "xyz" is Some("x")
    EX: longest_sequence of "" is None
**/
pub fn longest_sequence(s: &str) -> Option<&str> {
    let mut longest_seq_start = 0;
    let mut longest_seq_end = 0;
    let mut longest_seq_len = 0;
    let mut current_seq_start = 0;
    let mut current_seq_end = 0;

    let chars = s.chars().collect::<Vec<char>>();
    let len = chars.len();

    for i in 1..len {
        if chars[i] == chars[current_seq_start] {
            current_seq_end = i;
        } else {
            let current_seq_len = (current_seq_end - current_seq_start) + 1;

            if current_seq_len > longest_seq_len {
                longest_seq_start = current_seq_start;
                longest_seq_end = current_seq_end;
                longest_seq_len = current_seq_len;
            }

            current_seq_start = i;
            current_seq_end = i;
        }
    }
    if longest_seq_len > 0 {
        Some(&s[longest_seq_start..=longest_seq_end])
    } else {
        None
    }
}