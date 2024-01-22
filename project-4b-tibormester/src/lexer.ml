open TokenTypes

(* Part 1: Lexer - IMPLEMENT YOUR CODE BELOW *)

let sanitize s =
  (*matches anything after spaces tabs newlines with any char including newlines*)
  let whitespaces = (Str.regexp "^[ \t\n\r]+") in
  Str.replace_first whitespaces "" s


let tokenize input = 
  let rec h_tokenize words toks =
    let str = sanitize words in
    let tok_id = Str.regexp "[a-zA-Z][a-zA-Z0-9]*" in
    let tok_string = Str.regexp "\"[^\"]*\"" in 
    let tok_sanitized = Str.regexp "[^\"]*" in
    let tok_int = Str.regexp "[0-9]+\\|(-[0-9]+)" in
    let semi_re = Str.regexp ";;" in
    if String.length str = 0 then
      toks
    (*Tok_ID of string and all keywords that start lowercase*)
    else if Str.string_match tok_id str 0 then
      let tok = Str.matched_string str in
      let remaining = Str.replace_first tok_id "" str in
      if Str.string_match (Str.regexp "not$") tok 0 then
        h_tokenize remaining (toks @ [Tok_Not])
      else if Str.string_match (Str.regexp "if$") tok 0 then
        h_tokenize remaining (toks @ [Tok_If])
      else if Str.string_match (Str.regexp "then$") tok 0 then
        h_tokenize remaining (toks @ [Tok_Then])
      else if Str.string_match (Str.regexp "else$") tok 0 then
        h_tokenize remaining (toks @ [Tok_Else])
      else if Str.string_match (Str.regexp "let$") tok 0 then
          h_tokenize remaining (toks @ [Tok_Let])
      else if Str.string_match (Str.regexp "def$") tok 0 then
        h_tokenize remaining (toks @ [Tok_Def])
      else if Str.string_match (Str.regexp "in$") tok 0 then
        h_tokenize remaining (toks @ [Tok_In])
      else if Str.string_match (Str.regexp "rec$") tok 0 then
        h_tokenize remaining (toks @ [Tok_Rec])
      else if Str.string_match (Str.regexp "fun$") tok 0 then
        h_tokenize remaining (toks @ [Tok_Fun])
      (*Tok_Bool*)
      else if Str.string_match (Str.regexp "true$") tok 0 then
        h_tokenize remaining (toks @ [Tok_Bool true])
      else if Str.string_match (Str.regexp "false$") tok 0 then
        h_tokenize remaining (toks @ [Tok_Bool false])
      (*Tok_ID if all keywords fail*)
      else
        h_tokenize remaining (toks @ [Tok_ID tok])
    (*Tok_String*)
    else if Str.string_match tok_string str 0 then
      let remaining = Str.replace_first tok_string "" str in
      let quote = Str.matched_string str in
      if Str.string_match tok_sanitized quote 1 then
        let quoted = Str.matched_string quote in
        h_tokenize remaining (toks @ [Tok_String quoted])
      else
        raise(InvalidInputException("Failed to Lex String")) 
    (*Tok_Int*)
    else if Str.string_match tok_int str 0 then
      let remaining = Str.replace_first tok_int "" str in
      let matched = Str.matched_string str in
      let valu = Str.global_replace (Str.regexp "(\\|)") "" matched in
      h_tokenize remaining (toks @ [Tok_Int (int_of_string valu)])
    (*Tok_DoubleSemi*)
    else if Str.string_match semi_re str 0 then
      h_tokenize (Str.replace_first semi_re "" str) (toks @ [Tok_DoubleSemi])
    (*Tok_Arrow*)
    else if Str.string_match (Str.regexp "->") str 0 then
      h_tokenize (Str.replace_first (Str.regexp "->") "" str) (toks @ [Tok_Arrow])
    (*Tok_Concat*)
    else if Str.string_match (Str.regexp "\\^") str 0 then
      h_tokenize (Str.replace_first (Str.regexp "\\^") "" str) (toks @ [Tok_Concat])
    (*Tok_Div*)
    else if Str.string_match (Str.regexp "/") str 0 then
      h_tokenize (Str.replace_first (Str.regexp "/") "" str) (toks @ [Tok_Div])
    (*Tok_Mult*)
    else if Str.string_match (Str.regexp "\\*") str 0 then
      h_tokenize (Str.replace_first (Str.regexp "\\*") "" str) (toks @ [Tok_Mult])
    (*Tok_Sub*)
    else if Str.string_match (Str.regexp "-") str 0 then
      h_tokenize (Str.replace_first (Str.regexp "-") "" str) (toks @ [Tok_Sub])
    (*Tok_Add*)
    else if Str.string_match (Str.regexp "\\+") str 0 then
      h_tokenize (Str.replace_first (Str.regexp "\\+") "" str) (toks @ [Tok_Add])
    (*Tok_And*)
    else if Str.string_match (Str.regexp "&&") str 0 then
      h_tokenize (Str.replace_first (Str.regexp "&&") "" str) (toks @ [Tok_And])
    (*Tok_Or*)
    else if Str.string_match (Str.regexp "||") str 0 then
      h_tokenize (Str.replace_first (Str.regexp "||") "" str) (toks @ [Tok_Or])
    (*Tok_LessEqual*)
    else if Str.string_match (Str.regexp "<=") str 0 then
      h_tokenize (Str.replace_first (Str.regexp "<=") "" str) (toks @ [Tok_LessEqual])
    (*Tok_GreaterEqual*)
    else if Str.string_match (Str.regexp ">=") str 0 then
      h_tokenize (Str.replace_first (Str.regexp ">=") "" str) (toks @ [Tok_GreaterEqual])
    (*Tok_NotEqual*)
    else if Str.string_match (Str.regexp "<>") str 0 then
      h_tokenize (Str.replace_first (Str.regexp "<>") "" str) (toks @ [Tok_NotEqual])
    (*Tok_Less*)
    else if Str.string_match (Str.regexp "<") str 0 then
      h_tokenize (Str.replace_first (Str.regexp "<") "" str) (toks @ [Tok_Less])
    (*Tok_Greater*)
    else if Str.string_match (Str.regexp ">") str 0 then
      h_tokenize (Str.replace_first (Str.regexp ">") "" str) (toks @ [Tok_Greater])
    (*Tok_Equal*)
    else if Str.string_match (Str.regexp "=") str 0 then
      h_tokenize (Str.replace_first (Str.regexp "=") "" str) (toks @ [Tok_Equal])
    (*Tok_LParen*)
    else if Str.string_match (Str.regexp "(") str 0 then
      h_tokenize (Str.replace_first (Str.regexp "(") "" str) (toks @ [Tok_LParen])
    (*Tok_RParen*)
    else if Str.string_match (Str.regexp ")") str 0 then
      h_tokenize (Str.replace_first (Str.regexp ")") "" str) (toks @ [Tok_RParen])
    else  
      raise(InvalidInputException("Failed to Lex Token")) 
  in h_tokenize input []